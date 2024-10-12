from pdm.core import Core

from pdm_sort.cli.commands import add


def setup_pdm_sort(core: Core) -> None:
    core.register_command(add.Command, "add")
