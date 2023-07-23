from abc import ABC, abstractmethod
from typing import Dict, List


class AuthorisationResult:
    '''An authorisation result from an authorisation enforcer.'''

    def __init__(self, reason: str) -> None:
        self.reason = reason


class ValidationResult:
    '''
    A validation result from a validator.

    Attributes:
        errors (Dict[str, List[str]]): A dictionary that maps property names to a list of error
        messages associated with each property.
        summary (str): A summary message representing the overall result of the validation.
    '''

    def __init__(
            self,
            errors: Dict[str, List[str]] = {},
            summary: str = "") -> None:
        self.errors = errors
        self.summary = summary

    @classmethod
    def from_error(cls, property: str, error_message: str) -> 'ValidationResult':
        '''
        Creates a ValidationResult instance with a single property error.

        Parameters:
            property (str): The property in error.
            error_message (str): The error message associated with the property.

        Returns:
            ValidationResult: A ValidationResult instance with the specified property error.
        '''
        instance = cls()
        instance.add_error(property, error_message)
        return instance

    @classmethod
    def from_summary(cls, summary: str) -> 'ValidationResult':
        '''
        Creates a ValidationResult instance with a summary message.

        Parameters:
            summary (str): The summary message representing the overall result of the validation.

        Returns:
            ValidationResult: A ValidationResult instance with the specified summary message.
        '''
        instance = cls()
        instance.summary = summary
        return instance

    def add_error(self, property: str, error_message: str) -> None:
        '''
        Adds an error message to the specified property.

        Parameters:
            property (str): The property in error.
            error_message (str): The error message to be added against the property.
        '''
        self.errors.setdefault(property, []).append(error_message) # type: ignore


class IOutputPort(ABC):
    '''Marks a class as a use case output port.'''
    pass


class IAuthenticationOutputPort(ABC):
    '''An output port for when authentication is required by the use case.'''

    @abstractmethod
    async def present_unauthenticated_async(self) -> None:
        '''Presents an authentication failure.'''
        pass


class IAuthorisationOutputPort(ABC):
    '''An output port for when authorisation is required by the use case.'''

    @abstractmethod
    async def present_unauthorised_async(self, authorisation_failure: AuthorisationResult) -> None:
        '''Presents an authorisation failure.'''
        pass


class IValidationOutputPort(ABC):
    '''An output port for when validation is required by the use case.'''

    @abstractmethod
    async def present_validation_failure_async(self, validation_failure: ValidationResult) -> None:
        '''Presents a validation failure.'''
        pass
