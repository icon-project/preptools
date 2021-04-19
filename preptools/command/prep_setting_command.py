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

from iconsdk.utils.convert_type import convert_int_to_hex_str
from preptools.core.prep import create_writer_by_args
from preptools.exception import InvalidFormatException, InvalidFileReadException
from preptools.utils import str_to_int
from preptools.utils.constants import fields_to_validate
from preptools.utils.validation_checker import (
    validate_prep_data,
    validate_field_in_prep_data
)


def init(sub_parser, common_parent_parser):
    tx_parent_parser = create_tx_parser()

    _init_for_register_prep(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_unregister_prep(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_set_prep(sub_parser, common_parent_parser, tx_parent_parser)
    _init_for_set_governance_variables(sub_parser, common_parent_parser, tx_parent_parser)


def _init_for_register_prep(sub_parser, common_parent_parser, tx_parent_parser):
    name = "registerPRep"
    desc = f"Register P-Rep"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        nargs="?",
        help="P-Rep name"
    )

    parser.add_argument(
        "--country",
        type=str,
        required=False,
        help="P-Rep's country"
    )

    parser.add_argument(
        "--city",
        type=str,
        required=False,
        help="P-Rep's city"
    )

    parser.add_argument(
        "--email",
        type=str,
        required=False,
        help="P-Rep's email"
    )

    parser.add_argument(
        "--website",
        type=str,
        required=False,
        help="P-Rep's homepage url"
    )

    parser.add_argument(
        "--details",
        type=str,
        required=False,
        help="json url including P-Rep detailed information"
    )

    parser.add_argument(
        "--p2p-endpoint",
        type=str,
        required=False,
        dest="p2pEndpoint",
        help="Network info used for connecting among P-Rep nodes"
    )

    parser.add_argument(
        "--node-address",
        type=str,
        required=False,
        dest="nodeAddress",
        help="PRep Node Key"
    )

    parser.add_argument(
        "--prep-json",
        type=str,
        required=False,
        nargs="?",
        help="json file having P-Rep information"
    )

    parser.set_defaults(func=_register_prep)


def _register_prep(args) -> str:
    writer = create_writer_by_args(args)

    if args.prep_json:
        params = _get_prep_json(args, blank_able=True)

    else:
        params = {}
        _get_prep_input(args, params)

    _get_prep_dict_from_cli(params)
    response = writer.register_prep(params)

    if response:
        return f'txHash : {response}'


def _get_prep_dict_from_cli(params, set_prep: bool = False):

    for field in fields_to_validate:

        while True:
            if params.get(field, None) is None:  # param is not found.

                cmd_input = input(f" > {field} : ")

                if len(cmd_input.strip()) > 0:  # field's value size > 0
                    try:
                        validate_field_in_prep_data(field, cmd_input)
                        params[field] = cmd_input
                        break

                    except InvalidFormatException as e:
                        print(e)

                elif set_prep:  # in case of set_prep, don't have to get all params.
                    break

                else:  # in case of register, it must have input.
                    print(f"please enter {field}.")

            else:
                break


def _get_prep_json(args, blank_able: bool = False):
    path = args.prep_json

    try:
        with open(path) as register:
            params = json.load(register)
            _get_prep_input(args, params)

    except (FileNotFoundError, IsADirectoryError):
        raise InvalidFileReadException(f"Cannot find json file, file path : {path}")

    validate_prep_data(params, blank_able)

    return params


def _get_prep_input(args, params: dict):
    for key in fields_to_validate:
        if hasattr(args, key) and getattr(args, key) is not None:
            params[key] = getattr(args, key)


def _init_for_unregister_prep(sub_parser, common_parent_parser, tx_parent_parser):
    name = "unregisterPRep"
    desc = f"Unregister P-Rep\nWARNING!! Unregistering P-Rep does not return the registration fee"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.set_defaults(func=_unregister_prep)


def _unregister_prep(args) -> str:

    writer = create_writer_by_args(args)
    response = writer.unregister_prep()

    if response:
        return f'txHash : {response}'


def _init_for_set_prep(sub_parser, common_parent_parser, tx_parent_parser):
    name = "setPRep"
    desc = f"Change enrolled P-Rep information"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "-i", "--interactive",
        help="Activate interactive mode when prep fields are blank.",
        action='store_true'
    )

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="PRep name"
    )

    parser.add_argument(
        "--country",
        type=str,
        required=False,
        help="P-Rep's country"
    )

    parser.add_argument(
        "--city",
        type=str,
        required=False,
        help="P-Rep's city"
    )

    parser.add_argument(
        "--email",
        type=str,
        required=False,
        help="P-Rep's email"
    )

    parser.add_argument(
        "--website",
        type=str,
        required=False,
        help="P-Rep's homepage url"
    )

    parser.add_argument(
        "--details",
        type=str,
        required=False,
        help="json url including P-Rep details information"
    )

    parser.add_argument(
        "--p2p-endpoint",
        type=str,
        required=False,
        dest="p2pEndpoint",
        help="Network info used for connecting among P-Rep nodes"
    )

    parser.add_argument(
        "--node-address",
        type=str,
        required=False,
        dest="nodeAddress",
        help="PRep Node Key"
    )

    parser.add_argument(
        "--prep-json",
        type=str,
        required=False,
        help="json file including P-Rep information"
    )

    parser.set_defaults(func=_set_prep)


def _set_prep(args) -> str:

    writer = create_writer_by_args(args)

    if args.prep_json:
        params = _get_prep_json(args, blank_able=True)

    else:
        params = dict()
        _get_prep_input(args, params)

    if args.interactive:
        _get_prep_dict_from_cli(params, set_prep=True)

    response = writer.set_prep(params)

    if response:
        return f'txHash : {response}'


def _init_for_set_governance_variables(sub_parser, common_parent_parser, tx_parent_parser):
    name = "setGovernanceVariables"
    desc = f"Change Governance variables used in network operation" \
           f"\ndeprecated.since revision9, set i-rep with network proposal"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "--irep",
        type=int,
        required=True,
        help="amounts of irep"
    )

    parser.set_defaults(func=_set_governance_variables)


def _set_governance_variables(args) -> str:
    params = {
        'irep': convert_int_to_hex_str(args.irep)
    }

    writer = create_writer_by_args(args)
    response = writer.set_governance_variables(params)

    if response:
        return f'txHash : {response}'


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
