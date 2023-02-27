# Copyright 2023 ICON Foundation
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
from typing import List, Dict

from .command import Command
from ...exception import InvalidArgumentException
from ...utils.validation_checker import is_valid_address


class CallMethod(Command):
    def __init__(self):
        self._name = "call"
        self._help = f"{self._name} network proposal"

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        parser.add_argument(
            "to",
            type=str,
            help="SCORE address"
        )
        parser.add_argument(
            "method",
            type=str,
            help="method name to call"
        )
        parser.add_argument(
            "--params",
            type=str,
            nargs="+",
            required=False,
            help="Arguments information that pass to method(type and value. separate with comma)"
                 "\nex) str,hello Address,hx1234.. ",
        )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        self._validate(args)
        value = {"to": args.to, "method": args.method}
        if args.params:
            value["params"] = self.convert_params(args.params)
        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)
        return proposal

    @staticmethod
    def _validate(args: Namespace):
        if "method" not in args:
            raise InvalidArgumentException(f"method required.")
        if not is_valid_address(args.to):
            raise InvalidArgumentException(f"Invalid address: {args.to}")

    @staticmethod
    def convert_params(params: List[str]) -> List[Dict[str,str]]:
        new_params = []
        for p in params:
            if "," not in p:
                raise InvalidArgumentException("invalid arguments information format. comma required")
            t, v = p.split(",")
            new_params.append({"type": t, "value": v})
        return new_params
