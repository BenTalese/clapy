import inspect
import re
from typing import Optional, Type
from dependency_injector import containers


class ServiceProvider(containers.DeclarativeContainer):
    pass


@staticmethod
def register_service(service_provider: ServiceProvider, provider_method: Type, concrete_type: Type, interface_type: Optional[Type] = None, *args) -> None:
    _DependencyName = _generate_service_name(interface_type if interface_type is not None else concrete_type)

    if hasattr(service_provider, _DependencyName):
        return

    _ConstructorDependencies = [_Param for _ParamName, _Param in inspect.signature(concrete_type.__init__).parameters.items()
                                    if _ParamName.startswith("DI_") and _Param.annotation != inspect.Parameter.empty]

    if not _ConstructorDependencies:
        setattr(service_provider, _DependencyName, provider_method(concrete_type, *args))
    else:
        _SubDependencies = []
        for _Dependency in _ConstructorDependencies:
            _SubDependencyName = _generate_service_name(_Dependency.annotation)
            _SubDependencies.append(getattr(service_provider, _SubDependencyName))

        setattr(service_provider, _DependencyName, provider_method(concrete_type, *_SubDependencies, *args))


@staticmethod
def get_service(service_provider: ServiceProvider, service: Type) -> object:
    _ServiceName = _generate_service_name(service)

    if _Service := service_provider.providers.get(_ServiceName):
        return _Service()
    else:
        raise LookupError(f"Was not able to retrieve '{service.__name__}' from DI container.")


@staticmethod
def _generate_service_name(service: Type) -> str:
    _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(service))

    if not _TypeMatch:
        raise Exception(f"Could not detect class name from fully qualified name of {service}.")

    return _TypeMatch.group().replace('.', '_')
