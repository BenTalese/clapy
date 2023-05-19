from typing import Any, Coroutine, Union

from sample.pipeline.name_checker import NameChecker
from sample.use_cases.greet.greet_input_port import GreetInputPort
from sample.use_cases.greet.igreet_output_port import IGreetOutputPort


class GreetNameChecker(NameChecker):

    async def execute_async(
            self,
            input_port: GreetInputPort,
            output_port: IGreetOutputPort) -> Coroutine[GreetInputPort, Any, Union[Coroutine, None]]:
        if len(input_port.name) > 10:
            return output_port.present_validation_failure_async("Your name is too long for me to say... 😔")

        print("That's a nice name! 😊")
