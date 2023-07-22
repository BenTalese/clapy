from sample.use_cases.greet.greet_input_port import GreetInputPort
from sample.use_cases.greet.igreet_output_port import IGreetOutputPort
from src.clapy.pipeline import Interactor


class GreetInteractor(Interactor):

    async def execute_async(self, input_port: GreetInputPort, output_port: IGreetOutputPort) -> None:
        await output_port.present_greeting_async(f"Hello {input_port.name}!")
