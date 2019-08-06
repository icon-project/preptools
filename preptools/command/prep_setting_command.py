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
import sys

from preptools.exception import InvalidFormatException

from preptools.core.prep import create_writer_by_args
from preptools.utils.format_checker import (
    validate_prep_data
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
        "--prep",
        type=str,
        required=False,
        nargs="?",
        help="json file having prepInfo"
    )

    parser.set_defaults(func=_register_prep)


def _register_prep(args) -> str:

    if args.prep is not None:
        params = _get_json(args.prep)
    else:
        params = _get_prep_info_from_cli()

    writer = create_writer_by_args(args)
    response = writer.register_prep(params)

    return response


def _get_prep_dict_from_cli():

    prep_info = dict()

    try:
        prep_info['name'] = input('> name : ')
        prep_info['country'] = input('> country : ')
        prep_info['city'] = input('> city : ')
        prep_info['email'] = input('> email : ')
        prep_info['website'] = input('> website : ')
        prep_info['details'] = input('> details : ')
        prep_info['p2pEndpoint'] = input('> p2pEndpoint : ')

    except InvalidFormatException as e:
        print(e.args[0])

    ret = dict()

    for k, v in prep_info.items():
        if v is not '':
            ret[k] = v

    return ret


def _get_prep_info_from_cli():

    while True:

        prep_info = _get_prep_dict_from_cli()

        print(json.dumps(prep_info, indent=4))

        check = input('All of them are right? (Y/n): ')

        if check.lower() == 'y':
            break

    return prep_info


def _get_json(path, set_prep: bool = False):
    with open(path) as register:
        params = json.load(register)

    try:
        validate_prep_data(params, set_prep)
    except InvalidFormatException as e:
        print(e.args[0])
        sys.exit(1)  # invalid format entered.

    return params


def _init_for_unregister_prep(sub_parser, common_parent_parser, tx_parent_parser):
    name = "unregisterPRep"
    desc = f"Unregister P-Rep"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.set_defaults(func=_unregister_prep)


def _unregister_prep(args) -> str:
    writer = create_writer_by_args(args)
    response = writer.unregister_prep()

    return response


def _init_for_set_prep(sub_parser, common_parent_parser, tx_parent_parser):
    name = "setPRep"
    desc = f"Change enrolled P-Rep information"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "--prep",
        type=str,
        required=False,
        help="json file having prepInfo"
    )

    parser.set_defaults(func=_set_prep)


def _set_prep(args) -> str:

    if args.prep is not None:
        params = _get_json(args.prep,set_prep=True)
    else:
        params = _get_prep_info_from_cli(is_set_prep=True)

    writer = create_writer_by_args(args)
    response = writer.set_prep(params)

    return response


def _init_for_set_governance_variables(sub_parser, common_parent_parser, tx_parent_parser):
    name = "setGovernanceVariables"
    desc = f"Change Governance variables used in network operation "

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser, tx_parent_parser],
        help=desc)

    parser.add_argument(
        "--irep",
        type=str,
        required=True,
        nargs="?",
        help="amounts of irep"
    )

    parser.set_defaults(func=_set_governance_variables)


def _set_governance_variables(args) -> str:
    params = {
        'irep': args.irep
    }
    writer = create_writer_by_args(args)
    response = writer.set_governance_variables(params)

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
        required=True,
        help="keystore file path"
    )

    return parent_parser
