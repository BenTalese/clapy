from abc import ABC, abstractmethod
from typing import Generic

from generics import TAuthorisationFailure, TValidationFailure

class IAuthenticationOutputPort(ABC):
    
    @abstractmethod
    def present_unauthenticated() -> None:
        pass


class IAuthorisationOutputPort(Generic[TAuthorisationFailure], ABC):
    
    @abstractmethod
    def present_unauthorised(self, authorisation_failure: TAuthorisationFailure) -> None:
        pass
    

class IBusinessRuleValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    def present_business_rule_validation_failure(self, validation_failure: TValidationFailure) -> None:
        pass


class IValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    def present_validation_failure(self, validation_failure: TValidationFailure) -> None:
        pass
