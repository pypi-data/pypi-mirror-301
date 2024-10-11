import logging
from typing import Optional

from transformers import PreTrainedModel
from transformers.generation.configuration_utils import GenerationConfig

from ..base import GeneratorForDecoderOnlyModels
from .generation_strategy import (
    BeamSearch,
    GreedySearch,
    MLPerfSubmissionBeamSearch,
    MLPerfSubmissionGreedySearch,
)

USE_CACHE = False
logger = logging.getLogger(__name__)


class Generator(GeneratorForDecoderOnlyModels):
    block_size = 1
    max_batch_size = 4

    def __init__(
        self, model: PreTrainedModel, generation_config_helper: Optional[GenerationConfig] = None
    ):
        super().__init__(model, generation_config_helper, logger)
        self.logger = logger
        self._greedy_search = GreedySearch(model)
        self._beam_search = BeamSearch(model)


class MLPerfSubmissionGenerator(GeneratorForDecoderOnlyModels):
    block_size = 1
    max_batch_size = 4

    def __init__(
        self, model: PreTrainedModel, generation_config_helper: Optional[GenerationConfig] = None
    ):
        super().__init__(model, generation_config_helper, logger)
        self.logger = logger
        self._greedy_search = MLPerfSubmissionGreedySearch(model)
        self._beam_search = MLPerfSubmissionBeamSearch(model)
