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


class NetworkScoreDesignationCommand(Command):
    def __init__(self):
        self._name = "networkScoreDesignation"
        self._help = f"{self._name} network proposal"
        self._roles = ("cps", "relay")

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )

        for role in self._roles:
            parser.add_argument(
                f"--{role}",
                type=str,
                required=False,
                help=f"network score address for {role}",
            )
            parser.set_defaults(func=self._run)

    def _run(self, args: Namespace):
        print(args)
        network_scores = []
        for role in self._roles:
            address: Optional[str] = getattr(args, role)
            if isinstance(address, str):
                network_scores.append({"role": role, "address": address})

        value = {"networkScores": network_scores}
        ret = make_proposal(self._name, value)
        print(ret)
