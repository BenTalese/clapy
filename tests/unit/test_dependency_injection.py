import pytest

from src.clapy.dependency_injection import DependencyInjectorServiceProvider


# ---------------- get_service tests ----------------

@pytest.fixture
def mock_service():
    class MockService:
        pass
    return MockService


def test__get_service__ServiceExists__ReturnsInstanceOfService(mocker, mock_service):
    # Arrange
    service_provider = DependencyInjectorServiceProvider()
    service_provider._container = mocker.Mock()
    service_provider._container.providers.get.return_value = mock_service

    # Act
    result = service_provider.get_service(mock_service)

    # Assert
    assert isinstance(result, mock_service)


def test__get_service__ServiceDoesNotExist__RaisesLookupError(mocker, mock_service):
    # Arrange
    service_provider = DependencyInjectorServiceProvider()
    service_provider._container = mocker.Mock()
    service_provider._container.providers.get.return_value = None

    # Act and Assert
    with pytest.raises(LookupError):
        service_provider.get_service(mock_service)

# end get_service tests


# ---------------- register_service tests ----------------

# end register_service tests
