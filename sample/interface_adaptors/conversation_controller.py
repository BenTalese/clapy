from typing import List, Type

from sample.use_cases.greet.greet_input_port import GreetInputPort
from sample.use_cases.greet.igreet_output_port import IGreetOutputPort
from src.clapy.pipeline import IPipe
from src.clapy.services import IUseCaseInvoker


class ConversationController:

    def __init__(self, use_case_invoker: IUseCaseInvoker):
        self._use_case_invoker = use_case_invoker

    async def greet_async(self, input_port: GreetInputPort, output_port: IGreetOutputPort, pipeline_configuration: List[Type[IPipe]]):
        await self._use_case_invoker.invoke_usecase_async(input_port, output_port, pipeline_configuration)
