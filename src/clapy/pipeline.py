from abc import ABC, abstractmethod
from enum import Enum
from typing import Coroutine, NamedTuple, Type, cast, get_type_hints

from .outputs import IOutputPort, IValidationOutputPort, ValidationResult
from .utils import AttributeChangeTracker

__all__ = [
    "InputPort",
    "IPipe",
    "PipeConfigurationOption",
    "PipeConfiguration",
    "AuthenticationVerifier",
    "AuthorisationEnforcer",
    "EntityExistenceChecker",
    "InputPortValidator",
    "InputTypeValidator",
    "Interactor",
    "PersistenceRuleValidator",
    "RequiredInputValidator"
    ]


class InputPort:
    '''Marks a class as an input port (not an implementation of IPipe). The entry point for all use cases.'''

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class IPipe(ABC):
    '''Marks a class as a pipe. A pipe is a class that has an execution method and reports on failures.'''

    has_failures = False

    @abstractmethod
    async def execute_async(self, input_port: InputPort, output_port: IOutputPort) -> None:
        '''
        Summary
        -------
        Defines the behaviour of the pipe when executed.

        Parameters
        ----------
        `input_port` The input of the use case to be processed\n
        `output_port` The interface containing methods to output the result of the pipe's execution

        '''
        pass


class PipeConfigurationOption(Enum):
    '''Determines the method to be used for adding a pipe when constructing the pipeline.'''

    DEFAULT = "DEFAULT"
    '''If found from searching the use case pipes, the pipe will be added, otherwise it is ignored.'''

    INSERT = "INSERT"
    '''Will insert the pipe at the specified location, regardless of its presence within the defined used case.'''


class PipeConfiguration(NamedTuple):
    '''
    A named tuple representing the configuration for a pipe in a pipeline.

    Attributes:
        type (Type[IPipe]): The type of the pipe.
        option (PipeConfigurationOption): The inclusion option for the pipe. Defaults to
        `PipeConfigurationOption.DEFAULT`.
        should_ignore_failures (bool): If true, will tell the invoker to continue the pipeline
        regardless of failures. Defaults to `false`.
        pre_action (Coroutine): An optional pre-action to be executed before pipe execution
        post_action (Coroutine): An optional post-action to be executed after pipe execution
    '''
    type: Type[IPipe]
    option: PipeConfigurationOption = PipeConfigurationOption.DEFAULT
    should_ignore_failures: bool = False
    pre_action: Coroutine = None # type: ignore
    post_action: Coroutine = None # type: ignore


class AuthenticationVerifier(IPipe):
    '''Marks a class as an authentication verifier pipe. Used to force a consumer to be authenticated.'''
    pass


class AuthorisationEnforcer(IPipe):
    '''Marks a class as an authorisation enforcer pipe. Used to enforce permission business rules.'''
    pass


class EntityExistenceChecker(IPipe):
    '''Marks a class as an entity existence checker pipe. Used to verify
    entities exist before performing operations on them.'''
    pass


class InputPortValidator(IPipe):
    '''Marks a class as an input port validator pipe. Used to enforce integrity and correctness of input data.'''
    pass


class InputTypeValidator(IPipe):
    '''A use case validation pipe. Verifies all attributes on the InputPort have
    been provided a value matching the type hint defined on the attribute.'''

    async def execute_async(self, input_port: InputPort, output_port: IOutputPort) -> None:
        try:
            input_port.__annotations__
        except:
            return

        _ValidationResult = ValidationResult()

        for attr_name, type_hint in get_type_hints(input_port).items():
            try:
                attr_value = getattr(input_port, attr_name)

                if hasattr(type_hint, "__origin__") and type_hint.__origin__ is AttributeChangeTracker:
                    if not (hasattr(attr_value, "__origin__") and type_hint.__origin__ is AttributeChangeTracker):
                        _ValidationResult.add_error(attr_name, f"'{attr_name}' must be of type '{AttributeChangeTracker.__name__}[{type_hint.__args__[0].__name__}]'.")

                    # Get inner types of AttributeChangeTrackers
                    type_hint = type_hint.__args__[0]
                    inner_attr_value = attr_value.value

                if (type(type_hint) != type(inner_attr_value)
                    and not issubclass(type(inner_attr_value), type_hint)
                    and inner_attr_value is not None):
                    _ValidationResult.add_error(attr_name, f"'{attr_name}' must be of type '{type_hint.__name__}'.")

            except AttributeError:
                pass

        if issubclass(type(output_port), IValidationOutputPort) and _ValidationResult.errors:
            self.has_failures = True
            _ValidationResult.summary = "Types of inputs are mismatching input port's defined attribute types."
            await cast(IValidationOutputPort, output_port).present_validation_failure_async(_ValidationResult)


class Interactor(IPipe):
    '''Marks a class as an interactor pipe. Performs the main action of the use case.'''
    pass


class PersistenceRuleValidator(IPipe):
    '''Marks a class as a persistence rule validator pipe. Used to enforce
    data integrity business rules via a persistence store.'''
    pass


class RequiredInputValidator(IPipe):
    '''A use case validation pipe. Verifies all attributes on the InputPort have
    been provided a value.'''

    async def execute_async(self, input_port: InputPort, output_port: IOutputPort) -> None:
        try:
            input_port.__annotations__
        except:
            return

        _ValidationResult = ValidationResult()

        for attr_name, _ in get_type_hints(input_port).items():
            try:
                _ = getattr(input_port, attr_name)
            except AttributeError:
                _ValidationResult.add_error(attr_name, f"'{attr_name}' must have a value.")

        if issubclass(type(output_port), IValidationOutputPort) and _ValidationResult.errors:
            self.has_failures = True
            _ValidationResult.summary = "Required inputs are missing values."
            await cast(IValidationOutputPort, output_port).present_validation_failure_async(_ValidationResult)
