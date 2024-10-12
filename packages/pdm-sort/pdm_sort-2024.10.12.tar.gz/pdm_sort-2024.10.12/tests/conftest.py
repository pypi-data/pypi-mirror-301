from collections.abc import Iterable
from pathlib import Path

import pytest
from pdm.core import Core
from pytest import FixtureRequest

from pdm_sort import setup_pdm_sort

pytest_plugins = "pdm.pytest"


@pytest.fixture
def core(core: Core) -> Core:
    setup_pdm_sort(core)
    return core


@pytest.fixture
def repository_pypi_json() -> Path:
    return Path(__file__).parent / "fixtures" / "pypi.json"


@pytest.fixture(params=(False, True))
def dev_option(request: FixtureRequest) -> Iterable[str]:
    return ("--dev",) if request.param else ()


@pytest.fixture(params=(False, True))
def no_sort_option(request: FixtureRequest) -> Iterable[str]:
    return ("--no-sort",) if not request.param else ()
