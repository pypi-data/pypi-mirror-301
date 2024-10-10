import pytest
import resources.commands
from importlib.abc import Traversable
from importlib.resources import files
from itg_cli.commands import add_pack, add_song, censor, uncensor


def get_test_command_resource(filename: str):
    """Returns a Treversable pointing to tests/resources/config/`filename`"""
    return files(resources.commands).joinpath(filename)


### add_pack


def test_many_pack_directories():
    pass


def test_no_pack_directories():
    pass


def test_macos_files():
    pass


def test_pack_already_exists():
    pass


def test_more_simfiles():
    pass


def test_less_simfiles():
    pass


def test_same_simfiles():
    pass


def test_overwrite_flag():
    pass


def test_overwrite_callback():
    pass
