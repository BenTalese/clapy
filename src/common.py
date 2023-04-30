import importlib
import inspect
import re
from typing import List


DIR_EXCLUSIONS = [r"__pycache__"]
'''
Clapy's default list of regular expression patterns that are used to exclude certain directories
from being scanned during file searches.
'''
FILE_EXCLUSIONS = [r".*__init__\.py", r".*outputport\.py", r".*output_port\.py"]
'''
Clapy's default list of regular expression patterns that are used to exclude certain files
from being scanned during file searches.
'''


@staticmethod
def import_class_by_namespace(namespace: str) -> type:
    '''
    Summary
    -------
    Imports the first class matching the module by name under the provided namespace.
    
    Parameters
    ----------
    `namespace` A string that represents the fully qualified name of a Python module.
    It is used to dynamically import and retrieve a class object from the specified module.
    
    Exceptions
    -------
    Raises an `ImportError` if the class cannot be found.

    Returns
    -------
    The class object corresponding to the namespace passed as an argument.

    Example
    -------
    `example_to_demonstrate.py`  (module)\n
        | -- `OtherClassA`\n
        | -- `ExampleToDemonstrate`    (class to be imported)\n
        | -- `OtherClassB`\n
        | -- `OtherClassC`\n
    
    '''
    _ModuleName = "".join([part.lower() for part in namespace.rsplit(".", 1)[1].split("_")])
    _Module = importlib.import_module(namespace, package=None)
    _ModuleClasses = inspect.getmembers(_Module, inspect.isclass)
    _ModuleClass = next((obj for name, obj in _ModuleClasses if name.lower() == _ModuleName), None)

    if _ModuleClass is None:
        raise ImportError(f"""Could not find class for '{namespace}'. Classes must be named the same as their module (e.g. my_example 
        (Module) -> MyExample (Class)) to be registered in the dependency container. If you do not want this module to be scanned,
        add it to the file exclusions, or be more specific with your scan locations.""")

    return _ModuleClass


@staticmethod
def apply_exclusion_filter(collection: List[str], exclusion_patterns: List[str]) -> None:
    '''
    Summary
    -------
    Applies RegEx exclusion patterns to a collection of strings and removes any
    items that match those patterns.
    
    Parameters
    ----------
    `collection` A list of strings that represents the collection of items that need
    to be filtered.\n
    `exclusion_patterns` A list of regular expression patterns that should be used to exclude
    certain items from the collection.

    Example
    -------
    my_collection = ["a", "b", "c", "d"]\n
    exclusion_patterns = ["b", "d"]\n
    MyClass.apply_exclusion_filter(my_collection, exclusion_patterns)\n
    print(my_collection)  # Output: ["a", "c"]
    
    '''
    for _ExclusionPattern in exclusion_patterns:
        collection[:] = [_Item for _Item in collection if not re.match(_ExclusionPattern, _Item)]
