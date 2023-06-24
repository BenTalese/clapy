from enum import Enum
from src.clapy.pipeline import InputPortValidator, Interactor, PipeConfiguration, PipeConfigurationOption
from sample.pipeline.name_checker import NameChecker
from sample.pipeline.test_pipe import TestPipe


class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        PipeConfiguration(NameChecker, PipeConfigurationOption.DEFAULT),
        PipeConfiguration(Interactor, PipeConfigurationOption.DEFAULT)
    ]

    OtherConfiguration = [
        PipeConfiguration(NameChecker, PipeConfigurationOption.DEFAULT),
        PipeConfiguration(TestPipe, PipeConfigurationOption.INSERT),
        PipeConfiguration(InputPortValidator, PipeConfigurationOption.DEFAULT),
        PipeConfiguration(TestPipe, PipeConfigurationOption.INSERT),
        PipeConfiguration(Interactor, PipeConfigurationOption.DEFAULT),
        PipeConfiguration(TestPipe, PipeConfigurationOption.INSERT)
    ]
