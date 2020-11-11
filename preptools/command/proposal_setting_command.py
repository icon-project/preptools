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

import json
import argparse

from iconsdk.utils.convert_type import convert_bytes_to_hex_str, convert_int_to_hex_str, convert_params_value_to_hex_str
from preptools.core.prep import create_writer_by_args
from preptools.exception import InvalidArgumentException
from preptools.utils import str_to_int
from preptools.utils.constants import proposal_param_by_type
from preptools.utils.utils import print_proposal_value
from preptools.utils.validation_checker import valid_proposal_param_by_type


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

    parser.add_argument(
        "--type",
        type=int,
        required=True,
        help="type of Proposal"
    )

    parser.add_argument(
        "--value-value",
        type=str,
        help="type 0:text message, "
             "type 4:step price in loop (required when type 0 or 4)"
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

    parser.set_defaults(func=_register_proposal)


def _register_proposal(args) -> dict:

    params = {
        "title": args.title,
        "description": args.desc,
        "type": convert_int_to_hex_str(int(args.type)),
        "value": None
    }

    value = _get_value_by_type(args)
    params['value'] = _convert_value_to_hex_str(value)

    writer = create_writer_by_args(args)
    if not args.yes or args.verbose:
        print_proposal_value(value)
    response = writer.register_proposal(params)

    return response


def _get_value_by_type(args) -> dict:

    if valid_proposal_param_by_type[args.type](args):
        return _make_dict_with_args(proposal_param_by_type[args.type], args)

    raise InvalidArgumentException("Type should be between 0 ~ 4")


def _make_dict_with_args(param_list, args) -> dict:
    value = dict()
    prefix = 'value_'

    for key in param_list:
        if key.startswith(prefix):
            key_str = key[len(prefix):]
        else:
            return None

        value[key_str] = getattr(args, key)

    return convert_params_value_to_hex_str(value)


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
        dest="step_limit",
        help="step limit to set"
    )

    return parent_parser


def _convert_value_to_hex_str(value: dict) -> str:
    return convert_bytes_to_hex_str(json.dumps(value).encode())
