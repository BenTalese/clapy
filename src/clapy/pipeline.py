from abc import ABC, abstractmethod
from enum import Enum
from typing import Coroutine, NamedTuple, Type, cast, get_type_hints

from .common import Common
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
        except Exception:
            return

        _ValidationResult = ValidationResult()

        def validate_attribute(attr_value, type_hint):
            if not hasattr(type_hint, "__origin__"):
                if (type(attr_value) != type_hint
                    and not issubclass(type(attr_value), type_hint)
                    and attr_value is not None):
                    return f"'{attr_name}' must be of type '{type_hint.__name__}'."

            else:
                type_origin = type_hint.__origin__
                type_args = type_hint.__args__

                if not isinstance(attr_value, type_origin):
                    return f"'{attr_name}', or a sub-value of, must be of type '{type_origin.__name__}'."

                elif Common.is_iterable(attr_value):
                    if len(set([type(val) for val in attr_value])) != len(type_args):
                        return f"'{attr_name}' has the wrong number of value types for type '{type_hint}'."

                    for val in attr_value:
                        if (type(val) not in type_args
                            and type(val) not in [ta.__origin__ for ta in type_args if hasattr(ta, "__origin__")]
                            and not any(issubclass(type(val), type_arg) for type_arg in type_args)
                            and val is not None):
                            return f"'{val}' of type {type(val)} does not match the " + \
                            f"type(s) '{', '.join(arg.__name__ for arg in type_args)}' for '{attr_name}'."

                elif type(attr_value) == AttributeChangeTracker:
                    return validate_attribute(
                        attr_value._value,
                        type_args if not hasattr(type_hint, "__origin__") else type_args[0])

        for attr_name, type_hint in get_type_hints(input_port).items():
            try:
                attr_value = getattr(input_port, attr_name)
            except AttributeError:
                continue

            try:
                _ErrorMessage = validate_attribute(attr_value, type_hint)
                if _ErrorMessage:
                    _ValidationResult.add_error(attr_name, _ErrorMessage)
            except Exception as e:
                print(f"[CLAPY ERROR]: Could not validate '{attr_name}' of type '{type_hint}' with value '{attr_value}', see exception: {e}")

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
        except Exception:
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
