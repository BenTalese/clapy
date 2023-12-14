__all__ = [
    "DependencyConstructionError",
    "DuplicateServiceError",
    "PipeConfigurationError"]


class DependencyConstructionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DuplicateServiceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PipeConfigurationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
