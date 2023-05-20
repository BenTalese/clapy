import os
import sys
sys.path.append(os.getcwd())

import asyncio

from dependency_injector import providers

from sample.interface_adaptors.conversation_controller import \
    ConversationController
from sample.interface_adaptors.greet_presenter import GreetPresenter
from sample.pipeline.name_checker import NameChecker
from sample.pipeline.test_pipe import TestPipe
from sample.use_cases.greet.greet_input_port import GreetInputPort
from src.clapy.dependency_injection import DependencyInjectorServiceProvider
from src.clapy.pipeline import Interactor


async def main():
    _ServiceProvider = DependencyInjectorServiceProvider()

    # TODO: Let user know it starts scanning from top of project, also put in docs
    _UsecaseScanLocations = ["sample/use_cases"]

    # TODO: Still feels retarded that the user can get clapy to scan absolutely everywhere
    _ServiceProvider.register_usecase_services(_UsecaseScanLocations, [r"venv", r"src"], [r".*main\.py"])
    _ServiceProvider.construct_usecase_invoker(_UsecaseScanLocations)

    _ServiceProvider.register_service(providers.Factory, ConversationController)

    _Controller = _ServiceProvider.get_service(ConversationController)

    await _Controller.greet_async(GreetInputPort("Ben"), GreetPresenter(), [NameChecker, TestPipe, Interactor])

if __name__ == "__main__":
    asyncio.run(main())
