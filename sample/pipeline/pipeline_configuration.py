from enum import Enum
from src.clapy.pipeline import InputPortValidator, Interactor, PipeConfiguration, PipeConfigurationOption, RequiredInputValidator
from sample.pipeline.name_checker import NameChecker


class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        PipeConfiguration(RequiredInputValidator, PipeConfigurationOption.INSERT),
        PipeConfiguration(InputPortValidator),
        PipeConfiguration(NameChecker),
        PipeConfiguration(Interactor)
    ]
