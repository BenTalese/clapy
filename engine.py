import os
from typing import Dict, List, Optional, Type

from dependency_injector import providers #TODO: Tidy up imports

from common import DIR_EXCLUSIONS, FILE_EXCLUSIONS, apply_exclusion_filter, import_class_by_namespace
from generics import TInputPort, TOutputPort
from pipeline import (IAuthenticationVerifier, IAuthorisationEnforcer,
                      IBusinessRuleValidator, IEntityExistenceChecker,
                      IInputPortValidator, IInteractor, IPipe, PipePriority)
from services import IPipelineFactory, IServiceProvider, IUseCaseInvoker


class PipelineFactory(IPipelineFactory):
    
    def __init__(self, service_provider: IServiceProvider, usecase_registry: Dict[str, List[Type[IPipe]]]):
        self._service_provider = service_provider if service_provider is not None else ValueError(f"'{service_provider=}' cannot be None.")
        self._usecase_registry = usecase_registry if usecase_registry is not None else ValueError(f"'{usecase_registry=}' cannot be None.")


    def create_pipeline(self, input_port: TInputPort) -> List[Type[IPipe]]:
        _UsecaseKey = input_port.__module__.rsplit(".", 1)[0]

        if _UsecaseKey not in self._usecase_registry:
            raise KeyError(f"Could not find '{input_port}' in the pipeline registry.")
        
        _PipeNamespaces = self._usecase_registry[_UsecaseKey]["pipes"]

        _PipeClasses = [import_class_by_namespace(_Namespace) for _Namespace in _PipeNamespaces]

        _Pipes = [self._service_provider.get_service(_PipeClass) for _PipeClass in _PipeClasses]
        
        return sorted(_Pipes, key=lambda _Pipe: _Pipe.priority)


class UseCaseInvoker(IUseCaseInvoker):

    def __init__(self, pipeline_factory: IPipelineFactory):
        self._pipeline_factory = pipeline_factory if pipeline_factory is not None else ValueError(f"'{pipeline_factory=}' cannot be None.")


    def can_invoke_usecase(self, input_port: TInputPort, output_port: TOutputPort) -> bool:
        _Pipeline = self._pipeline_factory.create_pipeline(input_port)

        _PipelineResult = None
        while _PipelineResult is None:

            _Pipe = _Pipeline.pop(0)

            if not isinstance(_Pipe, IInteractor):
                _PipelineResult = _Pipe.execute(input_port, output_port)

                if _PipelineResult is not None:
                    return False

            else:
                return True


    def invoke_usecase(self, input_port: TInputPort, output_port: TOutputPort) -> None:
        _Pipeline = self._pipeline_factory.create_pipeline(input_port)

        _PipelineResult = None
        while _PipelineResult is None and len(_Pipeline) > 0:

            _Pipe = _Pipeline.pop(0)

            _PipelineResult = _Pipe.execute(input_port, output_port)

        _PipelineResult()


@staticmethod
def construct_usecase_registry(
    usecase_locations: Optional[List[str]] = ["."],
    directory_exclusion_patterns: Optional[List[str]] = [],
    file_exclusion_patterns: Optional[List[str]] = []) -> Dict[str, List[str]]:

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
                _UsecaseRegistry[_DirectoryNamespace] = { "pipes": _Pipes }

    return _UsecaseRegistry


@staticmethod
def set_pipe_priority(priorities: Dict[str, int]) -> None:
    for key, value in priorities.items():
        setattr(PipePriority, key, value)


@staticmethod
def set_default_pipe_priorities() -> None:
    set_pipe_priority({
        f'{IAuthenticationVerifier.__name__}': 1,
        f'{IEntityExistenceChecker.__name__}': 2,
        f'{IAuthorisationEnforcer.__name__}': 3,
        f'{IBusinessRuleValidator.__name__}': 4,
        f'{IInputPortValidator.__name__}': 5,
        f'{IInteractor.__name__}': 6
    })
