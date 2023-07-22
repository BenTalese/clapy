from src.clapy.outputs import IOutputPort
from src.clapy.pipeline import IPipe, InputPort


class NameChecker(IPipe, InputPort, IOutputPort):
    pass
