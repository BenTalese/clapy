import os
import sys

sys.path.append(os.getcwd())

import asyncio

from dependency_injector import providers

from sample.interface_adaptors.conversation_controller import \
    ConversationController
from sample.interface_adaptors.greet_presenter import GreetPresenter
from sample.pipeline.pipeline_configuration import PipelineConfiguration
from sample.use_cases.greet.greet_input_port import GreetInputPort
from src.clapy.dependency_injection import DependencyInjectorServiceProvider
from src.clapy.pipeline import RequiredInputValidator


async def main():
    _ServiceProvider = DependencyInjectorServiceProvider()

    _UsecaseScanLocations = ["sample/use_cases"]

    _ServiceProvider.register_pipe_services(_UsecaseScanLocations, [r"venv", r"src"], [r".*main\.py"])
    _ServiceProvider.construct_usecase_invoker(_UsecaseScanLocations)

    _ServiceProvider.register_service(providers.Factory, RequiredInputValidator) #TODO: hmm....this isn't great

    _ServiceProvider.register_service(providers.Factory, ConversationController)

    _Controller: ConversationController = _ServiceProvider.get_service(ConversationController)

    _InputPort = GreetInputPort()
    _InputPort.name = "Ben Ben"

    await _Controller.greet_async(_InputPort, GreetPresenter(), PipelineConfiguration.DefaultConfiguration.value)

if __name__ == "__main__":
    asyncio.run(main())
