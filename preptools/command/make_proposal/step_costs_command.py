# Copyright 2022 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from argparse import (
    ArgumentParser,
    Namespace,
)
from typing import Optional

from .command import Command
from ...utils import str_to_int


class StepCostsCommand(Command):
    _options = (
        "default",
        "contract-call",
        "contract-create",
        "contract-update",
        "contract-set",
        "get",
        "get-base",
        "set",
        "set-base",
        "delete",
        "delete-base",
        "input",
        "log",
        "log-base",
        "api-call",
    )

    def __init__(self):
        self._name = "stepCosts"
        self._help = f"{self._name} network proposal"

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        self._init_arguments(parser)

    def _init_arguments(self, parser: ArgumentParser):
        for option in self._options:
            parser.add_argument(
                f"--{option}",
                dest=_to_lower_camel_case(option, "-"),
                type=str_to_int,
                required=False,
            )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        costs = {}

        for option in self._options:
            option = _to_lower_camel_case(option, "-")
            cost: Optional[int] = getattr(args, option)
            if cost is not None:
                costs[option] = cost

        proposal: str = self._make_proposal(self._name, value={"costs": costs})
        self._write_proposal(args.output, proposal)
        return proposal


def _to_lower_camel_case(value: str, sep: str = "-") -> str:
    tokens = value.split(sep)
    for i in range(1, len(tokens)):
        tokens[i] = tokens[i].title()

    return "".join(tokens)
