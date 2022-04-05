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
from ...utils.argparse_utils import FileReadHexAction


class NetworkScoreUpdateCommand(Command):
    def __init__(self):
        self._name = "networkScoreUpdate"
        self._help = f"{self._name} network proposal"

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        parser.add_argument(
            "address",
            type=str,
            help="The address of network score to update"
        )
        parser.add_argument(
            "content",
            type=str,
            action=FileReadHexAction,
            nargs="?",
            help=(
                "jar file contents in hexadecimal or filepath with @ prefix. "
                "python score is not supported. "
                "[0xa23de..., or @./a/b/c/score.jar]"
            )
        )
        parser.add_argument(
            "--params",
            type=str,
            nargs="+",
            required=False,
            help="Arguments used to update a networkScore\nex) hello 100 hx1234....",
        )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        value = {
            "address": args.address,
            "content": args.content,
        }
        if isinstance(args.params, list) and len(args.params) > 0:
            value["params"] = args.params

        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)
        return proposal
