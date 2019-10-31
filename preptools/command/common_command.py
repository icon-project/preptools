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

import getpass
import json
import os

from iconsdk.wallet.wallet import KeyWallet

from preptools.exception import InvalidFormatException
from preptools.utils.preptools_config import FN_CLI_CONF, preptools_config
from preptools.utils.utils import write_file
from preptools.utils.validation_checker import validate_password


def init(sub_parser, common_parent_parser):
    _init_for_keystore(sub_parser)
    _init_for_genconf(sub_parser)


def _init_for_keystore(sub_parser):
    name = "keystore"
    desc = 'Create keystore file in the specified path.'

    parser = sub_parser.add_parser(
        name,
        help=desc)

    parser.add_argument('path',
                        type=str,
                        help='Path of keystore file.')
    parser.add_argument('-p', '--password',
                        help='Keystore file\'s password',
                        dest='password')

    parser.set_defaults(func=_keystore)


def _keystore(args):
    password = args.password
    password = _check_keystore(password)

    content = KeyWallet.create()
    content.store(args.path, password)

    print(f"Made keystore file successfully")

    return 0


def _init_for_genconf(sub_parser):
    name = "genconf"
    desc = 'Create config file in the specified path.'

    parser = sub_parser.add_parser(
        name,
        help=desc)

    parser.add_argument('--path',
                        type=str,
                        default=FN_CLI_CONF,
                        help='Path of configue file. default(./preptools_config.json)')

    parser.set_defaults(func=_genconf)


def _genconf(args):
    """Generate tbears config files. (tbears_server_config.json, tbears_cli_config.json, keystore_test1)"""
    result = _gen_conf_file()

    if result:
        print(f"Made {result} successfully")
    else:
        print(f"There were configuration files already.")

    return 0


def _gen_conf_file():

    if os.path.exists(FN_CLI_CONF) is False:
        write_file('./', FN_CLI_CONF, json.dumps(preptools_config, indent=4))
        return FN_CLI_CONF

    return None


def _check_keystore(password: str):
    if not password:
        password = getpass.getpass("Input your keystore password: ")
        password_retype = getpass.getpass("Retype your keystore password: ")

        if password != password_retype:
            raise InvalidFormatException("Sorry, passwords do not match. Failed to make keystore file")

    if not validate_password(password):
        raise InvalidFormatException("Password must be at least 8 characters long including alphabet, number, "
                                     "and special character.")
    return password
