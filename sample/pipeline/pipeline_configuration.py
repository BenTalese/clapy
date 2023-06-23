from enum import Enum
from src.clapy.pipeline import InputPortValidator, Interactor, PipeConfigurationOption
from sample.pipeline.name_checker import NameChecker
from sample.pipeline.test_pipe import TestPipe


class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        (NameChecker, PipeConfigurationOption.DEFAULT),
        (Interactor, PipeConfigurationOption.DEFAULT)
    ]

    OtherConfiguration = [
        (NameChecker, PipeConfigurationOption.DEFAULT),
        (InputPortValidator, PipeConfigurationOption.DEFAULT),
        (TestPipe, PipeConfigurationOption.INSERT),
        (Interactor, PipeConfigurationOption.DEFAULT)
    ]
