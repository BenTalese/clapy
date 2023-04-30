import asyncio
import os
from typing import Dict, List, Optional, Type

from common import (DIR_EXCLUSIONS, FILE_EXCLUSIONS, apply_exclusion_filter,
                    import_class_by_namespace)
from generics import TInputPort, TOutputPort
from pipeline import IInteractor, IPipe, PipePriority
from services import IPipelineFactory, IServiceProvider, IUseCaseInvoker


class PipelineFactory(IPipelineFactory):
    '''Responsible for creating the pipeline for the use case invoker to execute.'''

    def __init__(self, service_provider: IServiceProvider, usecase_registry: Dict[str, List[Type[IPipe]]]):
        self._service_provider = service_provider if service_provider is not None else ValueError(f"'{service_provider=}' cannot be None.")
        self._usecase_registry = usecase_registry if usecase_registry is not None else ValueError(f"'{usecase_registry=}' cannot be None.")


    async def create_pipeline_async(self, input_port: TInputPort) -> List[Type[IPipe]]:
        '''
        Summary
        -------
        Creates a list of IPipe objects, sorted by priority, for a use case based on the input port provided.
        
        Parameters
        ----------
        `input_port` The input port of the use case to construct the pipeline for
        
        Exceptions
        ----------
        Raises a `KeyError` if the provided `input_port` does not match any registered use case.

        Returns
        -------
        The pipeline consisting of the use case pipes ordered by their priority.
        
        '''
        _UsecaseKey = input_port.__module__.rsplit(".", 1)[0]

        if _UsecaseKey not in self._usecase_registry:
            raise KeyError(f"Could not find '{input_port}' in the pipeline registry.")
        
        _PipeNamespaces = self._usecase_registry[_UsecaseKey]

        _PipeClasses = [import_class_by_namespace(_Namespace) for _Namespace in _PipeNamespaces]

        _Pipes: List[IPipe] = [self._service_provider.get_service(_PipeClass) for _PipeClass in _PipeClasses]
        
        return sorted(_Pipes, key=lambda _Pipe: _Pipe.priority)


class UseCaseInvoker(IUseCaseInvoker):
    '''The main engine of Clapy. Handles the invocation of use case pipelines and the execution of resulting actions.'''

    def __init__(self, pipeline_factory: IPipelineFactory):
        self._pipeline_factory = pipeline_factory if pipeline_factory is not None else ValueError(f"'{pipeline_factory=}' cannot be None.")


    async def can_invoke_usecase_async(self, input_port: TInputPort, output_port: TOutputPort) -> bool:
        '''
        Summary
        -------
        Checks if a use case can be successfully invoked based on provided input and output ports,
        without performing the interactor execution. Useful for situations such as proactively disabling
        a UI button based on whether or not a use case's interactor can be successfully invoked.
        
        Parameters
        ----------
        `input_port` The input port of the use case to be invoked\n
        `output_port` The output port of the use case to be invoked
        
        Returns
        -------
        `True` if all pipes were successfully invoked without error responses and the interactor was reached, otherwise `false`.
        
        '''
        _Pipeline = await self._pipeline_factory.create_pipeline_async(input_port)

        _PipelineResult = None
        while _PipelineResult is None and len(_Pipeline) > 0:

            _Pipe = _Pipeline.pop(0)

            if not isinstance(_Pipe, IInteractor):
                _PipelineResult = await _Pipe.execute_async(input_port, output_port)
                
                if asyncio.iscoroutine(_PipelineResult):
                    await _PipelineResult

            if _PipelineResult is not None:
                return False
            
        return True


    async def invoke_usecase_async(self, input_port: TInputPort, output_port: TOutputPort) -> None:
        '''
        Summary
        -------
        Performs the invocation of a use case with the provided input and output ports. Will stop
        invocation on receival of a coroutine result, or if the pipeline's pipes are exhausted.
        
        Parameters
        ----------
        `input_port` The input port of the use case to be invoked\n
        `output_port` The output port of the use case to be invoked
        
        '''
        _Pipeline = await self._pipeline_factory.create_pipeline_async(input_port)

        _PipelineResult = None
        while _PipelineResult is None and len(_Pipeline) > 0:

            _Pipe = _Pipeline.pop(0)
            
            _PipelineResult = await _Pipe.execute_async(input_port, output_port)

            if asyncio.iscoroutine(_PipelineResult):
                await _PipelineResult
            

@staticmethod
def construct_usecase_registry(
    usecase_locations: Optional[List[str]] = ["."],
    directory_exclusion_patterns: Optional[List[str]] = [],
    file_exclusion_patterns: Optional[List[str]] = []) -> Dict[str, List[str]]:
    '''
    Summary
    -------
    Scans the provided project location, or entire project if no location provided, for use
    cases and builds a dictonary of use cases and the associated use case's pipes by their namespace.
    
    Parameters
    ----------
    `usecase_scan_locations` An optional list of locations within the project where the usecase services
    should be scanned for.\n
    `directory_exclusion_patterns` An optional list of regular expression patterns used to exclude directories
    from being scanned.\n
    `file_exclusion_patterns`An optional list of regular expression patterns used to exclude files
    from being scanned and registered.
    
    Returns
    -------
    A dictionary with the key being the namespace of the use case folder, and value being a list of use case
    pipes found under that use case folder.
    
    '''
    directory_exclusion_patterns = directory_exclusion_patterns + DIR_EXCLUSIONS
    file_exclusion_patterns = file_exclusion_patterns + FILE_EXCLUSIONS

    _UsecaseRegistry = {}

    for _Location in usecase_locations:
        for _Root, _Directories, _Files in os.walk(_Location):

            apply_exclusion_filter(_Directories, directory_exclusion_patterns)
            apply_exclusion_filter(_Files, file_exclusion_patterns)

            _DirectoryNamespace = _Root.replace('/', '.')
            _Pipes = []

            for _File in _Files:
                _Namespace = _DirectoryNamespace + "." + _File[:-3]
                _Class = import_class_by_namespace(_Namespace)

                if issubclass(_Class, IPipe):
                    _Pipes.append(_Namespace)

            if _Pipes:
                _UsecaseRegistry[_DirectoryNamespace] = { _Pipes }

    return _UsecaseRegistry


@staticmethod
def set_pipe_priority(priorities: Dict[str, int]) -> None:
    '''
    Summary
    -------
    Sets the priority for use case pipes as attributes on the PipePriority class
    based on the provided priorities.
    
    Parameters
    ----------
    `priorities` A dictionary of pipe names and their priority number.
    
    '''
    for key, value in priorities.items():
        setattr(PipePriority, key, value)
