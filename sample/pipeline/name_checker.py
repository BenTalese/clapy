
from typing import Generic
from generics import TInputPort, TOutputPort
from pipeline import IPipe, PipePriority


class NameChecker(IPipe, Generic[TInputPort, TOutputPort]):
    
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, NameChecker.__name__)