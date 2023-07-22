from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple, Type

from .outputs import IOutputPort, IValidationOutputPort, ValidationResult


class InputPort:
    '''Marks a class as an input port (not an implementation of IPipe). The entry point for all use cases.'''
    pass


class IPipe(InputPort, IOutputPort, ABC):
    '''Marks a class as a pipe. A pipe is a class that has an execution method and reports on failures.'''

    def __init__(self) -> None:
        self._has_failures = False

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

    @property
    def has_failures(self) -> bool:
        '''Determines whether or not a failure has occurred during the pipe's execution.'''
        return self._has_failures

    @has_failures.setter
    def has_failures(self, value: bool):
        self._has_failures = value


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
    '''
    type: Type[IPipe]
    option: PipeConfigurationOption = PipeConfigurationOption.DEFAULT
    should_ignore_failures: bool = False


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


class Interactor(IPipe):
    '''Marks a class as an interactor pipe. Performs the main action of the use case.'''
    pass


class PersistenceRuleValidator(IPipe):
    '''Marks a class as a persistence rule validator pipe. Used to enforce
    data integrity business rules via a persistence store.'''
    pass


def required(func):
    '''Marks a property on an InputPort as required. Used alongside the `RequiredInputValidator`
    pipe, the `required` decorator enforces values to be supplied to use cases.'''
    def wrapper(self):
        return func(self)
    return wrapper


class RequiredInputValidator(IPipe):
    '''A validation pipe, used to check if any required inputs from the use case's InputPort have
    not been given a value. Required inputs are identified via the `required` decorator.'''

    async def execute_async(self, input_port: InputPort, output_port: IValidationOutputPort) -> None:
        _Properties = [(attr, getattr(input_port.__class__, attr)) for attr in dir(input_port.__class__)
                      if isinstance(getattr(input_port.__class__, attr), property)]

        _MissingInputs = []

        for _Name, _Property in _Properties:
            if _Property.__get__(input_port) is None:
                _MissingInputs.append(_Name)

        if issubclass(type(output_port), IValidationOutputPort) and _MissingInputs:
            await output_port.present_validation_failure_async(
                ValidationResult.from_summary(f"Required inputs must have a value: {', '.join(_MissingInputs)}"))
            self.has_failures = True
