import importlib
import inspect
import os
import re
from typing import Any, List, Tuple

__all__ = ["Common"]


DIR_EXCLUSIONS = [r"__pycache__"]
'''
Clapy's default list of regular expression patterns that are used to exclude certain directories
from being scanned during file searches.
'''

FILE_EXCLUSIONS = [r".*__init__\.py", r".*outputport\.py", r".*output_port\.py", r"^.*(?<!\.py)$"]
'''
Clapy's default list of regular expression patterns that are used to exclude certain files
from being scanned during file searches.
'''


class Common:
    '''
    This class contains static utility methods for scanning and importing classes.
    '''

    @staticmethod
    def is_iterable(value: Any):
        """
        The function `is_iterable` checks if a value is iterable or not.

        :param value: The parameter "value" is the input that we want to check if it is iterable or not
        :return: The function is_iterable is returning a boolean value. It returns True if the input
        value is iterable, and False if it is not iterable.
        """
        try:
            iter(value)
            return True
        except TypeError:
            return False

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
            raise ImportError(f"""Could not find class for '{namespace}'. Classes must be named the same as
            their module (e.g. my_example (Module) -> MyExample (Class)) to be registered in the dependency
            container. If you do not want this module to be scanned, add it to the file exclusions, or be
            more specific with your scan locations.""")

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

    @staticmethod
    def get_all_classes(
          location: str,
          directory_exclusion_patterns: List[str],
          file_exclusion_patterns: List[str]) -> List[Tuple[type, str]]:
        '''
        Summary
        -------
        Returns a list of classes with their namespaces found in the specified location.

        Parameters
        ----------
        `location` The root directory to search for classes\n
        `directory_exclusion_patterns` A list of directory patterns to exclude from the search\n
        `file_exclusion_patterns` A list of file patterns to exclude from the search

        Returns
        -------
        A list of tuples containing the class objects and their namespaces.
        '''
        _ClassesWithNamespaces = []

        for _Root, _Directories, _Files in os.walk(location):

            Common.apply_exclusion_filter(_Directories, directory_exclusion_patterns + DIR_EXCLUSIONS)
            Common.apply_exclusion_filter(_Files, file_exclusion_patterns + FILE_EXCLUSIONS)

            for _File in _Files:
                _Namespace = _Root.replace('\\\\', '.').replace('\\', '.').replace('/', '.').lstrip(".") + "." + _File[:-3]
                _Module = importlib.import_module(_Namespace, package=None)
                for _Name, _Class in inspect.getmembers(_Module, inspect.isclass):
                    if _Class.__module__ == _Module.__name__:
                        _ClassesWithNamespaces.append((_Class, _Namespace))

        return _ClassesWithNamespaces
