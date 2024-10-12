from argparse import ArgumentParser, Namespace

from pdm.cli.commands import add
from pdm.project import Project


class Command(add.Command):
    def add_arguments(self, parser: ArgumentParser) -> None:
        super().add_arguments(parser)
        parser.add_argument(
            "--no-sort",
            dest="sort",
            default=True,
            action="store_false",
            help="Do not sort packages",
        )

    def handle(self, project: Project, options: Namespace) -> None:
        if options.sort:
            options.packages = sorted(options.packages)
        super().handle(project, options)
