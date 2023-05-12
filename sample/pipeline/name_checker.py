
from typing import Generic

from src.clapy.generics import TInputPort, TOutputPort
from src.clapy.pipeline import IPipe, PipePriority


class NameChecker(IPipe, Generic[TInputPort, TOutputPort]):
    
    @property
    def priority(self) -> PipePriority:
        return getattr(PipePriority, NameChecker.__name__)