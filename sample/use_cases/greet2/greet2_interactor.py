from sample.use_cases.greet2.greet2_input_port import Greet2InputPort
from sample.use_cases.greet2.igreet2_output_port import IGreet2OutputPort
from src.clapy.pipeline import Interactor


class Greet2Interactor(Interactor):

    async def execute_async(self, input_port: Greet2InputPort, output_port: IGreet2OutputPort) -> None:
        await output_port.present_greeting_async(f"Hello {input_port.name}!")
