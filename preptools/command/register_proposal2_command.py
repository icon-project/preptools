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
import json
from argparse import ArgumentParser, Namespace
from typing import (
    Any,
    Dict,
    List,
    Union,
)

from iconsdk.utils.typing.conversion import object_to_str
from .utils import create_tx_parser
from ..core.prep import create_writer_by_args
from ..exception import InvalidArgumentException
from ..utils.argparse_utils import FileReadAction
from ..utils.constants import NETWORK_PROPOSAL_FEE


def init(sub_parsers, common_parent_parser: ArgumentParser):
    tx_parent_parser = create_tx_parser()
    cmd = RegisterProposal2Command()
    cmd.init(sub_parsers, common_parent_parser, tx_parent_parser)


class RegisterProposal2Command:
    def __init__(self):
        self._name = "registerProposal2"
        self._desc = (
            "Register network proposals in a new format supported by governance2 score\n"
            "CAUTION: a proposer will be charged a fee of 100 ICX to submit proposals every transaction"
        )

    def init(self, sub_parsers, *parent_parsers):
        parser: ArgumentParser = sub_parsers.add_parser(
            self._name,
            parents=parent_parsers,
            help=self._desc
        )

        parser.add_argument(
            "--title",
            type=str,
            required=True,
            help="Proposal title"
        )
        parser.add_argument(
            "--desc",
            type=str,
            required=True,
            help="Proposal description"
        )
        parser.add_argument(
            "--proposals",
            type=str,
            nargs="+",
            required=True,
            action=FileReadAction,
            help=(
                "Proposal contents in governance2 score format "
                "or filepath with '@' prefix, which includes proposal contents"
            ),
        )
        parser.set_defaults(func=self._run)

    @classmethod
    def _merge_proposals(cls, args: Namespace) -> List[Dict[str, str]]:
        """Merge proposals from arguments
        """
        ret: List[Dict[str, Any]] = []
        proposals: List[str] = args.proposals

        for proposal in proposals:
            param: Union[Dict[str, Any], List[Dict[str, Any]]] = json.loads(proposal)
            if isinstance(param, list):
                ret += param
            elif isinstance(param, dict):
                ret.append(param)
            else:
                raise InvalidArgumentException(f"Unsupported proposal format: {param}")

        # convert all values in list to str recursively
        return object_to_str(ret)

    def _run(self, args: Namespace) -> Dict[str, Any]:
        proposals: List[Dict[str, str]] = self._merge_proposals(args)
        value: str = f"0x{json.dumps(proposals, separators=(',', ':')).encode('utf-8').hex()}"

        if not args.yes or args.verbose:
            print(json.dumps(proposals, indent=4))

        params = {
            "title": args.title,
            "description": args.desc,
            "value": value,
        }
        writer = create_writer_by_args(args)
        response = writer.register_proposal(params, value=NETWORK_PROPOSAL_FEE)
        return response
