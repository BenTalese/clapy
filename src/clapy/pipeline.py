from abc import ABC, abstractmethod
from typing import Coroutine, Generic, Union

from .generics import TInputPort, TOutputPort


class IPipe(Generic[TInputPort, TOutputPort], ABC):
    '''Marks a class as a pipe. A pipe is a class that must have an execution method and a priority.'''

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
    pass


class AuthorisationEnforcer(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an authorisation enforcer pipe.'''
    pass


#TODO: Should i have this still? maybe rename?
# Don't forget it is in the README
class BusinessRuleValidator(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as a business rule validator pipe.'''
    pass


class EntityExistenceChecker(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an entity existence checker pipe.'''
    pass


class InputPortValidator(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an input port validator pipe.'''
    pass


class InputPort():
    '''Marks a class as an input port (not an implementation of IPipe).'''
    pass


class Interactor(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an interactor pipe.'''
    pass
