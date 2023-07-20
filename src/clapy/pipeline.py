from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Coroutine, Generic, NamedTuple, Type, Union

from .outputs import IValidationOutputPort
from .generics import TInputPort, TOutputPort


class IPipe(Generic[TInputPort, TOutputPort], ABC):
    '''Marks a class as a pipe. A pipe is a class that must have an execution method and a priority.'''

    def __init__(self) -> None:
        self._has_failures = False

    @abstractmethod
    async def execute_async(self, input_port: TInputPort, output_port: TOutputPort) -> Union[Coroutine, None]:
        '''
        Summary
        -------
        Defines the behaviour of the pipe when executed. Must return either a coroutine
        function (an output port method), or no result.

        Parameters
        ----------
        `input_port` The input of the use case to be processed\n
        `output_port` The interface containing output methods to return as a result of the pipe's execution

        Returns
        -------
        `Coroutine` (a method of the output port) if the pipe has a result to return, otherwise `None`.

        '''
        pass

    @property
    def has_failures(self) -> bool:
        return self._has_failures

    @has_failures.setter
    def has_failures(self, value: bool):
        self._has_failures = value


class PipeConfigurationOption(Enum):
    '''Determines the method to be used for adding a pipe when constructing the pipeline.'''

    DEFAULT = "DEFAULT"
    '''If found from searching the use case pipes, the pipe will be added, otherwise it is ignored.'''

    INSERT = "INSERT"
    '''Will insert the provided pipe at the specified location.'''


class PipeConfiguration(NamedTuple):
    '''
    A named tuple representing the configuration for a pipe in a pipeline.

    Attributes:
        type (Type[IPipe]): The type of the pipe.
        option (PipeConfigurationOption): The configuration option for the pipe.
        TODO
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


class InputPort:
    '''Marks a class as an input port (not an implementation of IPipe). The entry point for all use cases.'''
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
    '''#TODO: docs'''
    def wrapper(self):
        return func(self)
    return wrapper


class RequiredInputValidator(IPipe):
    #TODO: Docs

    async def execute_async(self, input_port: Any, output_port: Any) -> Coroutine[Any, Any, Union[Coroutine, None]]:
        properties = [(attr, getattr(input_port.__class__, attr)) for attr in dir(input_port.__class__)
                      if isinstance(getattr(input_port.__class__, attr), property)]

        fails = []

        for name, prop in properties:
            if prop.__get__(input_port) is None:
                fails.append(name)

        if issubclass(type(output_port), IValidationOutputPort) and fails:
            await output_port.present_validation_failure_async(f"Required inputs must have a value: {', '.join(fails)}")
            self.has_failures = True
