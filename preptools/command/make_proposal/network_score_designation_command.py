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
import sys
from argparse import (
    ArgumentParser,
    Namespace,
)
from typing import Optional

from .command import Command
from ...exception import InvalidArgumentException
from ...utils.validation_checker import is_valid_address


class NetworkScoreDesignationCommand(Command):
    def __init__(self):
        self._name = "networkScoreDesignation"
        self._help = f"{self._name} network proposal"
        self._roles = ("cps", "relay")
        self._parser: Optional[ArgumentParser] = None

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
                metavar="scoreAddress",
                help=f"network score address for {role}",
            )
            parser.set_defaults(func=self._run)

        self._parser = parser

    def _run(self, args: Namespace) -> Optional[str]:
        network_scores = []
        for role in self._roles:
            address: Optional[str] = getattr(args, role)
            if address is None:
                continue
            if is_valid_address(address):
                network_scores.append({"role": role, "address": address})
            else:
                raise InvalidArgumentException(f"Invalid address: {address}")

        if len(network_scores) == 0:
            self._parser.print_help(sys.stderr)
            return

        value = {"networkScores": network_scores}
        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)
        return proposal
