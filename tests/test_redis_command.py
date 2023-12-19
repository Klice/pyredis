import pytest
from pyredis.redis_command_parser import RedisCommand
from pyredis.redis_server import REDIS_COMMANDS


@pytest.fixture
def command():
    return REDIS_COMMANDS["SET"]


class TestParamList:
    def test_extra_args(self):
        command = RedisCommand(["*key"])
        assert command.parse(["key1", "key2", "key3"])["key"] == ["key1", "key2", "key3"]


class TestConfigCommand:
    def test_extra_args(self):
        command = RedisCommand(allow_extra=True)
        command.parse(["key"])


class TestSetCommand:

    def test_set_no_args(self, command):
        res = command.parse(["somekey", "somevalue"])
        assert res["key"] == "somekey"
        assert res["value"] == "somevalue"

    def test_set_nx_flag(self, command):
        res = command.parse(["somekey", "somevalue", "XX"])
        assert res["is_xx"] is True

    def test_set_xx_flag(self, command):
        res = command.parse(["somekey", "somevalue", "NX"])
        assert res["is_nx"] is True

    def test_set_keepttp_flag(self, command):
        res = command.parse(["somekey", "somevalue", "KEEPTTL"])
        assert res["is_keepttl"] is True

    def test_set_mutually_exclusive_flags_error(self, command):
        with pytest.raises(Exception) as _:
            command.parse(["somekey", "somevalue", "NX", "XX"])

    def test_set_ex(self, command):
        res = command.parse(["somekey", "somevalue", "EX", '123'])
        assert res["ex"] == 123

    def test_set_mutually_exclusive_params_error(self, command):
        with pytest.raises(Exception) as _:
            command.parse(["somekey", "somevalue", "EX", '123', "PX", '123'])

    def test_set_mutually_exclusive_param_and_flag_error(self, command):
        with pytest.raises(Exception) as _:
            command.parse(["somekey", "somevalue", "EX", '123', "KEEPTTL"])

    def test_set_param_wrong_type(self, command):
        with pytest.raises(Exception) as _:
            command.parse(["somekey", "somevalue", "EX", "aaa"])

    def test_set_invalid_arg(self, command):
        with pytest.raises(Exception) as ex_info:
            command.parse(["somekey", "somevalue", "FFFF"])
        assert "Invalid argument" in str(ex_info.value)
