import inspect
import re
from typing import List, Tuple

from dependency_injector import containers, providers

from .common import Common
from .engine import Engine, PipelineFactory, UseCaseInvoker
from .exceptions import DependencyConstructionError, DuplicateServiceError
from .pipeline import InputTypeValidator, IPipe, RequiredInputValidator
from .services import IPipelineFactory, IServiceProvider, IUseCaseInvoker

__all__ = ["DependencyInjectorServiceProvider"]


class DependencyInjectorServiceProvider(IServiceProvider):
    '''
    Clapy's default service provider implementation for using Clapy with dependency_injector. Uses
    the DeclarativeContainer from dependency_injector.

    '''

    def __init__(self):
        self._container = containers.DeclarativeContainer()

    def get_service(self, service: type) -> object:
        '''
        Summary
        -------
        Retrieves the specified service from the dependency_injector container.

        Parameters
        ----------
        `service` The service to be retrieved.

        Exceptions
        ----------
        Raises a `LookupError` if the service could not be resolved.

        Returns
        -------
        An instance of the requested service type with a lifetime as defined on the container.

        '''
        _ServiceName, _GenerationSuccess = self._try_generate_service_name(service)

        if _GenerationSuccess:
            _Service = self._container.providers.get(_ServiceName)

            if _Service is not None:
                try:
                    return _Service()
                except TypeError as ex:
                    raise DependencyConstructionError(f"Unable to construct service '{service.__name__}'. " +
                                                      "Make sure all required services are registered in the DI " +
                                                      "container, and make sure all services implementing an " +
                                                      "interface are implemented correctly. " +
                                                      f"See inner exception: {ex}.")

        raise LookupError(f"Unable to retrieve '{service.__name__}' from DI container.")

    def register_service(
            self,
            provider_method: type,
            concrete_type: type,
            interface_type: type = None, # type: ignore
            *args) -> None:
        '''
        Summary
        -------
        Registers a service in the dependency_injector container with its dependencies. If dependencies of the service
        are detected to be registered in the container, they will be linked to the service automatically. Dependencies
        are detected via the type hints of the service's constructor's parameters.

        Parameters
        ----------
        `provider_method` The lifetime of the service, defined using the providers module from dependency_injector.\n
        `concrete_type` The concrete implementation of the service being registered. Can be registered on its own.\n
        `interface_type` The optional interface that the concrete type implements.\n
        `*args` Any required dependencies for this service to be constructed that are not registered in the
        dependency_injector container.

        Exceptions
        ----------
        Raises `DuplicateServiceError` if the dependency_injector container already contains a service of the same type.\n
        Raises `ValueError` if unable to generate a service name for the service.

        '''
        _DependencyName, _GenerationSuccess = self._try_generate_service_name(interface_type or concrete_type)

        if not _GenerationSuccess:
            raise ValueError(f"Failed to generate service name for {interface_type or concrete_type}.")

        if hasattr(self._container, _DependencyName):
            raise DuplicateServiceError(f"An already registered service is conflicting with {interface_type or concrete_type}.")

        _ConstructorDependencies = [_Param for _Param in inspect.signature(concrete_type.__init__).parameters.values() # type: ignore
                                    if _Param.annotation != inspect.Parameter.empty
                                    and self._has_service(_Param.annotation)]

        if not _ConstructorDependencies:
            setattr(self._container, _DependencyName, provider_method(concrete_type, *args))
        else:
            _SubDependencies = []
            for _Dependency in _ConstructorDependencies:
                _SubDependencyName, _ = self._try_generate_service_name(_Dependency.annotation)
                _SubDependencies.append(getattr(self._container, _SubDependencyName))

            setattr(self._container, _DependencyName, provider_method(concrete_type, *_SubDependencies, *args))

    def register_pipe_services(
            self,
            usecase_scan_locations: List[str] = ["."],
            directory_exclusion_patterns: List[str] = [],
            file_exclusion_patterns: List[str] = []) -> None:
        '''
        Summary
        -------
        Scans and registers use case pipes under the specified locations to the dependency_injector
        container. For this class to be registered, it must implement the IPipe interface. Registered
        using `providers.Factory`.

        Parameters
        ----------
        `usecase_scan_locations` An optional list of locations within the project where the usecase services
        should be scanned for. If none are provided, the entire project will be scanned.\n
        `directory_exclusion_patterns` An optional list of regular expression patterns used to exclude directories
        from being scanned.\n
        `file_exclusion_patterns`An optional list of regular expression patterns used to exclude files
        from being scanned and registered.

        '''
        for _Location in usecase_scan_locations:
            _ClassesWithNamespaces = Common.get_all_classes(_Location, directory_exclusion_patterns, file_exclusion_patterns)

            for _ClassNamespace in _ClassesWithNamespaces:
                if issubclass(_ClassNamespace[0], IPipe):
                    self.register_service(providers.Factory, _ClassNamespace[0])

    def configure_clapy_services(
            self,
            usecase_scan_locations: List[str] = ["."],
            directory_exclusion_patterns: List[str] = [],
            file_exclusion_patterns: List[str] = []) -> None:
        '''
        Summary
        -------
        Builds and registers the dependencies of Clapy's use case invoker, returning the built use case
        invoker. Will scan for use cases under the specified locations, or the entire project if
        locations are not provided.

        Parameters
        ----------
        `usecase_scan_locations` An optional list of locations within the project where the usecase services
        should be scanned for. If none are provided, the entire project will be scanned.\n
        `directory_exclusion_patterns` An optional list of regular expression patterns used to exclude directories
        from being scanned.\n
        `file_exclusion_patterns`An optional list of regular expression patterns used to exclude files
        from being scanned and registered.

        Returns
        -------
        An instance of the concrete implementation for the `IUseCaseInvoker`.

        '''
        self.register_pipe_services(usecase_scan_locations,
                                    directory_exclusion_patterns,
                                    file_exclusion_patterns)

        _UsecaseRegistry = Engine.construct_usecase_registry(usecase_scan_locations,
                                                             directory_exclusion_patterns,
                                                             file_exclusion_patterns)

        self.register_service(providers.Singleton, PipelineFactory, IPipelineFactory, self, _UsecaseRegistry)
        self.register_service(providers.Factory, UseCaseInvoker, IUseCaseInvoker)
        self.register_service(providers.Factory, RequiredInputValidator)
        self.register_service(providers.Factory, InputTypeValidator)

    def _try_generate_service_name(self, service: type) -> Tuple[str, bool]:
        '''
        Summary
        -------
        Generates a service name from a given service type by extracting the fully qualified
        name of the service, then replacing dots with underscores.

        Parameters
        ----------
        `service` The service to generate a name for and true on success, otherwise empty string and false.

        Returns
        -------
        The generated name of the service.

        '''
        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(service))

        if not _TypeMatch:
            return "", False

        return _TypeMatch.group().replace('.', '_'), True

    def _has_service(self, service: type) -> bool:
        '''
        Summary
        -------
        Checks if a service exists in the dependency_injector container.

        Parameters
        ----------
        `service` The service that is being checked for existence in the container.

        Returns
        -------
        True if the service could be found, false otherwise.

        '''
        _ServiceName, _GenerationSuccess = self._try_generate_service_name(service)

        if _GenerationSuccess:
            return hasattr(self._container, _ServiceName)

        return False
