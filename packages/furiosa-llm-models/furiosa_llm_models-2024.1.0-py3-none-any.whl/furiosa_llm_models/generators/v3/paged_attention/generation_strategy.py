import abc
import copy
import logging
from typing import Dict, List, Optional, Tuple, Union

import torch
from transformers import PreTrainedModel
from transformers.generation import (
    BeamScorer,
)
from transformers.generation.logits_process import (
    LogitsProcessorList,
)
from transformers.generation.stopping_criteria import (
    StoppingCriteriaList,
    validate_stopping_criteria,
)
from transformers.generation.utils import BeamSearchDecoderOnlyOutput, GreedySearchDecoderOnlyOutput
from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions, CausalLMOutputWithPast

from ..packing import greedy_attention_packing
from .generation_utils import create_key_value_blocks

SUPPORTED_GENERATION_RETURN_DICT_TYPES = (CausalLMOutputWithPast, CausalLMOutputWithCrossAttentions)
logger = logging.getLogger(__name__)


class GenerationStrategy(abc.ABC):
    block_size = 1
    max_batch_size = 4

    def __init__(self, model: PreTrainedModel) -> None:
        self.model = model
        self.model_config = model.config

    def __call__(self, *args, **kwargs):
        return self.decode(*args, **kwargs)

    @abc.abstractmethod
    def decode(self, *args, **kwargs): ...

    def create_key_value_blocks(
        self,
        batch_size: int,
        bucket_size: int,
        kv_dtype: torch.dtype,
        device: torch.device,
    ) -> List[Tuple[torch.Tensor, torch.Tensor]]:
        batch_size = min(batch_size, self.max_batch_size)

        key_value_blocks = create_key_value_blocks(
            model_config=self.model_config,
            batch_size=batch_size,
            block_size=self.block_size,
            device=device,
            bucket_size=bucket_size,
            kv_dtype=kv_dtype,
        )

        _, block_size, _, _ = key_value_blocks[0][0].shape

        if bucket_size % block_size != 0:
            raise ValueError(
                f"Bucket size ({bucket_size}) should be divisible by block size ({block_size})"
            )

        if self.block_size != 1:
            raise ValueError(
                "Block size is fixed for RNGD architecture. Got block_size: {block_size} != 1"
            )

        return key_value_blocks

    def initialize_key_value_block_indices(
        self, key_value_blocks: List[Tuple[torch.Tensor, torch.Tensor]]
    ) -> torch.Tensor:
        block_indices, block_size, _, _ = key_value_blocks[0][0].shape
        self.block_size = block_size

        self.active_key_block_indices: List[List[int]] = []
        self.active_value_block_indices: List[List[int]] = []

        # Below fields keep track of prompt block indices which are shared across beam candidates
        self.prompt_key_block_indices: List[List[int]] = []
        self.prompt_value_block_indices: List[List[int]] = []

        self.available_block_indices = list(range(1, block_indices))
        self.zero_block_index = 0  # this is a special zero block
        self.total_block_count = block_indices

    def move_kv_cache_block_in_place(
        self, seq_idx: int, new_location: torch.Tensor, existing_block_indices: List[List[int]]
    ) -> None:
        # new key location should always be shape [batch, 1]
        for single_batch_block_indices, new_index in zip(existing_block_indices, new_location):
            single_batch_block_indices[seq_idx] = new_index.item()

    def reset(self):
        self.active_key_block_indices: List[List[int]] = []
        self.active_value_block_indices: List[List[int]] = []
        self.available_block_indices = list(range(1, self.total_block_count))


