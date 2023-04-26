from abc import ABC, abstractmethod
from typing import Generic

from generics import TAuthorisationFailure, TValidationFailure

class IAuthenticationOutputPort(ABC):
    
    @abstractmethod
    async def present_unauthenticated_async() -> None:
        pass


class IAuthorisationOutputPort(Generic[TAuthorisationFailure], ABC):
    
    @abstractmethod
    async def present_unauthorised_async(self, authorisation_failure: TAuthorisationFailure) -> None:
        pass
    

class IBusinessRuleValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    async def present_business_rule_validation_failure_async(self, validation_failure: TValidationFailure) -> None:
        pass


class IValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    async def present_validation_failure_async(self, validation_failure: TValidationFailure) -> None:
        pass
