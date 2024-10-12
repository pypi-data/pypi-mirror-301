from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from pdm.project import Project
from pdm.pytest import MockWorkingSet

if TYPE_CHECKING:
    from pdm.pytest import PDMCallable


def test_add_command(
    project: Project,
    working_set: MockWorkingSet,
    dev_option: Iterable[str],
    no_sort_option: Iterable[str],
    pdm: PDMCallable,
) -> None:
    pdm(
        ["add", *dev_option, *no_sort_option, "click", "bcrypt", "aiohttp"], obj=project
    )
    group = (
        project.pyproject.settings["dev-dependencies"]["dev"]  # type: ignore[index]
        if dev_option
        else project.pyproject.metadata["dependencies"]
    )
    if no_sort_option:
        expected = [
            "click>=8.1.7",
            "bcrypt>=4.2.0",
            "aiohttp>=3.10.10",
        ]
    else:
        expected = [
            "aiohttp>=3.10.10",
            "bcrypt>=4.2.0",
            "click>=8.1.7",
        ]
    assert group.value == expected
