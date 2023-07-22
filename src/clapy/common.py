import importlib
import inspect
import os
import re
from typing import List, Tuple


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
    def get_all_classes(
          location: str,
          directory_exclusion_patterns: List[str],
          file_exclusion_patterns: List[str]) -> List[Tuple[object, str]]:
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

            for _ExclusionPattern in directory_exclusion_patterns + DIR_EXCLUSIONS:
                        _Directories[:] = [_Dir for _Dir in _Directories if not re.match(_ExclusionPattern, _Dir)]

            for _ExclusionPattern in file_exclusion_patterns + FILE_EXCLUSIONS:
                        _Files[:] = [_File for _File in _Files if not re.match(_ExclusionPattern, _File)]

            for _File in _Files:
                _Namespace = _Root.replace('/', '.').lstrip(".") + "." + _File[:-3]
                _Module = importlib.import_module(_Namespace, package=None)
                for _Name, _Class in inspect.getmembers(_Module, inspect.isclass):
                    _ClassesWithNamespaces.append((_Class, _Namespace))

        return _ClassesWithNamespaces
