# -*- coding: utf-8 -*-

# Copyright 2019 ICON Foundation
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

import argparse
import json
from enum import IntEnum
from typing import Any, Dict

from iconsdk.utils.convert_type import convert_bytes_to_hex_str, convert_int_to_hex_str
from iconsdk.utils.typing.conversion import object_to_str

from preptools.core.prep import create_writer_by_args
from preptools.exception import InvalidArgumentException
from preptools.utils import str_to_int
from preptools.utils.constants import proposal_param_by_type
from preptools.utils.utils import print_proposal_value
from preptools.utils.validation_checker import valid_proposal_param_by_type
from ..core.network_proposal import validate_network_proposal


class ProposalType(IntEnum):
    Text = 0
    Revision = 1
    MaliciousScore = 2
    PRepDisqualification = 3
    StepPrice = 4
    IRep = 5
    StepCosts = 6
    RewardFundSetting = 7
    RewardFundAllocation = 8

    Last = 8


def init(sub_parser, common_parent_parser):
    tx_parent_parser = create_tx_parser()

    _init_for_register_proposal(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_cancel_proposal(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_vote_proposal(sub_parser, common_parent_parser, tx_parent_parser)


def _init_for_register_proposal(sub_parser, common_parent_parser, tx_parent_parser):
    name = "registerProposal"
    desc = f"Register Proposal"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

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

    _add_type_argument(parser)

    parser.add_argument(
        "--value-value",
        type=str,
        help="type 0:text message, "
             "type 4:step price in loop"
             "type 5:irep in loop (required when type 0, 4 or 5)"
    )

    parser.add_argument(
        "--value-code",
        type=int,
        help="revision code (required when type 1)"
    )

    parser.add_argument(
        "--value-name",
        type=str,
        help="icon-service version (required when type 1)"
    )

    parser.add_argument(
        "--value-address",
        type=str,
        help="type 2: address of SCORE, "
             "type 3: address of main/sub P-Rep (required when type 2 or 3)"
    )

    parser.add_argument(
        "--value-type",
        type=int,
        help="0 : freeze, 1 : unfreeze (required when type 2)"
    )

    parser.add_argument(
        "--value-costs",
        type=str,
        nargs="+",
        help="step cost configuration. COST_TYPE,VALUE"
    )

    parser.add_argument(
        "--value-iglobal",
        type=int,
        help="iglobal value"
    )

    parser.add_argument(
        "--value-rewardFunds",
        type=str,
        nargs="+",
        help="reward fund allocation configuration. REWARD_TYPE,VALUE."
             "All REWARD_TYPE must be specified."
    )

    parser.add_argument(
        "--raw",
        type=str,
        metavar="JSON string",
        nargs="?",
        required=False,
        default=None,
        help=(
            'raw data for network proposal in json format. '
            'int and bool types can be changed to hexa strings automatically '
            'ex) \'{"code":10,"name":"1.9.1"}\''
        )
    )

    parser.set_defaults(func=_register_proposal)


def _add_type_argument(parser: argparse.ArgumentParser):
    types = (f"{p_type}-{p_type.name}" for p_type in ProposalType)
    parser.add_argument(
        "--type",
        type=int,
        required=True,
        help=f"Proposal type [{', '.join(types)}]"
    )


def _register_proposal(args) -> dict:
    value: Dict[str, Any] = _get_proposal_value(args)
    params = {
        "title": args.title,
        "description": args.desc,
        "type": convert_int_to_hex_str(args.type),
        "value": _convert_value_to_hex_str(value),
    }

    writer = create_writer_by_args(args)
    if not args.yes or args.verbose:
        print_proposal_value(value)
    response = writer.register_proposal(params)

    return response


def _get_proposal_value(args: argparse.Namespace) -> Dict[str, Any]:
    if args.raw is None:
        return _get_value_by_type(args)
    else:
        return _get_value_from_raw(args.raw)


def _get_value_by_type(args) -> Dict[str, Any]:
    if valid_proposal_param_by_type[args.type](args):
        return _make_dict_with_args(proposal_param_by_type[args.type], args)

    raise InvalidArgumentException(f"Type should be between {ProposalType.Text} ~ {ProposalType.Last}")


def _get_value_from_raw(proposal_type: ProposalType, raw: str) -> Dict[str, Any]:
    try:
        o = json.loads(raw)
        validate_network_proposal(proposal_type, o)
        return object_to_str(o)
    except:
        raise InvalidArgumentException(f"Invalid json format: {raw}")


def _make_dict_with_args(param_list, args) -> dict:
    value = {}
    prefix = 'value_'

    for key in param_list:
        key_str = key[len(prefix):]
        value[key_str] = getattr(args, key)

    return object_to_str(value)


def _init_for_cancel_proposal(sub_parser, common_parent_parser, tx_parent_parser):
    name = "cancelProposal"
    desc = f"Cancel Proposal"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "--id",
        type=str,
        required=True,
        nargs="?",
        help="hash of registerProposal TX"
    )

    parser.set_defaults(func=_cancel_proposal)


def _cancel_proposal(args) -> dict:
    params = {
        "id": args.id
    }

    writer = create_writer_by_args(args)
    response = writer.cancel_proposal(params)

    return response


def _init_for_vote_proposal(sub_parser, common_parent_parser, tx_parent_parser):
    name = "voteProposal"
    desc = f"Vote Proposal"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "--id",
        type=str,
        required=True,
        help="hash of registerProposal TX"
    )

    parser.add_argument(
        "--vote",
        type=int,
        required=True,
        help="0 : disagree, 1 : agree"
    )

    parser.set_defaults(func=_vote_proposal)


def _vote_proposal(args) -> dict:
    params = {
        "id": args.id,
        "vote": args.vote
    }

    writer = create_writer_by_args(args)
    response = writer.vote_proposal(params)

    return response


def create_tx_parser() -> argparse.ArgumentParser:
    """Common options for invoke commands

    :return:
    """

    parent_parser = argparse.ArgumentParser(add_help=False)

    parent_parser.add_argument(
        "--password", "-p",
        type=str,
        required=False,
        default=None,
        help="keystore password"
    )

    parent_parser.add_argument(
        "--keystore", "-k",
        type=str,
        required=False,
        help="keystore file path"
    )

    parent_parser.add_argument(
        "--step-limit", "-s",
        type=str_to_int,
        required=False,
        default=None,
        dest="step_limit",
        help="step limit to set"
    )

    parent_parser.add_argument(
        "--step-margin", "-m",
        type=str_to_int,
        required=False,
        default="0",
        dest="step_margin",
        help="Can be used when step-limit option is not given.\n"
             "Set step-limit value to estimated Step + this value(step-margin)"
    )

    return parent_parser


def _convert_value_to_hex_str(value: Dict[str, Any]) -> str:
    return convert_bytes_to_hex_str(json.dumps(value, separators=(",", ":")).encode())
