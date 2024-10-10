import tempfile
import pytest
import resources.config
from importlib.abc import Traversable
from importlib.resources import files
from itg_cli._config import CLISettings
from itg_cli._config import ConfigError
from pathlib import Path
from tomlkit.toml_file import TOMLFile


def get_test_config_resource(filename: str) -> Traversable:
    """Returns a Treversable pointing to tests/resources/config/`filename`"""
    return files(resources.config).joinpath(filename)


### Holistic Tests
# def test_default_config():
#     with tempfile.TemporaryDirectory() as temp:
#         temp = Path(temp)
#         print("TEMP:", temp)
#         CLISettings(temp / "config.toml", write_default=True)


### CLISettings.__init__


def test_missing_tables():
    with pytest.raises(ConfigError, match=r"Missing table (.*) in config: .*"):
        CLISettings(get_test_config_resource("missing_tables.toml"))


def test_missing_required_keys():
    with pytest.raises(
        ConfigError, match=r"Required field (.*) is empty or unbound in config: .*"
    ):
        CLISettings(get_test_config_resource("missing_fields.toml"))


# def test_extra_fields():
#     pass
#     CLISettings(get_test_config_resource("extra_keys.toml"))


### CLISettings.__write_default_toml


# def test_unknown_platform():
#     pass


# def test_defaults_dont_exist():
#     pass


def test_toml_not_exist():
    with pytest.raises(FileNotFoundError):
        CLISettings(get_test_config_resource("doesnt_exist.toml"))


### CLISettings.__validate_dirs


# def test_nonexistent_directories():
#     pass


# def test_unwritable_directories():
#     pass


# def test_none_downloads():
#     pass


# def test_downloads():
#     pass
