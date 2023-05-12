from typing import Generic

from src.clapy.generics import TInputPort, TOutputPort
from src.clapy.pipeline import IPipe


class NameChecker(IPipe, Generic[TInputPort, TOutputPort]):
    pass
