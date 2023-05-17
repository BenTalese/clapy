from unittest.mock import Mock

import pytest

from src.clapy.common import Common


# ---------------- import_class_by_namespace tests ----------------

@pytest.fixture
def mock_classes():
    return [
        ('', Mock()),
        ('CoffeeMakerPro2000', Mock()),
        ('CoffeeMakerPro200', Mock()),
        ('CoffeeMaker_Pro2000', Mock())
    ]


@pytest.fixture
def mock_module():
    return Mock()


def test__import_class_by_namespace__ModuleContainsManyClasses__ImportsClassMatchingModuleName(mocker, mock_classes, mock_module):  # noqa E501
    # Arrange
    mocker.patch("inspect.getmembers", return_value=mock_classes)
    mocker.patch('importlib.import_module', return_value=mock_module)

    _Namespace = 'some.place.in.project.coffee_maker_pro_2000'

    _Expected = mock_classes[1][1]

    # Act
    _Actual = Common.import_class_by_namespace(_Namespace)

    # Assert
    assert _Actual == _Expected


def test__import_class_by_namespace__NoMatchingClassExists__RaisesImportError(mocker, mock_classes, mock_module):
    # Arrange
    mock_classes.pop(1)

    mocker.patch("inspect.getmembers", return_value=mock_classes)
    mocker.patch('importlib.import_module', return_value=mock_module)

    _Namespace = 'some.place.in.project.coffee_maker_pro_2000'

    # Act and Assert
    with pytest.raises(ImportError):
        Common.import_class_by_namespace(_Namespace)

# end import_class_by_namespace tests


# ---------------- apply_exclusion_filter tests ----------------

@pytest.fixture
def file_names():
    return [
        "file1.txt",
        "file2.py",
        "file3.py",
        "file4.txt"
    ]


@pytest.fixture
def patterns():
    return [
        r".*file1\.py",
        r".*file4\.py",
        r"^.*(?<!\.py)$"
    ]


def test__apply_exclusion_filter__NoPatternsMatchItems__CollectionNotModified(file_names, patterns):
    # Arrange
    patterns.pop(2)

    _Expected = ["file1.txt", "file2.py", "file3.py", "file4.txt"]

    # Act
    Common.apply_exclusion_filter(file_names, patterns)

    # Assert
    assert file_names == _Expected


def test__apply_exclusion_filter__NoPatternsProvided__CollectionNotModified(file_names, patterns):
    # Arrange
    patterns = []

    _Expected = ["file1.txt", "file2.py", "file3.py", "file4.txt"]

    # Act
    Common.apply_exclusion_filter(file_names, patterns)

    # Assert
    assert file_names == _Expected


def test__apply_exclusion_filter__EmptyCollection__CollectionNotModified(file_names, patterns):
    # Arrange
    file_names = []
    _Expected = []

    # Act
    Common.apply_exclusion_filter(file_names, patterns)

    # Assert
    assert file_names == _Expected


def test__apply_exclusion_filter__MultipleItemsMatchPattern__MatchingItemsRemovedFromCollection(file_names, patterns):
    # Arrange
    _Expected = ["file2.py", "file3.py"]

    # Act
    Common.apply_exclusion_filter(file_names, patterns)

    # Assert
    assert file_names == _Expected

# end apply_exclusion_filter tests
