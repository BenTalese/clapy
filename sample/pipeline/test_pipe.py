from typing import Any, Coroutine, Generic, Union
from src.clapy.generics import TInputPort, TOutputPort
from src.clapy.pipeline import IPipe


'''
TODO:
Update docs everywhere
Look into doctest
Update readme
Either learn how to use github workflow, or remove it
Unit tests
Demo doing "can invoke use case"
Demo doing bulk actions (so cut out unnecessary steps)
Set version numbers to 2.0.0
Change from beta to production in toml
Test package locally
Test package by publishing to testpypi, then try and use it somewhere outside this repo

Publish!
'''


class TestPipe(IPipe, Generic[TInputPort, TOutputPort]):

    async def execute_async(self, input_port: Any, output_port: Any) -> Coroutine[Any, Any, Union[Coroutine, None]]:
        print("blah")
