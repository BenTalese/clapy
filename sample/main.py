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

    # Setup:
    _ServiceProvider = DependencyInjectorServiceProvider()
    _UsecaseScanLocations = ["sample/use_cases"]
    _ServiceProvider.configure_clapy_services(_UsecaseScanLocations, [r"venv", r"src"], [r".*main\.py"])

    _ServiceProvider.register_service(providers.Factory, RequiredInputValidator)
    _ServiceProvider.register_service(providers.Factory, ConversationController)

    _Controller: ConversationController = _ServiceProvider.get_service(ConversationController)

    # Example of simple default use case invocation:
    _InputPort1 = GreetInputPort()
    _InputPort1.name = "Ben Ben"
    await _Controller.greet_async(_InputPort1, GreetPresenter(), PipelineConfiguration.DefaultConfiguration.value)

    # Example of bulk operation using less pipes to be efficient:
    _Names = ["Bill", "Bob" ,"Ben", "Bud"]
    _GreetingTasks = []
    for _Name in _Names:
        _InputPort2 = GreetInputPort()
        _InputPort2.name = _Name
        _GreetingTasks.append(_Controller.greet_async(_InputPort2, GreetPresenter(), PipelineConfiguration.BulkGreetConfiguration.value))

    await asyncio.gather(*_GreetingTasks)

    # Example of proactively checking for use case success and providing UI feedback:
    _InputPort3 = GreetInputPort()
    _CanInvokeUsecase = await _Controller.greet_async(_InputPort3, GreetPresenter(), PipelineConfiguration.ValidationOnlyConfiguration.value)
    if not _CanInvokeUsecase:
        print("You can provide UI feedback based on this result!")

if __name__ == "__main__":
    asyncio.run(main())
