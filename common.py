import importlib
import inspect
import re
from typing import List


DIR_EXCLUSIONS = [r"__pycache__"]
FILE_EXCLUSIONS = [r".*__init__\.py", r".*outputport\.py", r".*output_port\.py"]


@staticmethod
def import_class_by_namespace(namespace: str):
    _ModuleName = "".join([part.lower() for part in namespace.rsplit(".", 1)[1].split("_")])
    _Module = importlib.import_module(namespace, package=None)
    _ModuleClasses = inspect.getmembers(_Module, inspect.isclass)
    _ModuleClass = next((obj for name, obj in _ModuleClasses if name.lower() == _ModuleName), None)

    if _ModuleClass is None:
        raise Exception(f"""Could not find class for '{namespace}'. Classes must be named the same as their module
        to be registered in the dependency container. If you do not want this module to be scanned, add it to the
        file exclusions, or be more specific with your scan locations.""")

    return _ModuleClass


@staticmethod
def apply_exclusion_filter(collection: List[str], exclusion_patterns: List[str]) -> None:
    for _ExclusionPattern in exclusion_patterns:
        collection[:] = [_Item for _Item in collection if not re.match(_ExclusionPattern, _Item)]
