from enum import Enum

from sample.pipeline.name_checker import NameChecker
from sample.pipeline.utils import report_time
from src.clapy.pipeline import (InputPortValidator, Interactor,
                                PipeConfiguration, PipeConfigurationOption,
                                RequiredInputValidator)


class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        PipeConfiguration(RequiredInputValidator,
                          PipeConfigurationOption.INSERT,
                          pre_action=report_time("Start time is: ")),
        PipeConfiguration(InputPortValidator),
        PipeConfiguration(NameChecker),
        PipeConfiguration(Interactor, post_action=report_time("Finish time is: "))
    ]
