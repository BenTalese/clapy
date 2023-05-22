from enum import Enum
from pipeline import Interactor
from sample.pipeline.name_checker import NameChecker
from sample.pipeline.test_pipe import TestPipe


class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        NameChecker,
        TestPipe,
        Interactor
    ]
