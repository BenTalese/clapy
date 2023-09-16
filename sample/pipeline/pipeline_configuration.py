from enum import Enum

from sample.pipeline.name_checker import NameChecker
from sample.pipeline.utils import report_time
from src.clapy.pipeline import (InputPortValidator, InputTypeValidator, Interactor,
                                PipeConfiguration, PipeConfigurationOption,
                                RequiredInputValidator)


class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        PipeConfiguration(RequiredInputValidator,
                          PipeConfigurationOption.INSERT,
                          True,
                          report_time("Start time is: ")),
        PipeConfiguration(InputTypeValidator, PipeConfigurationOption.INSERT),
        PipeConfiguration(InputPortValidator),
        PipeConfiguration(NameChecker),
        PipeConfiguration(Interactor, post_action=report_time("Finish time is: "))
    ]

    BulkGreetConfiguration = [
        PipeConfiguration(RequiredInputValidator, PipeConfigurationOption.INSERT),
        PipeConfiguration(Interactor)
    ]

    ValidationOnlyConfiguration = [
        PipeConfiguration(RequiredInputValidator, PipeConfigurationOption.INSERT),
        PipeConfiguration(InputPortValidator),
        PipeConfiguration(NameChecker)
    ]
