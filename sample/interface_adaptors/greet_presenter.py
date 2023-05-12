from typing import Any, Coroutine

from sample.use_cases.greet.igreet_output_port import IGreetOutputPort


class GreetPresenter(IGreetOutputPort):

    async def present_greeting_async(self, greeting: str) -> Coroutine[Any, Any, None]:
        return print(greeting)
    
    async def present_validation_failure_async(self, validation_failure: Any) -> Coroutine[Any, Any, None]:
        return print(validation_failure)
