# from unittest.mock import Mock

# import pytest

# from src.clapy.engine import UseCaseInvoker
# from src.clapy.outputs import IOutputPort
# from src.clapy.pipeline import InputPort, IPipe, PipeConfiguration
# from src.clapy.services import IPipelineFactory

# # INFO: Python 3.7 has jack shit for testing async code

# # @pytest.fixture
# # def mock_pipeline_factory(mocker, get_pipeline):
# #     # my_mock = Mock(spec=IPipelineFactory)
# #     # my_mock.patch.object(mock_pipeline_factory, 'create_pipeline_async', return_value=[Mock()])
# #     # return my_mock
# #     mock = mocker.patch("", spec=IPipelineFactory)
# #     mock.create_pipeline_async.return_value = mocker.AsyncMock()
# #     return mock


# class Pipe(IPipe):
#     async def execute_async(self, input_port: InputPort, output_port: IOutputPort):
#         print("Hello!")


# @pytest.fixture
# def get_pipeline():
#     return [Pipe(), Pipe(), Pipe()]

# class MockPipelineFactory:
#     async def create_pipeline_async(self, input_port, pipeline_configuration):
#         return [Pipe(), Pipe()]

# @pytest.fixture

# def mock_pipeline_factory(mocker, get_pipeline):
#     mock_factory = MockPipelineFactory()
#     mocker.patch('src.clapy.services.IPipelineFactory', return_value=mock_factory)
#     mocker.patch('asyncio.create_task', side_effect=lambda coro: coro())
#     return mock_factory


# # @pytest.fixture
# # def mock_pipeline_factory(mocker, get_pipeline):
# #     mock = Mock(spec=IPipelineFactory)
# #     mock.create_pipeline_async.return_value = AsyncMock()
# #     # mocker.patch.object(mock, 'create_pipeline_async', return_value = mocker.AsyncMock(return_value=get_pipeline))
# #     mocker.patch('src.clapy.services.IPipelineFactory', return_value=mock)
# #     return mock

# @pytest.fixture
# def pipeline_configuration():
#     return [
#         PipeConfiguration(Pipe) # TODO: What if empty config? or pipe missing from config
#     ]

# # TODO: test constructor null argument

# @pytest.mark.asyncio
# async def test__invoke_usecase_async__success__success(mocker, mock_pipeline_factory, pipeline_configuration):
#     # Arrange

#     use_case_invoker = UseCaseInvoker(mock_pipeline_factory)

#     # Mock pipeline creation
#     # mocker.patch.object(mock_pipeline_factory, 'create_pipeline_async', return_value=[Mock()])

#     # Mock pipe execution
#     # mocker.patch.object(Mock, 'execute_async')

#     input_port = Mock()
#     output_port = Mock()

#     # Act
#     result = await use_case_invoker.invoke_usecase_async(input_port, output_port, pipeline_configuration)

#     # Assert
#     # assert result is True  # Assuming your code returns True on success
#     # mock_pipeline_factory.create_pipeline_async.assert_called_once_with(input_port, pipeline_configuration)
#     # Mock.execute_async.assert_called_once_with(input_port, output_port)
#     assert result is True
#     mock_pipeline_factory.create_pipeline_async.assert_called_once_with(input_port, pipeline_configuration)

#     # Assert that execute_async is called for each pipe in the pipeline
#     for pipe in mock_pipeline_factory.create_pipeline_async.return_value:
#         pipe.execute_async.assert_called_once_with(input_port, output_port)

# def test_invoke_usecase_async_ignore_failures(mocker, mock_pipeline_factory, mock_input_port, mock_output_port, mock_pipe_configuration):
#     # Arrange
#     pipeline_configuration = [mock_pipe_configuration]
#     use_case_invoker = UseCaseInvoker(mock_pipeline_factory)

#     # Mock pipeline creation
#     mocker.patch.object(mock_pipeline_factory, 'create_pipeline_async', return_value=[Mock()])

#     # Mock pipe execution with failures
#     mocker.patch.object(Mock, 'execute_async', side_effect=[Exception("Pipe failure")])

#     # Act
#     result = use_case_invoker.invoke_usecase_async(mock_input_port, mock_output_port, pipeline_configuration)

#     # Assert
#     assert result is False  # Assuming your code returns False when there are failures
#     mock_pipeline_factory.create_pipeline_async.assert_called_once_with(mock_input_port, pipeline_configuration)
#     Mock.execute_async.assert_called_once_with(mock_input_port, mock_output_port)

# def test_invoke_usecase_async_stop_on_failure(mocker, mock_pipeline_factory, mock_input_port, mock_output_port, mock_pipe_configuration):
#     # Arrange
#     pipeline_configuration = [mock_pipe_configuration]
#     use_case_invoker = UseCaseInvoker(mock_pipeline_factory)

#     # Mock pipeline creation
#     mocker.patch.object(mock_pipeline_factory, 'create_pipeline_async', return_value=[Mock()])

#     # Mock pipe execution with failures
#     mocker.patch.object(Mock, 'execute_async', side_effect=[Exception("Pipe failure")])

#     # Act
#     result = use_case_invoker.invoke_usecase_async(mock_input_port, mock_output_port, pipeline_configuration)

#     # Assert
#     assert result is False  # Assuming your code returns False when there are failures
#     mock_pipeline_factory.create_pipeline_async.assert_called_once_with(mock_input_port, pipeline_configuration)
#     Mock.execute_async.assert_called_once_with(mock_input_port, mock_output_port)

# def test_invoke_usecase_async_custom_actions(mocker, mock_pipeline_factory, mock_input_port, mock_output_port, mock_pipe_configuration):
#     # Arrange
#     pipeline_configuration = [mock_pipe_configuration]
#     use_case_invoker = UseCaseInvoker(mock_pipeline_factory)

#     # Mock pipeline creation
#     mocker.patch.object(mock_pipeline_factory, 'create_pipeline_async', return_value=[Mock()])

#     # Mock custom actions
#     mocker.patch.object(Mock, 'pre_action')
#     mocker.patch.object(Mock, 'post_action')

#     # Act
#     result = use_case_invoker.invoke_usecase_async(mock_input_port, mock_output_port, pipeline_configuration)

#     # Assert
#     assert result is True  # Assuming your code returns True on success
#     mock_pipeline_factory.create_pipeline_async.assert_called_once_with(mock_input_port, pipeline_configuration)
#     Mock.pre_action.assert_called_once()
#     Mock.post_action.assert_called_once()
