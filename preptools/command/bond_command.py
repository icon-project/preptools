# -*- coding: utf-8 -*-

# Copyright 2021 ICON Foundation
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

from preptools.command.prep_setting_command import create_tx_parser
from preptools.core.prep import create_writer_by_args, create_reader_by_args


def init(sub_parser, common_parent_parser):
    tx_parent_parser = create_tx_parser()

    _init_for_set_stake(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_get_stake(sub_parser, common_parent_parser)

    _init_for_set_bond(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_get_bond(sub_parser, common_parent_parser)

    _init_for_set_bonder_list(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_get_bonder_list(sub_parser, common_parent_parser)


def _init_for_set_stake(sub_parser, common_parent_parser, tx_parent_parse):
    name = "setStake"
    desc = f"Set stake value"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parse],
        help=desc)

    parser.add_argument(
        "value",
        type=int,
        help="Stake value"
    )

    parser.set_defaults(func=_set_stake)


def _set_stake(args) -> str:
    params = {
        'value': args.value,
    }

    writer = create_writer_by_args(args)
    return writer.set_stake(params)


def _init_for_get_stake(sub_parser, common_parent_parser):
    name = "getStake"
    desc = f"Get stake value"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "address",
        type=str,
        help="Address of you are looking for"
    )

    parser.set_defaults(func=_get_stake)


def _get_stake(args):
    reader = create_reader_by_args(args)
    response = reader.get_stake(args.address)

    return response


def _init_for_set_bond(sub_parser, common_parent_parser, tx_parent_parse):
    name = "setBond"
    desc = f"Set bond configuration"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parse],
        help=desc)

    parser.add_argument(
        "bond",
        type=str,
        nargs="+",
        help="Bond configurations. PREP_ADDRESS,VALUE (Max: 100)"
    )

    parser.set_defaults(func=_set_bond)


def _set_bond(args) -> str:
    bonder_list = args.bond
    bonds = []
    for bond in bonder_list:
        token = bond.split(",")
        bonds.append({"address": token[0], "value": hex(int(token[1], 0))})

    params = {
        "bonds": bonds
    }

    writer = create_writer_by_args(args)
    return writer.set_bond(params)


def _init_for_get_bond(sub_parser, common_parent_parser):
    name = "getBond"
    desc = f"Get bond configuration"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "address",
        type=str,
        help="Address of you are looking for"
    )

    parser.set_defaults(func=_get_bond)


def _get_bond(args):
    reader = create_reader_by_args(args)
    response = reader.get_bond(args.address)

    return response


def _init_for_set_bonder_list(sub_parser, common_parent_parser, tx_parent_parser):
    name = "setBonderList"
    desc = f"Set allowed bonder list of P-Rep"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "--bonder-list",
        type=str,
        required=True,
        dest="bonderList",
        help="list of address. separator is ','"
    )

    parser.set_defaults(func=_set_bonder_list)


def _set_bonder_list(args) -> str:
    bonder_str: str = args.bonderList
    bonder_list = bonder_str.split(',')
    params = {
        'bonderList': bonder_list
    }

    writer = create_writer_by_args(args)
    return writer.set_bonder_list(params)


def _init_for_get_bonder_list(sub_parser, common_parent_parser):
    name = "getBonderList"
    desc = f"Get allowed bonder list of P-Rep"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "address",
        type=str,
        help="Address of P-Rep you are looking for"
    )

    parser.set_defaults(func=_get_bonder_list)


def _get_bonder_list(args):
    address = args.address

    reader = create_reader_by_args(args)
    response = reader.get_bonder_list(address)

    return response
