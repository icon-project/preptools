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

from ..exception import InvalidArgumentException
from ..utils.argparse_utils import FileReadAction


def init(sub_parsers, common_parent_parser: ArgumentParser):
    cmd = RegisterProposal2Command()
    cmd.init(sub_parsers, common_parent_parser)


class RegisterProposal2Command:
    def __init__(self):
        self._name = "registerProposal2"
        self._desc = "Register new formatted proposals supported by governance2 score"

    def init(self, sub_parsers, common_parent_parser: ArgumentParser):
        parser: ArgumentParser = sub_parsers.add_parser(
            self._name,
            parents=(common_parent_parser,),
            help=self._desc
        )

        parser.add_argument(
            "proposals",
            type=str,
            nargs="+",
            action=FileReadAction,
            help=(
                "proposal contents in governance2 score format "
                "or filepath with '@' prefix, which includes proposal contents"
            ),
        )
        parser.set_defaults(func=self._run)

    @classmethod
    def _make_params(cls, args: Namespace) -> List[Dict[str, str]]:
        params: List[Dict[str, str]] = []
        proposals: List[str] = args.proposals

        for proposal in proposals:
            if proposal.startswith("@"):
                # filepath including a proposal content
                path = proposal
                with open(path, "rt") as f:
                    proposal = f.read()

            param: Union[Dict[str, str], List[Dict[str, str]]] = json.loads(proposal)
            if isinstance(param, list):
                params += param
            elif isinstance(param, dict):
                params.append(param)
            else:
                raise InvalidArgumentException(f"Unsupported proposal format: {param}")

        return params

    def _run(self, args: Namespace) -> Dict[str, Any]:
        params: List[Dict[str, str]] = self._make_params(args)

        if not args.yes or args.verbose:
            print(json.dumps(params, indent=4))

        return {"params": params}
        # writer = create_writer_by_args(args)
        # response = writer.register_proposal(params, value=NETWORK_PROPOSAL_FEE)
        # return response
