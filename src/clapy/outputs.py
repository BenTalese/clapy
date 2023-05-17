from abc import ABC, abstractmethod
from typing import Generic

from .generics import TAuthorisationFailure, TValidationFailure


class IAuthenticationOutputPort(ABC):
    '''An output port for when authentication is required by the use case.'''

    @abstractmethod
    async def present_unauthenticated_async() -> None:
        '''Presents an authentication failure.'''
        pass


class IAuthorisationOutputPort(Generic[TAuthorisationFailure], ABC):
    '''An output port for when authorisation is required by the use case.'''

    @abstractmethod     # TODO: Not sure the async keyword is needed really...
    async def present_unauthorised_async(self, authorisation_failure: TAuthorisationFailure) -> None:
        '''Presents an authorisation failure.'''
        pass


class IValidationOutputPort(Generic[TValidationFailure], ABC):
    '''An output port for when validation is required.'''

    @abstractmethod
    async def present_validation_failure_async(self, validation_failure: TValidationFailure) -> None:
        '''Presents a validation failure.'''
        pass
