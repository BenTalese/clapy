from typing import TypeVar

from pipeline import InputPort, Interactor


TAuthorisationFailure = TypeVar("TAuthorisationFailure")
TInputPort = TypeVar("TInputPort", bound=InputPort) #TODO: This one is questionable too...
TInteractor = TypeVar("TInteractor", bound=Interactor) #TODO: Is this even used anywhere anymore?
TOutputPort = TypeVar("TOutputPort")
TServiceType = TypeVar("TServiceType")
TValidationFailure = TypeVar("TValidationFailure")

#TAuthorisationFailure = TypeVar("TAuthorisationFailure", bound=IAuthorisationResult) # TODO: Investigate if IAuthorisationResult is worth doing
#TValidationFailure = TypeVar("TValidationFailure", bound=IValidationResult) # TODO: Investigate if IValidationResult is worth doing
