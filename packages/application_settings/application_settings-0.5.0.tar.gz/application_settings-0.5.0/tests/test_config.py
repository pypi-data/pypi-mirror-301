# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
import json
import sys
from pathlib import Path
from typing import Any

import pytest
import tomlkit
from loguru import logger

from application_settings import (
    LOGGER_NAME,
    ConfigBase,
    ConfigSectionBase,
    PathOpt,
    ValidationError,
    config_filepath_from_cli,
    dataclass,
    use_standard_logging,
)


@dataclass(frozen=True)
class AnExampleConfigSubSection(ConfigSectionBase):
    """Example of a Config subsection"""

    field3: tuple[int, str] = (3, "yes")


@dataclass(frozen=True)
class AnExample1ConfigSection(ConfigSectionBase):
    """Example 1 of a Config section"""

    field1: str = "field1"
    field2: int = 2
    subsec: AnExampleConfigSubSection = AnExampleConfigSubSection()


@dataclass(frozen=True)
class AnExample1Config(ConfigBase):
    """Example Config"""

    field0: float = 2.2
    section1: AnExample1ConfigSection = AnExample1ConfigSection()


@dataclass(frozen=True)
class Config(ConfigBase):
    """Config class def"""


class ConfigNoDataclass(ConfigBase):
    """Config class def, without dataclass decorator"""


@dataclass
class ConfigUnfrozenDataclass(ConfigBase):
    """Config class def, without dataclass decorator"""