class GreedySearch(GenerationStrategy):
    def decode(
        self,
        input_ids: torch.LongTensor,
        attention_mask: torch.Tensor,
        logits_processor: Optional[LogitsProcessorList] = None,
        stopping_criteria: Optional[StoppingCriteriaList] = None,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[Union[int, List[int]]] = None,
        return_dict_in_generate: Optional[bool] = None,
        **model_kwargs,
    ):
        kv_dtype = model_kwargs.get("kv_dtype")
        if kv_dtype is None:
            raise ValueError("`kv_dtype` is required for Paged Attention.")

        device = input_ids.device
        batch_size = input_ids.shape[0]
        bucket_size = model_kwargs.get("bucket_size") or max_length

        if bucket_size is None:
            raise ValueError("`bucket_size` is required for Paged Attention.")

        key_value_blocks = model_kwargs.get("key_value_blocks") or self.create_key_value_blocks(
            batch_size, bucket_size, kv_dtype, device
        )
        self.initialize_key_value_block_indices(key_value_blocks)
        # ----------- initial_settings -----------------
        starting_input_ids = input_ids
        starting_attention_mask = attention_mask
        batch_size, prompt_len = starting_input_ids.shape

        # TODO(MAX BATCH CHECK ONLY EXISTS FOR THIS PYTHON GENERATOR)
        # In vllm, generate is async and inner scheduler decides which batch to use based on
        # memory allocation
        assert batch_size <= self.max_batch_size

        starting_position_ids = starting_attention_mask.long().cumsum(-1) - 1
        starting_position_ids.masked_fill_(starting_attention_mask == 0, 1)

        # ----------- adjust to bucket settings --------
        device = input_ids.device
        attention_mask = torch.zeros((batch_size, bucket_size), dtype=torch.int).to(device)
        attention_mask[:, :prompt_len] = starting_attention_mask

        input_ids = torch.full(
            (batch_size, bucket_size), fill_value=pad_token_id, dtype=torch.int
        ).to(device)
        input_ids[:, :prompt_len] = starting_input_ids

        position_ids = torch.zeros((batch_size, bucket_size), dtype=torch.long).to(device)
        position_ids[:, :prompt_len] = starting_position_ids

        sequence_idx = prompt_len - 1
        is_prefill = True

        scores = None

        batch_size = input_ids.shape[0]
        unfinished_sequences = torch.ones(batch_size, dtype=torch.long, device=input_ids.device)
        if isinstance(eos_token_id, int):
            eos_token_id = [eos_token_id]
        eos_token_id_tensor = torch.tensor(eos_token_id).to(input_ids.device)
        next_tokens = None

        # start generating new tokens
        for i in range(max_length - prompt_len):
            if is_prefill:
                (new_key_location, new_value_location) = self.prepare_prefill_input_metadata(
                    attention_mask
                )

                (
                    packed_input_ids,
                    _,
                    causal_mask,
                    packed_position_ids,
                    logit_target_locations,
                    new_key_location,
                    new_value_location,
                ) = self.prepare_prefill_inputs(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    new_key_location=new_key_location,
                    new_value_location=new_value_location,
                    pad_token_id=pad_token_id,
                )  # original attention mask, original position ids

                forward_kwargs = {
                    "input_ids": packed_input_ids,
                    "attention_mask": None,
                    "causal_mask": causal_mask,
                    "position_ids": packed_position_ids,
                    "past_key_values": key_value_blocks,
                    "new_key_location": new_key_location,
                    "new_value_location": new_value_location,
                    "past_valid_key_indices": None,
                    "past_valid_value_indices": None,
                    "is_prefill": is_prefill,
                    "bucket_size": bucket_size,
                    "use_cache": False,
                }

            else:
                (input_ids, attention_mask, position_ids) = self.prepare_decode_inputs(
                    next_input_ids=next_tokens,
                    prev_attention_mask=attention_mask,
                    is_first_decode=(True if i == 1 else False),  # FIXME: hacky
                    seq_idx=sequence_idx,
                )

                logit_target_locations = None  # for decode, not needed

                (
                    new_key_location,
                    new_value_location,
                    valid_key_indices,
                    valid_value_indices,
                ) = self.prepare_decode_input_metadata()

                forward_kwargs = {
                    "input_ids": input_ids,
                    "attention_mask": attention_mask,
                    "causal_mask": None,
                    "position_ids": position_ids,
                    "past_key_values": key_value_blocks,
                    "new_key_location": new_key_location,
                    "new_value_location": new_value_location,
                    "past_valid_key_indices": valid_key_indices,
                    "past_valid_value_indices": valid_value_indices,
                    "is_prefill": is_prefill,
                    "bucket_size": bucket_size,
                    "use_cache": False,
                }

            outputs = self.model(**forward_kwargs)

            if not is_prefill:
                # now copy the new_key location back to original place for decode_phase
                self.move_kv_cache_block_in_place(
                    seq_idx=sequence_idx,
                    new_location=new_key_location,
                    existing_block_indices=self.active_key_block_indices,
                )
                self.move_kv_cache_block_in_place(
                    seq_idx=sequence_idx,
                    new_location=new_value_location,
                    existing_block_indices=self.active_value_block_indices,
                )

            # done
            outputs = handle_outputs(outputs)

            # done
            next_tokens = self.find_next_tokens(
                outputs,
                logit_target_locations,
                starting_input_ids,
                logits_processor,
                unfinished_sequences,
                pad_token_id,
                is_prefill,
            )

            starting_input_ids = torch.cat([starting_input_ids, next_tokens[:, None]], dim=-1)

            if eos_token_id is not None:
                unfinished_sequences = unfinished_sequences.mul(
                    next_tokens.tile(eos_token_id_tensor.shape[0], 1)
                    .ne(eos_token_id_tensor.unsqueeze(1))
                    .prod(dim=0)
                )
                if unfinished_sequences.max() == 0:
                    break

            if stopping_criteria(starting_input_ids, scores):
                break

            sequence_idx += 1

            # prepare for next phase
            is_prefill = False

        # reset must be called
        self.reset()
        if return_dict_in_generate:
            return GreedySearchDecoderOnlyOutput(sequences=starting_input_ids, scores=scores)
        return starting_input_ids

    def prepare_prefill_input_metadata(
        self, attention_mask: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        for prefill, valid_key_indices and valid_value_indices are none
        return (new_key_location, new_value_location)
        """
        new_key_location = []  # shape = (batch, bucket_size)
        new_value_location = []  # shape = (batch, bucket_size)
        for single_attention_mask in attention_mask:
            # for each attention_mask add zero block for padding
            block_indices = []
            for val in single_attention_mask:
                if val == 0:
                    # padding
                    block_indices.append(self.zero_block_index)
                else:
                    block_indices.append(self.available_block_indices.pop())

            self.active_key_block_indices.append(block_indices[:])
            self.active_value_block_indices.append(block_indices)

        new_key_location = torch.IntTensor(self.active_key_block_indices)
        new_value_location = torch.IntTensor(self.active_value_block_indices)

        return (
            new_key_location,
            new_value_location,
        )

    def prepare_decode_input_metadata(
        self,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        return (new_key_location, new_value_location, valid_key_indices, valid_valie_indices)
        """
        new_key_location = []  # shape = (batch, 1)
        new_value_location = []  # shape = (batch, 1)
        valid_key_indices = []  # shape = (batch*(bucket_size -1))
        valid_value_indices = []  #
        for key_batch, value_batch in zip(
            self.active_key_block_indices, self.active_value_block_indices
        ):
            valid_key_indices.extend(key_batch[:-1])
            valid_value_indices.extend(value_batch[:-1])

            # we use same block idx for key and value here
            new_block_idx = self.available_block_indices.pop()

            key_batch[-1] = new_block_idx
            value_batch[-1] = new_block_idx

            new_key_location.append([new_block_idx])
            new_value_location.append([new_block_idx])

        new_key_location = torch.IntTensor(new_key_location)
        new_value_location = torch.IntTensor(new_value_location)
        valid_key_indices = torch.IntTensor(valid_key_indices)
        valid_value_indices = torch.IntTensor(valid_value_indices)

        return (
            new_key_location,
            new_value_location,
            valid_key_indices,
            valid_value_indices,
        )

    def prepare_prefill_inputs(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        new_key_location: torch.Tensor,
        new_value_location: torch.Tensor,
        pad_token_id: int,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, List[List[int]]]:
        """
        return (packed_input_ids, causal_mask, packed_position_ids, logit_target_locations, packed_new_key_locatoin, packed_new_value_location)
        """  # noqa: E501
        (
            packed_attention_mask,
            packed_input_ids,
            causal_mask,
            logit_target_locations,
            packed_position_ids,
            packed_new_key_location,
            packed_new_value_location,
        ) = greedy_attention_packing(
            input_ids,
            attention_mask,
            new_key_location,
            new_value_location,
            pad_token_id=pad_token_id,
        )
        return (
            packed_input_ids,
            packed_attention_mask,
            causal_mask,
            packed_position_ids,
            logit_target_locations,
            packed_new_key_location,
            packed_new_value_location,
        )

    def prepare_decode_inputs(
        self,
        next_input_ids: torch.Tensor,
        prev_attention_mask: torch.Tensor,
        is_first_decode: bool,
        seq_idx: int,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        return (input_ids, attention_mask, position_ids)
        """
        next_attention_mask = prev_attention_mask.clone()

        if is_first_decode:
            # Before: [[1, 1, 1, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0]]
            # After : [[1, 1, 1, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 0, 0, 1]]
            next_attention_mask[:, -1] = 1
        else:
            # Before: [[1, 1, 1, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 0, 0, 1]]
            # After : [[1, 1, 1, 1, 0, 0, 0, 1], [0, 1, 1, 1, 0, 0, 0, 1]]
            next_attention_mask[:, seq_idx - 1] = 1

        next_position_ids = next_attention_mask.long().cumsum(-1) - 1
        next_position_ids = next_position_ids[:, -1:]

        return (next_input_ids[:, None], next_attention_mask, next_position_ids)

    def find_next_tokens(
        self,
        logits: torch.Tensor,
        logit_target_locations: Optional[List[List[int]]],
        input_ids: torch.Tensor,
        logits_processor: Optional[LogitsProcessorList],
        unfinished_sequences: torch.Tensor,
        pad_token_id: int,
        is_prefill: bool,
    ) -> torch.Tensor:
        next_tokens_scores: torch.Tensor
        if is_prefill:
            # outputs should be logits which would have shape of [batch, seq_len, embedding_dimension] # noqa
            # loop through each batch and find the logit location due to attention_packing
            next_token_logits = []
            for single_batch_logit, single_batch_logit_target_location in zip(
                logits, logit_target_locations
            ):
                assert single_batch_logit.dim() == 2
                for logit_target in single_batch_logit_target_location:
                    # logit target will just be index
                    next_token_logits.append(
                        single_batch_logit[logit_target]
                    )  # will be [embedding_dimension]

            # stack this back to [batch, vocab_size]
            next_token_logits = torch.stack(next_token_logits)

        else:
            next_token_logits = logits[:, 0, :]  # for decode seq_len would just be 1

        next_tokens_scores = logits_processor(input_ids, next_token_logits)
        next_tokens = torch.argmax(next_tokens_scores, dim=-1)
        next_tokens = next_tokens * unfinished_sequences + pad_token_id * (1 - unfinished_sequences)
        return next_tokens


class BeamSearch(GreedySearch):
    def decode(
        self,
        input_ids: torch.LongTensor,
        attention_mask: torch.Tensor,
        beam_scorer: BeamScorer,
        logits_processor: Optional[LogitsProcessorList] = None,
        stopping_criteria: Optional[StoppingCriteriaList] = None,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[Union[int, List[int]]] = None,
        return_dict_in_generate: Optional[bool] = None,
        **model_kwargs,
    ):
        """
        Generate N number of new tokens for each sequence
        where N = max_length - len(starting_input_ids[0])
        """
        kv_dtype = model_kwargs.get("kv_dtype")
        if kv_dtype is None:
            raise ValueError("`kv_dtype` is required for Paged Attention.")

        device = input_ids.device
        batch_size = input_ids.shape[0]
        bucket_size = model_kwargs.get("bucket_size") or max_length

        if bucket_size is None:
            raise ValueError("`bucket_size` is required for Paged Attention.")

        key_value_blocks = model_kwargs.get("key_value_blocks") or self.create_key_value_blocks(
            batch_size, bucket_size, kv_dtype, device
        )
        self.initialize_key_value_block_indices(key_value_blocks)
        # ----------- initial_settings -----------------
        starting_input_ids = input_ids
        starting_attention_mask = attention_mask
        batch_size, prompt_len = starting_input_ids.shape

        starting_position_ids = starting_attention_mask.long().cumsum(-1) - 1
        starting_position_ids.masked_fill_(starting_attention_mask == 0, 1)

        # ----------- adjust to bucket settings --------
        attention_mask = torch.zeros((batch_size, bucket_size), dtype=torch.int).to(device)
        attention_mask[:, :prompt_len] = starting_attention_mask

        input_ids = torch.full(
            (batch_size, bucket_size), fill_value=pad_token_id, dtype=torch.int
        ).to(device)
        input_ids[:, :prompt_len] = starting_input_ids

        position_ids = torch.zeros((batch_size, bucket_size), dtype=torch.long).to(device)
        position_ids[:, :prompt_len] = starting_position_ids

        if isinstance(eos_token_id, int):
            eos_token_id = [eos_token_id]

        if max_length is not None:
            logger.warning(
                "`max_length` is deprecated in this function, use "
                "`stopping_criteria=StoppingCriteriaList(MaxLengthCriteria(max_length=max_length))`\
                      instead."
            )
            stopping_criteria = validate_stopping_criteria(stopping_criteria, max_length)

        # beam search config
        batch_size = len(beam_scorer._beam_hyps)
        num_beams = beam_scorer.num_beams
        batch_beam_size, _ = input_ids.shape
        # TODO(this is because we use bucketization)
        cur_len = prompt_len

        # TODO(MAX BATCH CHECK ONLY EXISTS FOR THIS PYTHON GENERATOR)
        # In vllm, generate is async and inner scheduler decides which batch to use based on
        # memory allocation
        assert batch_size // num_beams <= self.max_batch_size

        if num_beams * batch_size != batch_beam_size:
            raise ValueError(
                f"Batch dimension of `input_ids` should be {num_beams * batch_size}, "
                f"but is {batch_beam_size}."
            )

        beam_scores = torch.zeros(
            (batch_size, num_beams), dtype=torch.float, device=input_ids.device
        )
        beam_scores[:, 1:] = -1e9
        beam_scores = beam_scores.view((batch_size * num_beams,))
        scores = None
        beam_indices = None

        is_prefill = True
        is_first_decode = False
        next_input_ids = None
        generated_ids = starting_input_ids

        while True:
            if is_prefill:
                (new_key_location, new_value_location) = self.prepare_prefill_input_metadata(
                    attention_mask, batch_size, num_beams
                )
                (
                    packed_input_ids,
                    _,
                    causal_mask,
                    packed_position_ids,
                    logit_target_locations,
                    new_key_location,
                    new_value_location,
                ) = self.prepare_prefill_inputs(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    new_key_location=new_key_location,
                    new_value_location=new_value_location,
                    pad_token_id=pad_token_id,
                )  # original attention mask, original position ids

                forward_kwargs = {
                    "input_ids": packed_input_ids,
                    "attention_mask": None,
                    "causal_mask": causal_mask,
                    "position_ids": packed_position_ids,
                    "past_key_values": key_value_blocks,
                    "new_key_location": new_key_location,
                    "new_value_location": new_value_location,
                    "past_valid_key_indices": None,
                    "past_valid_value_indices": None,
                    "is_prefill": is_prefill,
                    "bucket_size": bucket_size,
                    "use_cache": False,
                }

                is_first_decode = True
            else:
                (next_input_ids, attention_mask, position_ids) = self.prepare_decode_inputs(
                    next_input_ids=next_input_ids,
                    prev_attention_mask=attention_mask,
                    is_first_decode=is_first_decode,
                    seq_idx=cur_len - 1,
                )

                logit_target_locations = None  # for decode, not needed

                (
                    new_key_location,
                    new_value_location,
                    valid_key_indices,
                    valid_value_indices,
                ) = self.prepare_decode_input_metadata()

                forward_kwargs = {
                    "input_ids": next_input_ids,
                    "attention_mask": attention_mask,
                    "causal_mask": None,
                    "position_ids": position_ids,
                    "past_key_values": key_value_blocks,
                    "new_key_location": new_key_location,
                    "new_value_location": new_value_location,
                    "past_valid_key_indices": valid_key_indices,
                    "past_valid_value_indices": valid_value_indices,
                    "is_prefill": is_prefill,
                    "bucket_size": bucket_size,
                    "use_cache": False,
                }

                is_first_decode = False

            outputs = self.model(**forward_kwargs)
            logits = handle_outputs(outputs)

            next_token_logits = self.find_next_tokens(logits, logit_target_locations, is_prefill)
            # hack: adjust tokens for Marian. For Marian we have to make sure that the `pad_token_id` # noqa
            # cannot be generated both before and after the `nn.functional.log_softmax` operation.
            next_token_logits = self.adjust_logits_during_generation(
                next_token_logits, cur_len=cur_len
            )
            next_token_scores = torch.nn.functional.log_softmax(
                next_token_logits, dim=-1
            )  # [batch_size * num_beams, vocab_size]

            next_token_scores_processed = logits_processor(generated_ids, next_token_scores)
            next_token_scores = next_token_scores_processed + beam_scores[:, None].expand_as(
                next_token_scores
            )

            vocab_size = next_token_scores.shape[-1]
            next_token_scores = next_token_scores.view(batch_size, num_beams * vocab_size)

            next_token_scores, next_tokens = torch.topk(
                next_token_scores, 2 * num_beams, dim=1, largest=True, sorted=True
            )
            next_indices = torch.div(next_tokens, vocab_size, rounding_mode="floor")
            next_tokens = next_tokens % vocab_size

            beam_outputs = beam_scorer.process(
                generated_ids,
                next_token_scores,
                next_tokens,
                next_indices,
                pad_token_id=pad_token_id,
                eos_token_id=eos_token_id,
                beam_indices=beam_indices,
            )
            beam_scores = beam_outputs["next_beam_scores"]
            beam_next_tokens = beam_outputs["next_beam_tokens"]
            beam_idx = beam_outputs["next_beam_indices"]

            generated_ids = torch.cat(
                [generated_ids[beam_idx, :], beam_next_tokens.unsqueeze(-1)], dim=-1
            )
            if not is_prefill:
                # now copy the new_key location back to original place for decode_phase
                self.move_kv_cache_block_in_place(
                    seq_idx=cur_len - 1,
                    new_location=new_key_location,
                    existing_block_indices=self.active_key_block_indices,
                )
                self.move_kv_cache_block_in_place(
                    seq_idx=cur_len - 1,
                    new_location=new_value_location,
                    existing_block_indices=self.active_value_block_indices,
                )
            # TODO(DONGHUN) based on this idx adjust the block index
            # we know new beams are chosen at this point
            new_key_block_indices = self.adjust_kv_cache_block(
                beam_idx, self.active_key_block_indices
            )
            self.active_key_block_indices = new_key_block_indices
            new_value_block_indices = self.adjust_kv_cache_block(
                beam_idx, self.active_value_block_indices
            )
            self.active_value_block_indices = new_value_block_indices

            cur_len = cur_len + 1
            if beam_scorer.is_done or stopping_criteria(generated_ids, scores):
                break

            # v2.Generator specific variables
            is_prefill = False
            next_input_ids = beam_next_tokens

        sequence_outputs = beam_scorer.finalize(
            generated_ids,
            beam_scores,
            next_tokens,
            next_indices,
            pad_token_id=pad_token_id,
            eos_token_id=eos_token_id,
            max_length=max_length,
            beam_indices=beam_indices,
        )

        # reset must be called for paged attention to call generate again
        self.reset()

        if return_dict_in_generate:
            return BeamSearchDecoderOnlyOutput(
                sequences=sequence_outputs["sequences"],
                sequences_scores=sequence_outputs["sequence_scores"],
                scores=scores,
                beam_indices=sequence_outputs["beam_indices"],
            )
        else:
            return sequence_outputs["sequences"]

    def prepare_prefill_input_metadata(
        self,
        attention_mask: torch.Tensor,
        batch_size: int,
        num_beams: int,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        for prefill, valid_key_indices and valid_value_indices are none
        return (new_key_location, new_value_location)
        """
        # beams belonging to same prompts should share blocks

        new_key_location = []  # shape = (batch, bucket_size)
        new_value_location = []  # shape = (batch, bucket_size)
        for count in range(batch_size):
            idx = count * num_beams
            single_attention_mask = attention_mask[idx]
            block_indices = []
            for val in single_attention_mask:
                if val == 0:
                    # padding
                    block_indices.append(self.zero_block_index)
                else:
                    block_indices.append(self.available_block_indices.pop())

            # at this point block has been created
            for _ in range(num_beams):
                self.active_key_block_indices.append(copy.deepcopy(block_indices))
                self.active_value_block_indices.append(copy.deepcopy(block_indices))

        new_key_location = torch.IntTensor(self.active_key_block_indices)
        new_value_location = torch.IntTensor(self.active_value_block_indices)

        return (
            new_key_location,
            new_value_location,
        )

    def adjust_kv_cache_block(
        self, beam_idx: torch.Tensor, existing_block_indices: List[List[int]]
    ):
        new_block_indices = []
        for idx in beam_idx:
            existing_block_index = existing_block_indices[idx]
            new_block_indices.append(copy.deepcopy(existing_block_index))

        return new_block_indices

    def find_next_tokens(
        self,
        logits: torch.Tensor,
        logit_target_locations: Optional[List[List[int]]],
        is_prefill: bool,
    ):
        next_tokens_scores: torch.Tensor
        if is_prefill:
            # outputs should be logits which would have shape of [batch, seq_len, embedding_dimension] # noqa
            # loop through each batch and find the logit location due to attention_packing
            next_tokens_scores = []
            for single_batch_logit, single_batch_logit_target_location in zip(
                logits, logit_target_locations
            ):
                assert single_batch_logit.dim() == 2
                for logit_target in single_batch_logit_target_location:
                    # logit target will just be index
                    next_tokens_scores.append(
                        single_batch_logit[logit_target]
                    )  # will be [embedding_dimension]

            # stack this back to [batch, vocab_size]
            next_tokens_scores = torch.stack(next_tokens_scores)

        else:
            next_tokens_scores = logits[:, 0, :]  # for decode seq_len would just be 1
        return next_tokens_scores

    # https://github.com/huggingface/transformers/blob/v4.31.0/src/transformers/generation/utils.py#L564-L568
    def adjust_logits_during_generation(
        self, logits: torch.FloatTensor, **kwargs
    ) -> torch.FloatTensor:
        """
        Implement in subclasses of [`PreTrainedModel`] for custom behavior to adjust the logits in \
            the generate method.
        """
        return logits


class MLPerfSubmissionGreedySearch(GreedySearch):
    pass


class MLPerfSubmissionBeamSearch(BeamSearch):
    @torch.no_grad()
    def decode(
        self,
        input_ids: torch.LongTensor,
        attention_mask: torch.Tensor,
        beam_scorer: BeamScorer,
        logits_processor: Optional[LogitsProcessorList] = None,
        stopping_criteria: Optional[StoppingCriteriaList] = None,
        max_length: Optional[int] = None,
        pad_token_id: Optional[int] = None,
        eos_token_id: Optional[Union[int, List[int]]] = None,
        return_dict_in_generate: Optional[bool] = None,
        **model_kwargs,
    ) -> Union[List[str], torch.Tensor]:
        """
        Generate N number of new tokens for each sequence
        where N = max_length - len(starting_input_ids[0])
        """
        kv_dtype = model_kwargs.get("kv_dtype")
        if kv_dtype is None:
            raise ValueError("`kv_dtype` is required for Paged Attention.")

        device = input_ids.device
        batch_size = input_ids.shape[0]
        bucket_size = model_kwargs.get("bucket_size") or max_length

        if bucket_size is None:
            raise ValueError("`bucket_size` is required for Paged Attention.")

        key_value_blocks = model_kwargs.get("key_value_blocks") or self.create_key_value_blocks(
            batch_size, bucket_size, kv_dtype, device
        )
        self.initialize_key_value_block_indices(key_value_blocks)
        # ----------- initial_settings -----------------
        starting_input_ids = input_ids
        starting_attention_mask = attention_mask
        batch_size, prompt_len = starting_input_ids.shape

        starting_position_ids = starting_attention_mask.long().cumsum(-1) - 1
        starting_position_ids.masked_fill_(starting_attention_mask == 0, 1)

        # ----------- adjust to bucket settings --------
        attention_mask = torch.zeros((batch_size, bucket_size), dtype=torch.int).to(device)
        attention_mask[:, :prompt_len] = starting_attention_mask

        input_ids = torch.full(
            (batch_size, bucket_size), fill_value=pad_token_id, dtype=torch.int
        ).to(device)
        input_ids[:, :prompt_len] = starting_input_ids

        position_ids = torch.zeros((batch_size, bucket_size), dtype=torch.long).to(device)
        position_ids[:, :prompt_len] = starting_position_ids

        if isinstance(eos_token_id, int):
            eos_token_id = [eos_token_id]

        if max_length is not None:
            logger.warning(
                "`max_length` is deprecated in this function, use "
                "`stopping_criteria=StoppingCriteriaList(MaxLengthCriteria(max_length=max_length))`\
                      instead."
            )
            stopping_criteria = validate_stopping_criteria(stopping_criteria, max_length)

        # beam search config
        batch_size = len(beam_scorer._beam_hyps)
        num_beams = beam_scorer.num_beams
        batch_beam_size, _ = input_ids.shape
        # TODO(this is because we use bucketization)
        cur_len = prompt_len

        # TODO(MAX BATCH CHECK ONLY EXISTS FOR THIS PYTHON GENERATOR)
        # In vllm, generate is async and inner scheduler decides which batch to use based on
        # memory allocation
        assert batch_size // num_beams <= self.max_batch_size

        if num_beams * batch_size != batch_beam_size:
            raise ValueError(
                f"Batch dimension of `input_ids` should be {num_beams * batch_size}, "
                f"but is {batch_beam_size}."
            )

        beam_scores = torch.zeros(
            (batch_size, num_beams), dtype=torch.float, device=input_ids.device
        )
        beam_scores[:, 1:] = -1e9
        beam_scores = beam_scores.view((batch_size * num_beams,))
        scores = None
        beam_indices = None

        is_prefill = True
        is_first_decode = False
        generated_ids = starting_input_ids
        next_input_ids = None
        count = 0

        # for MLPerf, we will soley use max_new_tokens = 128. This is why hardcoded.
        max_new_tokens = 128
        max_prompt_len = bucket_size - max_new_tokens

        while True:
            if is_prefill:
                (new_key_location, new_value_location) = self.prepare_prefill_input_metadata(
                    attention_mask, batch_size, num_beams, max_prompt_len
                )
                (
                    packed_input_ids,
                    _,
                    causal_mask,
                    packed_position_ids,
                    logit_target_locations,
                    new_key_location,
                    new_value_location,
                ) = self.prepare_prefill_inputs(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    new_key_location=new_key_location,
                    new_value_location=new_value_location,
                    pad_token_id=pad_token_id,
                )  # original attention mask, original position ids
                forward_kwargs = {
                    "input_ids": packed_input_ids.to(device),
                    "attention_mask": None,
                    "causal_mask": causal_mask.to(device),
                    "position_ids": packed_position_ids.to(device),
                    "past_key_values": key_value_blocks,
                    "new_key_location": new_key_location.to(device),
                    "new_value_location": new_value_location.to(device),
                    "past_valid_key_prompt_indices": None,
                    "past_valid_key_decode_indices": None,
                    "past_valid_value_prompt_indices": None,
                    "past_valid_value_decode_indices": None,
                    "is_prefill": is_prefill,
                    "bucket_size": bucket_size,
                    "use_cache": False,
                    "num_beam": num_beams,
                    "max_new_tokens": max_new_tokens,
                    "num_real_batch": batch_size,
                }

                is_first_decode = True
            else:
                (next_input_ids, attention_mask, position_ids) = self.prepare_decode_inputs(
                    next_input_ids=next_input_ids,
                    prev_attention_mask=attention_mask,
                    is_first_decode=is_first_decode,
                    seq_idx=max_prompt_len + count - 1,
                )

                logit_target_locations = None  # for decode, not needed

                (
                    new_key_location,
                    new_value_location,
                    past_valid_key_prompt_indices,
                    past_valid_key_decode_indices,
                    past_valid_value_prompt_indices,
                    past_valid_value_decode_indices,
                ) = self.prepare_decode_input_metadata(max_prompt_len=max_prompt_len)

                forward_kwargs = {
                    "input_ids": next_input_ids,
                    "attention_mask": attention_mask,
                    "causal_mask": None,
                    "position_ids": position_ids,
                    "past_key_values": key_value_blocks,
                    "new_key_location": new_key_location,
                    "new_value_location": new_value_location,
                    "past_valid_key_prompt_indices": past_valid_key_prompt_indices,
                    "past_valid_key_decode_indices": past_valid_key_decode_indices,
                    "past_valid_value_prompt_indices": past_valid_value_prompt_indices,
                    "past_valid_value_decode_indices": past_valid_value_decode_indices,
                    "is_prefill": is_prefill,
                    "bucket_size": bucket_size,
                    "use_cache": False,
                    "num_beam": num_beams,
                    "max_new_tokens": max_new_tokens,
                    "num_real_batch": batch_size,
                }

                is_first_decode = False

            outputs = self.model(**forward_kwargs)
            logits = handle_outputs(outputs)

            if is_prefill:
                next_token_logits = self.find_next_tokens(
                    logits, logit_target_locations, is_prefill
                )
                next_token_scores = torch.nn.functional.log_softmax(
                    next_token_logits, dim=-1
                )  # [batch_size * num_beams, vocab_size]
            else:
                # For decode, we will use the logits as scores as model outputs
                # torch.nn.functional.log_softmax(lm_logits[:, -1], dim=-1)
                next_token_scores = logits

            next_token_scores_processed = logits_processor(generated_ids, next_token_scores)

            next_token_scores = next_token_scores_processed + beam_scores[:, None].expand_as(
                next_token_scores
            )

            vocab_size = next_token_scores.shape[-1]
            next_token_scores = next_token_scores.view(batch_size, num_beams * vocab_size)

            next_token_scores, next_tokens = torch.topk(
                next_token_scores, 2 * num_beams, dim=1, largest=True, sorted=True
            )

            next_indices = torch.div(next_tokens, vocab_size, rounding_mode="floor")
            next_tokens = next_tokens % vocab_size

            beam_outputs = beam_scorer.process(
                generated_ids,
                next_token_scores,
                next_tokens,
                next_indices,
                pad_token_id=pad_token_id,
                eos_token_id=eos_token_id,
                beam_indices=beam_indices,
            )

            beam_scores = beam_outputs["next_beam_scores"]
            beam_next_tokens = beam_outputs["next_beam_tokens"]
            beam_idx = beam_outputs["next_beam_indices"]

            generated_ids = torch.cat(
                [generated_ids[beam_idx, :], beam_next_tokens.unsqueeze(-1)], dim=-1
            )

            if not is_prefill:
                # now copy the new_key location back to original place for decode_phase
                self.move_kv_cache_block_in_place(
                    seq_idx=max_prompt_len + count - 1,
                    new_location=new_key_location,
                    existing_block_indices=self.active_key_block_indices,
                )
                self.move_kv_cache_block_in_place(
                    seq_idx=max_prompt_len + count - 1,
                    new_location=new_value_location,
                    existing_block_indices=self.active_value_block_indices,
                )
            # TODO(DONGHUN) based on this idx adjust the block index
            # we know new beams are chosen at this point
            new_key_block_indices = self.adjust_kv_cache_block(
                beam_idx, self.active_key_block_indices
            )
            self.active_key_block_indices = new_key_block_indices
            new_value_block_indices = self.adjust_kv_cache_block(
                beam_idx, self.active_value_block_indices
            )
            self.active_value_block_indices = new_value_block_indices

            cur_len = cur_len + 1
            count += 1

            if beam_scorer.is_done or stopping_criteria(generated_ids, scores):
                break

            # v2.Generator specific variables
            is_prefill = False
            next_input_ids = beam_next_tokens

        sequence_outputs = beam_scorer.finalize(
            generated_ids,
            beam_scores,
            next_tokens,
            next_indices,
            pad_token_id=pad_token_id,
            eos_token_id=eos_token_id,
            max_length=max_length,
            beam_indices=beam_indices,
        )

        # reset must be called for paged attention to call generate again
        self.reset()

        if return_dict_in_generate:
            return BeamSearchDecoderOnlyOutput(
                sequences=sequence_outputs["sequences"],
                sequences_scores=sequence_outputs["sequence_scores"],
                scores=scores,
                beam_indices=sequence_outputs["beam_indices"],
            )
        else:
            return sequence_outputs["sequences"]

    def prepare_prefill_input_metadata(
        self,
        attention_mask: torch.Tensor,
        batch_size: int,
        num_beams: int,
        max_prompt_len: int,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        for prefill, valid_key_indices and valid_value_indices are none
        return (new_key_location, new_value_location)
        """
        # beams belonging to same prompts should share blocks

        new_key_location = []  # shape = (batch, bucket_size)
        new_value_location = []  # shape = (batch, bucket_size)
        for count in range(batch_size):
            idx = count * num_beams
            single_attention_mask = attention_mask[idx]
            block_indices = []
            for val in single_attention_mask:
                if val == 0:
                    # padding
                    block_indices.append(self.zero_block_index)
                else:
                    block_indices.append(self.available_block_indices.pop())

            # at this point block has been created
            # MAX_PROMPT_LEN is required to remove dynamic characteristc to decode phase
            self.prompt_key_block_indices.append(copy.deepcopy(block_indices[:max_prompt_len]))
            self.prompt_value_block_indices.append(copy.deepcopy(block_indices[:max_prompt_len]))

            for _ in range(num_beams):
                self.active_key_block_indices.append(copy.deepcopy(block_indices))
                self.active_value_block_indices.append(copy.deepcopy(block_indices))

        new_key_location = torch.IntTensor(self.active_key_block_indices)
        new_value_location = torch.IntTensor(self.active_value_block_indices)

        return (
            new_key_location,
            new_value_location,
        )

    def prepare_decode_input_metadata(
        self, max_prompt_len: int
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        return (new_key_location, new_value_location, valid_key_indices, valid_valie_indices)
        """
        new_key_location = []  # shape = (batch, 1)
        new_value_location = []  # shape = (batch, 1)
        past_valid_key_decode_indices = []
        past_valid_value_decode_indices = []

        for key_batch, value_batch in zip(
            self.active_key_block_indices, self.active_value_block_indices
        ):
            past_valid_key_decode_indices.extend(key_batch[max_prompt_len:-1])
            past_valid_value_decode_indices.extend(value_batch[max_prompt_len:-1])

            # we use same block idx for key and value here
            new_block_idx = self.available_block_indices.pop()

            key_batch[-1] = new_block_idx
            value_batch[-1] = new_block_idx

            new_key_location.append([new_block_idx])
            new_value_location.append([new_block_idx])

        new_key_location = torch.IntTensor(new_key_location)
        new_value_location = torch.IntTensor(new_value_location)

        past_valid_key_prompt_indices = torch.IntTensor(self.prompt_key_block_indices)
        past_valid_value_prompt_indices = torch.IntTensor(self.prompt_value_block_indices)
        past_valid_key_decode_indices = torch.IntTensor(past_valid_key_decode_indices)
        past_valid_value_decode_indices = torch.IntTensor(past_valid_value_decode_indices)

        return (
            new_key_location,
            new_value_location,
            past_valid_key_prompt_indices,
            past_valid_key_decode_indices,
            past_valid_value_prompt_indices,
            past_valid_value_decode_indices,
        )


def handle_outputs(
    outputs: Tuple[torch.Tensor, List[Tuple[torch.Tensor, torch.Tensor]]],
) -> torch.Tensor:
    # handle outputs differently based on prefill vs decode

    # SUPPORTED_GENERATION_RETURN_DICT_TYPES[1],
    # i.e., CausalLMOutputWithCrossAttentions is not yet checked.
    if isinstance(outputs, SUPPORTED_GENERATION_RETURN_DICT_TYPES[0]):
        logits = outputs.to_tuple()[0]
    elif isinstance(outputs, Tuple):
        logits = outputs[0]
    elif isinstance(outputs, Dict):
        logits = outputs["logits"]
    else:
        raise ValueError(f"Unsupported generation output type: {type(outputs)}")
    return logits
