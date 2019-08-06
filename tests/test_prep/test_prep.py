#
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
#

import json
import unittest

from iconsdk.wallet.wallet import KeyWallet
from iconsdk.utils.convert_type import convert_bytes_to_hex_str, convert_hex_str_to_int
from tests.commons.constants import (
    TEST_KEYSTORE_PATH,
    TEST_KEYSTORE_PASSWORD,
    TEST_REGISTER_JSON_PATH,
    TEST_SET_JSON_PATH,
    TEST_CONFIG_PATH
)
from preptools.core.prep import create_writer_by_args, create_reader_by_args, _get_common_args
from preptools.utils.utils import print_tx_result, print_tx_by_hash


class Container(object):
    pass


class TestPRep(unittest.TestCase):

    def setUp(self) -> None:
        self.args = Container()

        with open(TEST_CONFIG_PATH) as configure:
            conf = json.load(configure)

        self.args.url = conf['uri']
        self.args.nid = convert_hex_str_to_int(conf['nid'])
        self.args.keystore = TEST_KEYSTORE_PATH
        self.args.password = TEST_KEYSTORE_PASSWORD
        self.args.yes = True

    def test_register_prep(self):
        with open(TEST_REGISTER_JSON_PATH) as register:
            params = json.load(register)

        writer = create_writer_by_args(self.args)
        response = writer.register_prep(params)
        print(response)
        self.assertFalse(response.get('error', False))

    def test_unregister_prep(self):
        writer = create_writer_by_args(self.args)
        response = writer.unregister_prep()
        print(response)
        self.assertFalse(response.get('error', False))

    def test_set_prep(self):
        with open(TEST_SET_JSON_PATH) as register:
            params = json.load(register)

        writer = create_writer_by_args(self.args)
        response = writer.set_prep(params)
        print(response)
        self.assertFalse(response.get('error', False))

    def test_governance_variables(self):
        irep = "0x0x21e19e0c9bab2400000"
        params = {'irep': irep}
        writer = create_writer_by_args(self.args)
        response = writer.set_governance_variables(params)
        self.assertFalse(response.get('error', False))

    def test_get_prep(self):
        # success
        address = "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
        reader = create_reader_by_args(self.args)
        response = reader.get_prep(address)
        self.assertFalse(response.get('error', False))

        # with wrong address
        invalid_address = "hxef73db5d0ad02eb1fadb37d0041be96bfa56d411"
        response = reader.get_prep(invalid_address)
        self.assertFalse(response.get('result', False))

    def test_get_preps(self):
        reader = create_reader_by_args(self.args)
        response = reader.get_preps({})
        print_tx_result(response)
        self.assertFalse(response.get('error', False))

    def test_tx_result(self):
        reader = create_reader_by_args(self.args)
        response = reader.get_tx_result('0x001d8d2b99c0169df7f7545168451a2fb0608cc218e74ecec15516bf836bcd39')
        print_tx_result(response)
        self.assertFalse(response.get('error', False))

    def test_tx_by_hash(self):
        reader = create_reader_by_args(self.args)
        response = reader.get_tx_by_hash('0x1a4809d0a0446da469361e63a36265238f1dec6ff1afa10383231a64ed650692')
        print_tx_by_hash(response)
        self.assertFalse(response.get('error', False))

    def test_get_common_args(self):
        self.args.config = TEST_CONFIG_PATH
        url, nid, keyStore = _get_common_args(self.args)
        print(url, nid, keyStore)