@pytest.fixture(scope="session")
def toml_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    file_path = (
        tmp_path_factory.mktemp(AnExample1Config.default_foldername())
        / AnExample1Config.default_filename()
    )
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "field0": 33.33,
                "section1": {
                    "field1": "f1",
                    "field2": 22,
                    "subsec": {"field3": (-3, "no")},
                },
            },
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def toml_file_inc1(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_folder = tmp_path_factory.mktemp(AnExample1Config.default_foldername())
    file_path = tmp_folder / "conf_inc.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "section1": {
                    "field1": "f1",
                    "field2": 22,
                    "subsec": {"field3": (-3, "no")},
                },
            },
            fptr,
        )
    file_path = tmp_folder / "conf_main.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "field0": 33.33,
                "__include__": "./conf_inc.toml",
            },
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def toml_file_inc2(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_folder = tmp_path_factory.mktemp(AnExample1Config.default_foldername())
    file_path = tmp_folder / "conf_inc1.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "section1": {
                    "field1": "f1",
                    "field2": 22,
                    "subsec": {"field3": (-33, "no")},
                },
            },
            fptr,
        )
    file_path = tmp_folder / "conf_inc2.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "field0": 333.33,
            },
            fptr,
        )
    file_path = tmp_folder / "conf_main.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {"field0": 33.33, "__include__": ["./conf_inc1.toml", "./conf_inc2.toml"]},
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def toml_file_inc3(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_folder = tmp_path_factory.mktemp(AnExample1Config.default_foldername())
    file_path = tmp_folder / "conf_inc1.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "section1": {
                    "field1": "f1",
                    "field2": 22,
                    "subsec": {"field3": (-333, "no")},
                },
            },
            fptr,
        )
    file_path = tmp_folder / "conf_inc2.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {"field0": 333.33, "__include__": "./conf_inc1.toml"},
            fptr,
        )
    file_path = tmp_folder / "conf_main.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {"field0": 33.33, "__include__": "./conf_inc2.toml"},
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def toml_file_inc4(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_folder = tmp_path_factory.mktemp(AnExample1Config.default_foldername())
    file_path = tmp_folder / "conf_main.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "field0": 33.33,
                "__include__": 'fi:\0\\l*e/p"a?t>h|.t<xt',
            },
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def toml_file_inc5(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_folder = tmp_path_factory.mktemp(AnExample1Config.default_foldername())
    file_path = tmp_folder / "conf_main.toml"
    with file_path.open(mode="w") as fptr:
        tomlkit.dump(
            {
                "field0": 33.33,
                "__include__": 14,
            },
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def json_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    file_path = tmp_path_factory.mktemp(
        AnExample1Config.default_foldername()
    ) / AnExample1Config.default_filename().replace("toml", "json")
    with file_path.open(mode="w") as fptr:
        json.dump(
            {
                "section1": {
                    "field1": "f2",
                    "field2": 33,
                    "subsec": {"field3": (-4, "maybe")},
                }
            },
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def json_file_inc2(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_folder = tmp_path_factory.mktemp(AnExample1Config.default_foldername())
    file_path = tmp_folder / "conf_inc1.json"
    with file_path.open(mode="w") as fptr:
        json.dump(
            {
                "section1": {
                    "field1": "f1",
                    "field2": 22,
                    "subsec": {"field3": (-99, "no")},
                },
            },
            fptr,
        )
    file_path = tmp_folder / "conf_inc2.json"
    with file_path.open(mode="w") as fptr:
        json.dump(
            {
                "field0": 333.33,
            },
            fptr,
        )
    file_path = tmp_folder / "conf_main.json"
    with file_path.open(mode="w") as fptr:
        json.dump(
            {"field0": 99.99, "__include__": ["./conf_inc1.json", "./conf_inc2.json"]},
            fptr,
        )
    return file_path


@pytest.fixture(scope="session")
def ini_file(tmp_path_factory: pytest.TempPathFactory) -> Path:
    file_path = tmp_path_factory.mktemp(
        AnExample1Config.default_foldername()
    ) / AnExample1Config.default_filename().replace("toml", "ini")
    with file_path.open(mode="w") as fptr:
        fptr.write("inifile")
    return file_path


def test_kind_string() -> None:
    assert AnExample1ConfigSection.kind_string() == "Config"


def test_section_singleton(caplog: pytest.LogCaptureFixture) -> None:
    use_standard_logging(enable=True)
    assert AnExample1ConfigSection.get().field1 == "field1"
    assert " accessed before data has been loaded" in caplog.records[0].msg
    logger.disable(LOGGER_NAME)


def test_paths(toml_file: Path, caplog: pytest.LogCaptureFixture) -> None:
    use_standard_logging(enable=True)
    # default_filepath:
    if the_path := Config.default_filepath():
        assert the_path.parts[-2] == ".config"
    else:
        assert False

    if the_path := AnExample1Config.default_filepath():
        assert the_path.parts[-1] == "config.toml"
        assert the_path.parts[-2] == ".an_example1"
    else:
        assert False

    # filepath:
    # if not set, then equal to default_filepath
    assert AnExample1Config.filepath() == the_path
    # check set_filepath with a Path
    AnExample1Config.set_filepath(toml_file)
    assert AnExample1Config.filepath() == toml_file
    # check set_filepath with a str
    AnExample1Config.set_filepath(".")
    assert AnExample1Config.filepath() == Path.cwd()

    # reset to default:
    AnExample1Config.set_filepath("")
    assert AnExample1Config.filepath() == the_path

    AnExample1Config.get()
    assert "will try implicit loading with" in caplog.records[0].msg

    # raising of FileNotFoundError:
    with pytest.raises(FileNotFoundError):
        AnExample1Config.load(throw_if_file_not_found=True)

    # raising in case of invalid path:
    with pytest.raises(ValueError):
        AnExample1Config.set_filepath('fi:\0\\l*e/p"a?t>h|.t<xt')
    logger.disable(LOGGER_NAME)


def test_decorator() -> None:
    # raising of TypeError:
    with pytest.raises(TypeError):
        ConfigNoDataclass.load()
    with pytest.raises(TypeError):
        ConfigUnfrozenDataclass.load()


def test_config_cmdline(monkeypatch: pytest.MonkeyPatch) -> None:
    # test without commandline arguments
    # - this works, but not together with the last 4 lines
    # monkeypatch.setattr(sys, "argv", ["bla"])
    # config_filepath_from_cli(Config, short_option="-k")
    # assert Config.filepath() == Config.default_filepath()
    some_path = Path.home() / "ProgramData" / "test" / "config.toml"
    monkeypatch.setattr(sys, "argv", ["bla", "-k", str(some_path)])
    config_filepath_from_cli(AnExample1Config, short_option="-k")
    assert str(AnExample1Config.filepath()) == str(some_path)


def test_get_defaults(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    def mock_default_filepath() -> PathOpt:
        return None

    monkeypatch.setattr(AnExample1Config, "default_filepath", mock_default_filepath)
    use_standard_logging(enable=True)
    AnExample1Config.set_filepath("", load=True)
    assert AnExample1Config.get().section1.field1 == "field1"
    assert AnExample1Config.get().section1.field2 == 2
    assert AnExample1Config.get().section1.subsec.field3[1] == "yes"
    assert "Path None not valid." in caplog.records[0].msg
    # raising of FileNotFoundError:
    with pytest.raises(FileNotFoundError):
        AnExample1Config.load(throw_if_file_not_found=True)
    logger.disable(LOGGER_NAME)
    caplog.clear()


def test_set_filepath_after_get(
    toml_file: Path, caplog: pytest.LogCaptureFixture
) -> None:
    use_standard_logging(enable=True)
    AnExample1Config.set_filepath(toml_file, load=True)
    assert AnExample1Config.get().section1.field1 == "f1"
    assert AnExample1Config.get().section1.subsec.field3[1] == "no"
    # test if the subsection singleton is properly registered
    assert AnExampleConfigSubSection.get().field3[1] == "no"
    AnExample1Config.set_filepath("", load=False)
    assert "file is not loaded into the Config." in caplog.records[0].msg
    logger.disable(LOGGER_NAME)


def test_get(monkeypatch: pytest.MonkeyPatch, toml_file: Path) -> None:
    AnExample1Config.set_filepath(toml_file)
    AnExample1Config.load()
    assert AnExample1Config.get().field0 == 33.33
    assert AnExample1Config.get().section1.field1 == "f1"
    assert AnExample1Config.get().section1.field2 == 22

    # test that by default it is not reloaded
    def mock_tomlkit_load(
        fptr: Any,  # pylint: disable=unused-argument
    ) -> dict[str, dict[str, Any]]:
        return {"section1": {"field1": "f1", "field2": 222}}

    monkeypatch.setattr(tomlkit, "load", mock_tomlkit_load)
    assert AnExample1Config.get().section1.field2 == 22

    # and now test reload
    AnExample1Config.load()
    assert AnExample1Config.get().field0 == 2.2
    assert AnExample1Config.get().section1.field2 == 222


def test_get_json(json_file: Path) -> None:
    AnExample1Config.set_filepath(json_file)
    AnExample1Config.load()
    assert AnExample1Config.get().section1.field1 == "f2"
    assert AnExample1Config.get().section1.field2 == 33


def test_get_ini(ini_file: Path, caplog: pytest.LogCaptureFixture) -> None:
    use_standard_logging(enable=True)
    AnExample1Config.set_filepath(ini_file)
    AnExample1Config.load()
    assert AnExample1Config.get().section1.field1 == "field1"
    assert AnExample1Config.get().section1.field2 == 2
    assert "Unknown file format ini given in" in caplog.records[-2].msg
    logger.disable(LOGGER_NAME)


def test_type_coercion() -> None:
    AnExample1Config.set({"section1": {"field2": "22"}})
    test_config = AnExample1Config.get()
    assert isinstance(test_config.section1.field2, int)
    assert test_config.section1.field2 == 22


def test_wrong_type() -> None:
    with pytest.raises(ValidationError) as excinfo:
        AnExample1Config.set({"section1": {"field1": ("f1", 22), "field2": None}})
    assert "2 validation errors" in str(excinfo.value)
    assert "Input should be a valid string" in str(excinfo.value)
    assert "Input should be a valid integer" in str(excinfo.value)


def test_missing_extra_attributes() -> None:
    AnExample1Config.set({"section1": {"field1": "f1", "field3": 22}})
    test_config = AnExample1Config.get()
    assert test_config.section1.field2 == 2
    with pytest.raises(AttributeError):
        assert test_config.section1.field3 == 22  # type: ignore[attr-defined]


@dataclass(frozen=True)
class Example2aConfigSection(ConfigSectionBase):
    """Example 2a of a Config section"""

    field3: float
    field4: float = 0.5


@dataclass(frozen=True)
class Example2bConfigSection(ConfigSectionBase):
    """Example 2b of a Config section"""

    field1: str = "field1"
    field2: int = 2


@dataclass(frozen=True)
class Example2Config(ConfigBase):
    """Example Config"""

    section1: Example2aConfigSection
    section2: Example2bConfigSection = Example2bConfigSection()


def test_attributes_no_default() -> None:
    init_values = {
        "field0": 33.33,
        "section1": {
            "field1": "f1",
            "field2": 22,
            "subsec": {"field3": (-3, "no")},
        },
    }
    # field3 is a float and has no default value
    with pytest.raises(ValidationError):
        Example2Config.set(init_values)

    Example2Config.set({"section1": {"field3": 1.1}})
    test_config = Example2Config.get()
    assert test_config.section1.field3 == 1.1
    assert test_config.section1.field4 == 0.5
    assert test_config.section2.field1 == "field1"


def test_include_1(toml_file_inc1: Path) -> None:
    AnExample1Config.set_filepath(toml_file_inc1, load=True)
    assert AnExample1Config.get().section1.field1 == "f1"
    assert AnExample1Config.get().section1.subsec.field3[1] == "no"


def test_include_2(toml_file_inc2: Path) -> None:
    AnExample1Config.set_filepath(toml_file_inc2, load=True)
    assert AnExample1Config.get().field0 == 33.33
    assert AnExample1Config.get().section1.subsec.field3[0] == -33


def test_include_3(toml_file_inc3: Path) -> None:
    AnExample1Config.set_filepath(toml_file_inc3, load=True)
    assert AnExample1Config.get().section1.subsec.field3[0] == -333


def test_include_4(toml_file_inc4: Path) -> None:
    # raising in case of invalid path:
    with pytest.raises(ValueError):
        AnExample1Config.set_filepath(toml_file_inc4, load=True)


def test_include_5(toml_file_inc5: Path) -> None:
    # raising in case of invalid path:
    with pytest.raises(ValueError):
        AnExample1Config.set_filepath(toml_file_inc5, load=True)


def test_include_6(json_file_inc2: Path) -> None:
    AnExample1Config.set_filepath(json_file_inc2, load=True)
    assert AnExample1Config.get().field0 == 99.99
    assert AnExample1Config.get().section1.subsec.field3[0] == -99
