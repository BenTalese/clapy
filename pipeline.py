from abc import ABC, abstractmethod
from typing import Callable, Generic

from generics import TInputPort, TOutputPort


class PipePriorityMeta(type):
    
    def __setattr__(cls, key, value):
        if any(getattr(cls, _Key) == value for _Key in cls.__dict__ if _Key != key):
            raise ValueError(f"Cannot assign pipe priority '{value}' to '{key}'. Priority '{value}' is in use by another pipe.")
            
        super().__setattr__(key, value)


class PipePriority(metaclass=PipePriorityMeta):
    pass


class IPipe(Generic[TInputPort, TOutputPort], ABC):

    @property
    @abstractmethod
    def priority(self) -> PipePriority:
        pass

    @abstractmethod
    def execute(self, input_port: TInputPort, output_port: TOutputPort) -> Callable | None:
        pass


class IAuthenticationVerifier(IPipe, ABC):
    
    @property
    def priority(self) -> PipePriority:
        return PipePriority.IAuthenticationVerifier


class IAuthorisationEnforcer(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def priority(self) -> PipePriority:
        return PipePriority.IAuthorisationEnforcer


class IBusinessRuleValidator(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def priority(self) -> PipePriority:
        return PipePriority.IBusinessRuleValidator


class IEntityExistenceChecker(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def priority(self) -> PipePriority:
        return PipePriority.IEntityExistenceChecker


class IInputPortValidator(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def priority(self) -> PipePriority:
        return PipePriority.IInputPortValidator


class IInputPort(ABC):
    pass


class IInteractor(IPipe, Generic[TInputPort, TOutputPort], ABC):

    @property
    def priority(self) -> PipePriority:
        return PipePriority.IInteractor
