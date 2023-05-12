from abc import ABC, abstractmethod
from typing import Coroutine, Generic, Union

from .generics import TInputPort, TOutputPort


class PipePriorityMeta(type):
    '''The `PipePriorityMeta` class prevents assigning the same priority value to multiple pipes.'''
    def __setattr__(cls, key, value):
        if any(getattr(cls, _Key) == value for _Key in cls.__dict__ if _Key != key):
            raise ValueError(f"Cannot assign pipe priority '{value}' to '{key}'. Priority '{value}' is in use by another pipe.")
            
        super().__setattr__(key, value)


class PipePriority(metaclass=PipePriorityMeta):
    '''Defines the priorities of pipes.'''
    pass


class IPipe(Generic[TInputPort, TOutputPort], ABC):
    '''Marks a class as a pipe. A pipe is a class that must have an execution method and a priority.'''
    @property
    @abstractmethod
    def priority(self) -> PipePriority:
        '''Defines the priority of the pipe within the pipeline.'''
        pass

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


class AuthenticationVerifier(IPipe):
    '''Marks a class as an authentication verifier pipe.'''
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, AuthenticationVerifier.__name__)


class AuthorisationEnforcer(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an authorisation enforcer pipe.'''
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, AuthorisationEnforcer.__name__)

#TODO: Should i have this still? maybe rename?
# Don't forget it is in the README
class BusinessRuleValidator(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as a business rule validator pipe.'''
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, BusinessRuleValidator.__name__)


class EntityExistenceChecker(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an entity existence checker pipe.'''
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, EntityExistenceChecker.__name__)


class InputPortValidator(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an input port validator pipe.'''
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, InputPortValidator.__name__)


class InputPort():
    '''Marks a class as an input port (not an implementation of IPipe).'''
    pass


class Interactor(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an interactor pipe.'''
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, Interactor.__name__)
