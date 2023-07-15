import asyncio
import importlib
import inspect
import os
from typing import Dict, List, Optional, Type

from .common import DIR_EXCLUSIONS, FILE_EXCLUSIONS, Common
from .exceptions import PipeConfigurationError
from .generics import TInputPort, TOutputPort
from .pipeline import IPipe, InputPort, PipeConfiguration, PipeConfigurationOption
from .services import IPipelineFactory, IServiceProvider, IUseCaseInvoker


class PipelineFactory(IPipelineFactory):
    '''Responsible for creating the pipeline for the use case invoker to execute.'''

    def __init__(self, service_provider: IServiceProvider, usecase_registry: Dict[str, List[Type[IPipe]]]):
        self._service_provider = service_provider or ValueError("service_provider cannot be None.")
        self._usecase_registry = usecase_registry or ValueError("usecase_registry cannot be None.")

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

        Exceptions
        ----------
        Raises a `KeyError` if the provided `input_port` does not match any registered use case.

        Returns
        -------
        The pipeline consisting of the use case pipes ordered by their priority.

        '''
        _UsecaseKey = input_port.__module__

        if _UsecaseKey not in self._usecase_registry:
            raise KeyError(f"Could not find '{input_port}' in the pipeline registry.")

        _PipeServices = [self._service_provider.get_service(Common.import_class_by_namespace(_Namespace))
                         for _Namespace in self._usecase_registry[_UsecaseKey]]

        _FilteredPipes = [_Pipe for _Pipe in _PipeServices
                          if any(issubclass(type(_Pipe), _PipeConfig.type)
                                 for _PipeConfig in pipeline_configuration
                                 if _PipeConfig.option == PipeConfigurationOption.DEFAULT)]

        _SortedPipes = sorted(_FilteredPipes, key=lambda _Pipe:
                              pipeline_configuration.index(next(_PipeConfig
                                                                for _PipeConfig in pipeline_configuration
                                                                if issubclass(type(_Pipe), _PipeConfig.type))))

        _PipesToInsert = [(self._service_provider.get_service(_ExtraPipe.type), _Index)
                          for _Index, _ExtraPipe in enumerate(pipeline_configuration)
                          if not any(issubclass(type(_Pipe), _ExtraPipe.type) for _Pipe in _PipeServices)
                          and _ExtraPipe.option == PipeConfigurationOption.INSERT]

        for _PipeService, _Priority in _PipesToInsert:
            Engine._insert_pipe(_PipeService, _Priority, _SortedPipes, pipeline_configuration)

        return _SortedPipes


class UseCaseInvoker(IUseCaseInvoker):
    '''The main engine of Clapy. Handles the invocation of use case pipelines and the execution of resulting actions.'''

    def __init__(self, pipeline_factory: IPipelineFactory):
        self._pipeline_factory = pipeline_factory or ValueError("pipeline_factory cannot be None.")

    async def invoke_usecase_async(
            self,
            input_port: TInputPort,
            output_port: TOutputPort,
            pipeline_configuration: List[PipeConfiguration]) -> None:
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
        use case pipes.

        '''
        _Pipeline = await self._pipeline_factory.create_pipeline_async(input_port, pipeline_configuration)

        _PipelineResult = None
        while _PipelineResult is None and len(_Pipeline) > 0:

            _Pipe = _Pipeline.pop(0)

            _PipelineResult = await _Pipe.execute_async(input_port, output_port)

            if asyncio.iscoroutine(_PipelineResult):
                await _PipelineResult


class Engine:

    @staticmethod
    def construct_usecase_registry(
            usecase_locations: Optional[List[str]] = ["."],
            directory_exclusion_patterns: Optional[List[str]] = [],
            file_exclusion_patterns: Optional[List[str]] = []) -> Dict[str, List[str]]:
        '''
        TODO: DOC CHANGE
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
        _UsecaseRegistry = {}

        for _Location in usecase_locations:
            _ClassesWithNamespaces = Common.get_all_classes(_Location, directory_exclusion_patterns, file_exclusion_patterns)

            _InputPortClassesWithNamespaces = []
            _PipeClassesWithNamespaces = []

            #TODO: NamedTuple
            for _ClassNamespace in _ClassesWithNamespaces:
                if issubclass(_ClassNamespace[0], InputPort) and _ClassNamespace[0] != InputPort and _ClassNamespace not in _InputPortClassesWithNamespaces:
                    _InputPortClassesWithNamespaces.append(_ClassNamespace)

                if issubclass(_ClassNamespace[0], IPipe) and _ClassNamespace not in _PipeClassesWithNamespaces:
                    _PipeClassesWithNamespaces.append(_ClassNamespace)

            for _PipeNamespace in _PipeClassesWithNamespaces:
                _ExecuteAsyncMethod = next((_Function for _Name, _Function
                                            in inspect.getmembers(_PipeNamespace[0], inspect.isfunction)
                                            if _Name == IPipe.execute_async.__name__), None)

                _InputPortParam = next((_Param for _Param
                                   in inspect.signature(_ExecuteAsyncMethod).parameters.values()
                                   if _Param.annotation != inspect.Parameter.empty
                                   and any(_InputPortNamespace[0] is _Param.annotation for _InputPortNamespace in _InputPortClassesWithNamespaces)), None)

                if _InputPortParam:
                    _UsecaseKey = next(_InputPortNamespace[1] for _InputPortNamespace
                                       in _InputPortClassesWithNamespaces
                                       if type(_InputPortNamespace[0]) == type(_InputPortParam.annotation))
                    if _UsecaseKey:
                        _UsecaseRegistry.setdefault(_UsecaseKey, []).append(_PipeNamespace[1])
                    else:
                        raise ModuleNotFoundError(f"Could not get the source file of {_PipeNamespace[0]}.")

        return _UsecaseRegistry

    @staticmethod
    def _insert_pipe(
            new_pipe: IPipe,
            new_pipe_priority: int,
            pipeline: List[Type[IPipe]],
            pipeline_configuration: List[PipeConfiguration]) -> None:
        '''
        Summary
        -------
        Inserts a new pipe into the pipeline based on the specified configuration.

        Parameters
        ----------
        `new_pipe` The new pipe to be inserted into the pipeline.\n
        `new_pipe_priority` The order the pipe appears in the pipeline configuration.\n
        `pipeline` The current pipeline, represented as a list of pipe types.\n
        `pipeline_configuration` The configuration of the pipeline, specifying the order and types of pipes.

        Exceptions
        ----------
        Raises a `PipeConfigurationError` if the new pipe cannot be inserted into the pipeline.

        '''
        if not pipeline:
            pipeline.append(new_pipe)
            return

        left_pipe_index = None
        right_pipe_index = None

        pipes_from_config = [pipe_config.type for pipe_config in pipeline_configuration]

        for existing_pipe in pipeline:
            existing_pipe_idx = pipes_from_config.index(next(p for p in pipes_from_config if issubclass(type(existing_pipe), p)))

            if existing_pipe_idx < new_pipe_priority and (left_pipe_index is None or existing_pipe_idx > left_pipe_index):
                left_pipe_index = pipeline.index(existing_pipe)
            elif existing_pipe_idx > new_pipe_priority and (right_pipe_index is None or existing_pipe_idx < right_pipe_index):
                right_pipe_index = pipeline.index(existing_pipe)

        if right_pipe_index is not None:
            pipeline.insert(right_pipe_index, new_pipe)
        elif left_pipe_index is not None:
            pipeline.insert(left_pipe_index+1, new_pipe)
        else:
            raise PipeConfigurationError(f"Failed to insert the pipe '{new_pipe}' into the pipeline.")
