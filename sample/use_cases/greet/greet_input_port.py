from src.clapy.pipeline import InputPort, required


class GreetInputPort(InputPort):

    def __init__(self) -> None:
        self._name = None

    @property
    @required
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
