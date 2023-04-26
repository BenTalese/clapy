from abc import ABC, abstractmethod
from typing import List, Type

from generics import TInputPort, TOutputPort, TServiceType
from pipeline import IPipe


class IPipelineFactory(ABC):

    @abstractmethod
    def create_pipeline(self, input_port: TInputPort) -> List[Type[IPipe]]:
        pass


class IServiceProvider(ABC):

    @abstractmethod
    def get_service(self, service: Type[TServiceType]) -> TServiceType:
        pass


class IUseCaseInvoker(ABC):

    @abstractmethod
    async def can_invoke_usecase_async(self, input_port: TInputPort, output_port: TOutputPort) -> bool:
        pass

    @abstractmethod
    async def invoke_usecase_async(self, input_port: TInputPort, output_port: TOutputPort) -> None:
        pass
