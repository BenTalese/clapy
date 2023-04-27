import inspect
import os
import re
from abc import ABC, abstractmethod
from typing import List, Optional, Type

from dependency_injector import containers, providers

from common import DIR_EXCLUSIONS, FILE_EXCLUSIONS, apply_exclusion_filter, import_class_by_namespace
from engine import PipelineFactory, UseCaseInvoker, construct_usecase_registry
from generics import TServiceType
from pipeline import IPipe
from services import IPipelineFactory, IServiceProvider, IUseCaseInvoker

class IDependencyInjectorServiceProvider(IServiceProvider, ABC):
    '''
    Clapy's default service provider interface for using Clapy with dependency_injector.

    '''

    @abstractmethod
    def register_service(
        self,
        provider_method: Type,
        concrete_type: Type[TServiceType],
        interface_type: Optional[Type[TServiceType]] = None,
        *args) -> None:
        '''
        Summary
        -------
        Registers a service in the dependency_injector container with its dependencies.
        
        Parameters
        ----------
        `provider_method` The lifetime of the service, defined using the providers module from dependency_injector.\n
        `concrete_type` The concrete implementation of the service being registered. Can be registered on its own.\n
        `interface_type` The optional interface that the concrete type implements.\n
        `*args` Any required dependencies for this service to be constructed that are not registered in the dependency_injector container.
        
        '''
        pass

    
    @abstractmethod
    def register_usecase_services(
        self,
        usecase_scan_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> None:
        '''
        Summary
        -------
        Scans and registers use case pipes under the specified locations to the dependency_injector
        container.
        
        Parameters
        ----------
        `usecase_scan_locations` An optional list of locations within the project where the usecase services
        should be scanned for.\n
        `directory_exclusion_patterns` An optional list of regular expression patterns used to exclude directories
        from being scanned.\n
        `file_exclusion_patterns`An optional list of regular expression patterns used to exclude files
        from being scanned and registered.
        
        '''
        pass

    @abstractmethod
    def construct_usecase_invoker(
        self,
        usecase_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> IUseCaseInvoker:
        '''
        Summary
        -------
        Builds and registers the dependencies of Clapy's use case invoker, returning the built use case
        invoker.
        
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
        An instance of the concrete implementation for the `IUseCaseInvoker`.
        
        '''
        pass


class DependencyInjectorServiceProvider(IDependencyInjectorServiceProvider):
    '''
    Clapy's default service provider implementation for using Clapy with dependency_injector. Uses
    DeclarativeContainer from dependency_injector.

    '''

    def __init__(self):
        self._container = containers.DeclarativeContainer()


    def get_service(self, service: Type[TServiceType]) -> TServiceType:
        '''
        Summary
        -------
        Retrieves the specified service from the dependency_injectior container.
        
        Parameters
        ----------
        `service` The service to be retrieved.

        Exceptions
        -------
        Raises a LookupError if the service could not be resolved.
        
        Returns
        -------
        An instance of the requested service type with a lifetime as defined on the container.
        
        '''
        _ServiceName = self._generate_service_name(service)

        if _Service := self._container.providers.get(_ServiceName):
            return _Service()
        else:
            raise LookupError(f"Was not able to retrieve '{service.__name__}' from DI container.")


    def register_service(self, provider_method: Type, concrete_type: Type[TServiceType], interface_type: Optional[Type[TServiceType]] = None, *args) -> None:
        '''
        Summary
        -------
        Registers a service in the dependency_injector container with its dependencies. If dependencies of the service
        are detected to be registered in the container, they will be linked to the service automatically.
        
        Parameters
        ----------
        `provider_method` The lifetime of the service, defined using the providers module from dependency_injector.\n
        `concrete_type` The concrete implementation of the service being registered. Can be registered on its own.\n
        `interface_type` The optional interface that the concrete type implements.\n
        `*args` Any required dependencies for this service to be constructed that are not registered in the dependency_injector container.
        
        Exceptions
        -------
        Raises an exception if the dependency_injector container already contains a service of the same type.
        
        '''
        _DependencyName = self._generate_service_name(interface_type if interface_type is not None else concrete_type)

        if hasattr(self._container, _DependencyName):
            raise Exception(f"An already registered service is conflicting with {interface_type if interface_type is not None else concrete_type}.") # FIXME: Exception, fix docs

        _ConstructorDependencies = [_Param for _Param in inspect.signature(concrete_type.__init__).parameters.values()
                                        if _Param.annotation != inspect.Parameter.empty and self._has_service(_Param.annotation)]

        if not _ConstructorDependencies:
            setattr(self._container, _DependencyName, provider_method(concrete_type, *args))
        else:
            _SubDependencies = []
            for _Dependency in _ConstructorDependencies:
                _SubDependencyName = self._generate_service_name(_Dependency.annotation)
                _SubDependencies.append(getattr(self._container, _SubDependencyName))

            setattr(self._container, _DependencyName, provider_method(concrete_type, *_SubDependencies, *args))


    def register_usecase_services(
        self,
        usecase_scan_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> None:
        '''
        Summary
        -------
        Scans and registers use case pipes under the specified locations to the dependency_injector
        container. There must be a class within the file that matches by name. For this class to be
        registered, it must also implement the IPipe interface. Registered using providers.Factory. 
        
        Parameters
        ----------
        `usecase_scan_locations` An optional list of locations within the project where the usecase services
        should be scanned for. If none are provided, the entire project will be scanned.\n
        `directory_exclusion_patterns` An optional list of regular expression patterns used to exclude directories
        from being scanned.\n
        `file_exclusion_patterns`An optional list of regular expression patterns used to exclude files
        from being scanned and registered.
        
        '''
        directory_exclusion_patterns = directory_exclusion_patterns + DIR_EXCLUSIONS
        file_exclusion_patterns = file_exclusion_patterns + FILE_EXCLUSIONS

        for _Location in usecase_scan_locations:
            for _Root, _Directories, _Files in os.walk(_Location):

                apply_exclusion_filter(_Directories, directory_exclusion_patterns)
                apply_exclusion_filter(_Files, file_exclusion_patterns)

                for _File in _Files:
                    _Namespace = _Root.replace('/', '.') + "." + _File[:-3]
                    _Class = import_class_by_namespace(_Namespace)

                    if issubclass(_Class, IPipe):
                        self.register_service(providers.Factory, _Class)


    def construct_usecase_invoker(
        self,
        usecase_scan_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> IUseCaseInvoker:
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
        _UsecaseRegistry = construct_usecase_registry(usecase_scan_locations, directory_exclusion_patterns, file_exclusion_patterns)
        self.register_service(providers.Singleton, PipelineFactory, IPipelineFactory, self, _UsecaseRegistry)
        self.register_service(providers.Factory, UseCaseInvoker, IUseCaseInvoker)
        return self.get_service(IUseCaseInvoker)


    def _generate_service_name(self, service: Type[TServiceType]) -> str:
        '''
        Summary
        -------
        Generates a service name from a given service type by extracting the fully qualified
        name of the service, then replacing dots with underscores.
        
        Parameters
        ----------
        `service` The service to generate a name for.

        Exceptions
        -------
        Raises an exception if the method fails to extract the fully qualified name of the service.
        
        Returns
        -------
        The generated name of the service.
        
        '''
        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(service))

        if not _TypeMatch:
            raise Exception(f"Could not generate name from fully qualified name of {service}.") #TODO: Exception, you know the drill :(

        return _TypeMatch.group().replace('.', '_')


    def _has_service(self, service: Type[TServiceType]) -> bool:
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
        try:
            return hasattr(self._container, self._generate_service_name(service))
        except:
            pass
