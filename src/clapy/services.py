from abc import ABC, abstractmethod
from typing import List, Type

from .generics import TInputPort, TOutputPort, TServiceType
from .pipeline import IPipe, PipeConfiguration


class IPipelineFactory(ABC):
    '''Responsible for creating the pipeline for the use case invoker to execute.'''

    @abstractmethod
    async def create_pipeline_async(
            self,
            input_port: TInputPort,
            pipeline_configuration: List[PipeConfiguration]) -> List[Type[IPipe]]:
        '''
        Summary
        -------
        Creates a sorted list of IPipe objects based on the use case input port and pipeline
        configuration provided.

        Parameters
        ----------
        `input_port` The input port of the use case to construct the pipeline for\n
        `pipeline_configuration` The configuration used to determine order and inclusion of pipes

        Returns
        -------
        The pipeline consisting of the use case pipes ordered by their priority.

        '''
        pass


class IServiceProvider(ABC):
    '''A generic interface for getting services from a dependency injection container.'''

    @abstractmethod
    def get_service(self, service: Type[TServiceType]) -> TServiceType:
        '''
        Summary
        -------
        Retrieves the specified service from the dependency_injectior container.

        Parameters
        ----------
        `service` The service to be retrieved.

        Returns
        -------
        An instance of the requested service type with a lifetime as defined on the container.

        '''
        pass


class IUseCaseInvoker(ABC):
    '''The main engine of Clapy. Handles the invocation of use case pipelines and the execution of resulting actions.'''

    @abstractmethod
    async def invoke_usecase_async(
            self,
            input_port: TInputPort,
            output_port: TOutputPort,
            pipeline_configuration: List[Type[IPipe]]) -> None:
        '''
        Summary
        -------
        Performs the invocation of a use case with the provided input and output ports. Will stop
        invocation on receival of a coroutine result, or if the pipeline's pipes are exhausted.

        Parameters
        ----------
        `input_port` The input port of the use case to be invoked\n
        `output_port` The output port of the use case to be invoked\n
        `pipeline_configuration` The configuration used to determine priority and inclusion of
        use case pipes

        '''
        pass
