from abc import ABC, abstractmethod

from outputs import IValidationOutputPort


class IGreetOutputPort(IValidationOutputPort, ABC):

    @abstractmethod
    async def present_greeting_async(self, greeting: str) -> None: #TODO: None, or Coroutine?
        pass
