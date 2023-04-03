from abc import ABC, abstractmethod
from typing import Generic
from .generics import TInputPort, TOutputPort


class PipePriority:
    __initialized = False

    def __init__(self, **kwargs):
        if not self.__initialized:
            for key, value in self.__GetDefaultValues().items():
                setattr(self, key, value)
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.__initialized = True

    def __GetDefaultValues(self):
        return {
            f'{IAuthenticationVerifier.__name__}': 1,
            f'{IEntityExistenceChecker.__name__}': 2,
            f'{IAuthorisationEnforcer.__name__}': 3,
            f'{IBusinessRuleValidator.__name__}': 4,
            f'{IInputPortValidator.__name__}': 5,
            f'{IInteractor.__name__}': 6,
        }

    def __setattr__(self, key, value):
        if self.__initialized and key not in self.__dict__:
            raise TypeError("Cannot add new values to an initialized CustomEnum")
        if key is not '_CustomEnum__initialized' and any(getattr(self, k) == value for k in self.__dict__):
            raise ValueError(f"Cannot assign pipe priority '{value}' to '{key}'. Priority '{value}' is in use by another pipe.")
        super().__setattr__(key, value)


class IPipe(Generic[TInputPort, TOutputPort], ABC):

    def __init__(self):
        self.m_CanInvokeNextPipe = True

    @property
    def CanInvokeNextPipe(self) -> bool:
        return self.m_CanInvokeNextPipe
    
    @property
    @abstractmethod
    def Priority(self) -> int: # TODO: this was "-> PipePriority", but this should be built in a way the user can easily configure it
        pass                    # Also, probably don't want IPipe to be aware of how it is ordered

    @abstractmethod
    def Execute(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass


class IAuthorisationEnforcer(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def Priority(self) -> PipePriority:
        return PipePriority.AuthorisationEnforcer
