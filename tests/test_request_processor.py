from unittest.mock import Mock
import pytest

from redis.request_processor import RequestProcessor
from redis.types import RedisError, SimpleString


@pytest.fixture
def mock_server():
    return Mock()


@pytest.fixture
def processor(mock_server):
    return RequestProcessor(mock_server)


def test_inline_command(mock_server, processor):
    processor.process_request(b'PING')
    mock_server.run.assert_called_with(['PING'])


def test_inline_command_output(mock_server, processor):
    mock_server.run.return_value = "PONG"
    res = processor.process_request(b'PING')
    assert res == b'PONG\r\n'


def test_inline_command_with_args(mock_server, processor):
    processor.process_request(b'get key')
    mock_server.run.assert_called_with(['get', 'key'])


def test_array_command(mock_server, processor):
    processor.process_request("*2\r\n$3\r\nget\r\n$3\r\nkey\r\n".encode('ascii'))
    mock_server.run.assert_called_with(["get", "key"])


def test_array_command_serialized_output(mock_server, processor):
    mock_server.run.return_value = SimpleString("PONG")
    res = processor.process_request("*2\r\n$3\r\nget\r\n$3\r\nkey\r\n".encode('ascii'))
    assert res == "+PONG\r\n".encode('ascii')


def test_inline_command_error(mock_server, processor):
    mock_server.run.return_value = RedisError("ERROR")
    assert processor.process_request(b'PING') == b"ERROR\r\n"
