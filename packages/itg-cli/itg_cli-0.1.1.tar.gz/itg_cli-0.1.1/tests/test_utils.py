import pytest
import resources.utils
from importlib.abc import Traversable
from importlib.resources import files
from itg_cli._utils import (
    setup_working_dir,
    simfile_paths,
    delete_macos_files,
    extract,
)
from pathlib import Path
from tempfile import TemporaryDirectory

def get_test_utils_resource(filename: str) -> Traversable:
    """Returns a Treversable pointing to tests/resources/config/`filename`"""
    return files(resources.utils).joinpath(filename)



def test_extract_flat_zip():
    with TemporaryDirectory() as temp:
        dest = Path(temp)
        archive = 
        assert dest.rglob