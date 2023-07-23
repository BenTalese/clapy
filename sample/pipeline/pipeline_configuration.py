from enum import Enum

from sample.pipeline.name_checker import NameChecker
from src.clapy.pipeline import (InputPortValidator, Interactor,
                                PipeConfiguration, PipeConfigurationOption,
                                RequiredInputValidator)


class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        PipeConfiguration(RequiredInputValidator, PipeConfigurationOption.INSERT),
        PipeConfiguration(InputPortValidator),
        PipeConfiguration(NameChecker),
        PipeConfiguration(Interactor)
    ]
