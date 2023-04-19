from typing import TypeVar

from pipeline import IInputPort, IInteractor

TAuthorisationFailure = TypeVar("TAuthorisationFailure")
TInputPort = TypeVar("TInputPort", bound=IInputPort)
TInteractor = TypeVar("TInteractor", bound=IInteractor)
TOutputPort = TypeVar("TOutputPort")
TServiceType = TypeVar("TServiceType")
TValidationFailure = TypeVar("TValidationFailure")

#TAuthorisationFailure = TypeVar("TAuthorisationFailure", bound=IAuthorisationResult) # TODO: Investigate if IAuthorisationResult is worth doing
#TValidationFailure = TypeVar("TValidationFailure", bound=IValidationResult) # TODO: Investigate if IValidationResult is worth doing
