from argparse import (
    ArgumentParser,
    Namespace,
)

from .command import Command


class TextCommand(Command):
    def __init__(self):
        self._name = "text"
        self._help = f"{self._name} network proposal"

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        parser.add_argument("text", type=str)
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        value = {"text": args.text}
        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)
        return proposal
