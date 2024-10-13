# pylint: disable=missing-module-docstring

import sys
from pathlib import Path

import pytest
import tomlkit


@pytest.fixture(scope="session")
def toml_file_init(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create a toml file to test global initialization"""
    file_path = tmp_path_factory.mktemp(".example_init") / "config.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "field0": 33.33,
            },
            fptr,
        )
    return file_path


def test_global_initialization(
    monkeypatch: pytest.MonkeyPatch,
    toml_file_init: Path,  # pylint: disable=redefined-outer-name
) -> None:
    """Test global initialization"""
    monkeypatch.setattr(
        sys, "argv", ["test_global_initialization", "-a", str(toml_file_init)]
    )
    from .config_example_module_global import (  # pylint: disable=import-outside-toplevel
        test_global,
    )

    assert test_global == 33.33
