import os
import sys
import time


sys.path.append(os.getcwd())

import asyncio

from dependency_injector import providers

from sample.interface_adaptors.conversation_controller import \
    ConversationController
from sample.pipeline.test_pipe import TestPipe
from sample.interface_adaptors.greet_presenter import GreetPresenter
from sample.pipeline.pipeline_configuration import PipelineConfiguration
from sample.use_cases.greet.greet_input_port import GreetInputPort
from src.clapy.dependency_injection import DependencyInjectorServiceProvider


async def main():
    _ServiceProvider = DependencyInjectorServiceProvider()

    _UsecaseScanLocations = ["sample/use_cases"]

    _ServiceProvider.register_pipe_services(_UsecaseScanLocations, [r"venv", r"src"], [r".*main\.py"])
    _ServiceProvider.construct_usecase_invoker(_UsecaseScanLocations)

    _ServiceProvider.register_service(providers.Factory, ConversationController)
    _ServiceProvider.register_service(providers.Factory, TestPipe)

    _Controller = _ServiceProvider.get_service(ConversationController)

    await _Controller.greet_async(GreetInputPort("Ben"), GreetPresenter(), PipelineConfiguration.OtherConfiguration.value)

if __name__ == "__main__":
    asyncio.run(main())
