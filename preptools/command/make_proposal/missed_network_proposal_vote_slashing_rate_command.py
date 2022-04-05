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

from .command import Command
from ...exception import InvalidArgumentException
from ...utils import str_to_int


class MissedNetworkProposalVoteSlashingRateCommand(Command):
    def __init__(self):
        self._name = "missedNetworkProposalVoteSlashingRate"
        self._help = f"{self._name} network proposal"

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        parser.add_argument(
            "slashingRate",
            type=str_to_int,
            help="slashing rate in percent [0 ~ 100]"
        )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        self._validate(args)
        value = {"slashingRate": args.slashingRate}
        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)
        return proposal

    @staticmethod
    def _validate(args: Namespace):
        if not (0 <= args.slashingRate <= 100):
            raise InvalidArgumentException(f"Invalid slashingRate: {args.slashingRate}")
