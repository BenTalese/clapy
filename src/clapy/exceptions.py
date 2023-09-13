__all__ = ["DuplicateServiceError", "PipeConfigurationError"]


class DuplicateServiceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PipeConfigurationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
