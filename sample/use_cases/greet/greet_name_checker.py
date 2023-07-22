from typing import Any, Coroutine, Union
from outputs import ValidationResult

from sample.pipeline.name_checker import NameChecker
from sample.use_cases.greet.greet_input_port import GreetInputPort
from sample.use_cases.greet.igreet_output_port import IGreetOutputPort


class GreetNameChecker(NameChecker):

    async def execute_async(self, input_port: GreetInputPort, output_port: IGreetOutputPort) -> None:
        if len(input_port.name) > 20:
            await output_port.present_validation_failure_async(
                ValidationResult.from_error(input_port.name, "Your name is too long for me to say... 😔"))
            self.has_failures = True

        elif len(input_port.name.split(" ")) < 2:
            self.has_failures = not await output_port.present_missing_names_warning_async()

        else:
            print("That's a nice name! 😊")
