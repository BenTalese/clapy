from abc import ABC, abstractmethod
from typing import List, Type

from .outputs import IOutputPort
from .pipeline import IPipe, InputPort, PipeConfiguration

__all__ = ["IPipelineFactory", "IServiceProvider", "IUseCaseInvoker"]


class IPipelineFactory(ABC):
    '''Responsible for creating the pipeline for the use case invoker to execute.'''

    @abstractmethod
    async def create_pipeline_async(
            self,
            input_port: InputPort,
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
    def get_service(self, service: type) -> object:
        '''
        Summary
        -------
        Retrieves the specified service from the dependency_injection container.

        Parameters
        ----------
        `service` The service to be retrieved.

        Returns
        -------
        An instance of the requested service type with a lifetime as defined on the container.

        '''
        pass


class IUseCaseInvoker(ABC):
    '''The main engine of Clapy. Handles the invocation of use case pipelines.'''

    @abstractmethod
    async def invoke_usecase_async(
            self,
            input_port: InputPort,
            output_port: IOutputPort,
            pipeline_configuration: List[PipeConfiguration]) -> bool:
        '''
        Summary
        -------
        Performs the invocation of a use case with the provided input and output ports. Will stop
        the pipeline if the pipeline's pipes are exhausted, or on pipe failure unless configured to ignore.

        Parameters
        ----------
        `input_port` The input port of the use case to be invoked\n
        `output_port` The output port of the use case to be invoked\n
        `pipeline_configuration` The configuration used to determine priority and inclusion of
        use case pipes.

        Returns
        -------
        True if pipes exhausted and no pipe failures occurred. Does not check failure override from
        pipe configurations.

        '''
        pass
