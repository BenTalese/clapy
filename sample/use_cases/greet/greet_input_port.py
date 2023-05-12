from src.clapy.pipeline import InputPort


class GreetInputPort(InputPort):

    def __init__(self, name: str):
        self.name = name