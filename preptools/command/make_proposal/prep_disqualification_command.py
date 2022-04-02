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
from ...utils.validation_checker import is_valid_address


class PRepDisqualificationCommand(Command):
    def __init__(self):
        self._name = "prepDisqualification"
        self._help = f"{self._name} network proposal"

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        parser.add_argument("address", type=str, help="prep address to disqualify")
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        self._validate(args)
        value = {"address": args.address}
        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)
        return proposal

    @staticmethod
    def _validate(args: Namespace):
        address: str = args.address
        if not is_valid_address(address):
            raise InvalidArgumentException(f"Invalid address: {args.address}")
        if address.startswith("cx"):
            raise InvalidArgumentException(f"Score address not allowed")
