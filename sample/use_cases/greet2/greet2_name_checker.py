from sample.pipeline.name_checker import NameChecker
from sample.use_cases.greet2.greet2_input_port import Greet2InputPort
from sample.use_cases.greet2.igreet2_output_port import IGreet2OutputPort
from src.clapy.outputs import ValidationResult


class Greet2NameChecker(NameChecker):

    async def execute_async(self, input_port: Greet2InputPort, output_port: IGreet2OutputPort) -> None:
        if len(input_port.name) > 20:
            await output_port.present_validation_failure_async(
                ValidationResult.from_error(input_port, 'name', "Your name is too long for me to say... 😔"))
            self.has_failures = True

        elif len(input_port.name.split(" ")) < 2:
            self.has_failures = not await output_port.present_missing_names_warning_async()

        else:
            print("That's a nice name! 😊")
