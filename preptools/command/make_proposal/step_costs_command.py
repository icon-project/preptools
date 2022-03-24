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
from .utils import make_proposal


class StepCostsCommand(Command):
    _options = (
        "schema",
        "default",
        "contractCall",
        "contractCreate",
        "contractUpdate",
        "contractSet",
        "get",
        "getBase",
        "set",
        "setBase",
        "delete",
        "deleteBase",
        "input",
        "log",
        "logBase",
        "apiCall",
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
                type=int,
                required=False,
            )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace):
        value = {}
        for option in self._options:
            cost: Optional[int] = getattr(args, option)
            if cost is not None:
                value[option] = cost

        ret = make_proposal(self._name, value)
        print(ret)
