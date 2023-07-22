from abc import ABC, abstractmethod

from src.clapy.outputs import IOutputPort, IValidationOutputPort


class IGreetOutputPort(IOutputPort, IValidationOutputPort, ABC):

    @abstractmethod
    async def present_greeting_async(self, greeting: str) -> None:
        pass

    @abstractmethod
    async def present_missing_names_warning_async(self) -> bool:
        pass
