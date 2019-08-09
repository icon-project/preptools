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

from preptools.command.prep_setting_command import _get_prep_input
from preptools.core.prep import _get_common_args
from preptools.utils.utils import print_tx_result, print_tx_by_hash
from tests.commons.constants import (
    TEST_KEYSTORE_PATH,
    TEST_KEYSTORE_PASSWORD,
    TEST_REGISTER_JSON_PATH,
    TEST_SET_JSON_PATH,
    TEST_WRONG_CONFIG_PATH,
    REGISTER_SAMPLE,
    UNREGISTER_SAMPLE,
    SET_SAMPLE,
    SET_GOVERNANCE_VARIABLES_SAMPLE,
    GET_PREP_SAMPLE,
    GET_PREPS_SAMPLE,
    GET_TRANSACTION_RESULT_SAMPLE,
    GET_TRANSACTION_SAMPLE
)
from tests.commons.core_for_test import create_reader, create_writer


class Container(object):
    pass


class TestPRep(unittest.TestCase):

    def setUp(self) -> None:
        self.args_reset()

    def args_reset(self):
        self.args = Container()

        self.args.url = "127.0.0.1:9000/api/v3"
        self.args.nid = 3
        self.args.keystore = TEST_KEYSTORE_PATH
        self.args.password = TEST_KEYSTORE_PASSWORD
        self.args.yes = True

    def test_register_prep(self):
        # write with file
        with open(TEST_REGISTER_JSON_PATH) as register:
            params = json.load(register)

        writer = create_writer(self.args.keystore, self.args.password)
        response = writer.register_prep(params)
        self.assertTrue(is_request_equal(response, REGISTER_SAMPLE))

        # write with args. (cmd line)
        self.args_reset()
        self.args.name = "banana node"
        self.args.country = "KOR"
        self.args.city = "Seoul"
        self.args.email = "banana@example.com"
        self.args.website = "https://icon.banana.com"
        self.args.details = "https://icon.banana.com/json"
        self.args.p2pEndpoint = "node.example.com:7100"

        params = {}
        _get_prep_input(self.args, params)
        response = writer.register_prep(params)
        self.assertTrue(is_request_equal(response, REGISTER_SAMPLE))

    def test_unregister_prep(self):
        writer = create_writer(self.args.keystore, self.args.password)
        response = writer.unregister_prep()
        print(json.dumps(response, indent=4))
        self.assertTrue(is_request_equal(response, UNREGISTER_SAMPLE))

    def test_set_prep(self):
        # write with file
        with open(TEST_SET_JSON_PATH) as register:
            params = json.load(register)

        writer = create_writer(self.args.keystore, self.args.password)
        response = writer.set_prep(params)
        self.assertTrue(is_request_equal(response, SET_SAMPLE))

        # write with args (cmd line)
        self.args_reset()
        self.args.name = "kokoa node"
        self.args.country = "KOR"
        self.args.website = "https://icon.kokoa.com"
        self.args.details = "https://icon.kokoa.com/json"
        self.args.p2pEndpoint = "node.example.com:7100"

        response = writer.set_prep(params)
        self.assertTrue(is_request_equal(response, SET_SAMPLE))

    def test_governance_variables(self):
        irep = "0x0x21e19e0c9bab2400000"
        params = {'irep': irep}
        writer = create_writer(self.args.keystore, self.args.password)
        response = writer.set_governance_variables(params)
        self.assertTrue(is_request_equal(response, SET_GOVERNANCE_VARIABLES_SAMPLE))

    def test_get_prep(self):
        address = "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
        reader = create_reader()
        response = reader.get_prep(address)
        self.assertTrue(is_request_equal(response, GET_PREP_SAMPLE))

    def test_get_preps(self):
        reader = create_reader()
        response = reader.get_preps({})
        self.assertTrue(is_request_equal(response, GET_PREPS_SAMPLE))

    def test_tx_result(self):
        reader = create_reader()
        response = reader.get_tx_result('0x001d8d2b99c0169df7f7545168451a2fb0608cc218e74ecec15516bf836bcd39')
        print_tx_result(response)
        self.assertTrue(is_request_equal(response, GET_TRANSACTION_RESULT_SAMPLE))

    def test_tx_by_hash(self):
        reader = create_reader()
        response = reader.get_tx_by_hash('0x1a4809d0a0446da469361e63a36265238f1dec6ff1afa10383231a64ed650692')
        print_tx_by_hash(response)
        self.assertTrue(is_request_equal(response, GET_TRANSACTION_SAMPLE))

    def test_get_common_args(self):
        # when args value exists, have to maintain args value.
        self.args.config = TEST_WRONG_CONFIG_PATH
        url, nid, keystore = _get_common_args(self.args)

        self.assertTrue(url == self.args.url)
        self.assertTrue(nid == self.args.nid)
        self.assertTrue(keystore == self.args.keystore)

        # when args value non exists, have to get common args value from configure file.
        self.args.url = None
        self.args.nid = None
        self.args.keystore = None

        url, nid, keystore = _get_common_args(self.args)

        self.assertFalse(url == self.args.url)
        self.assertFalse(nid == self.args.nid)
        self.assertFalse(keystore == self.args.keystore)


def is_request_equal(first_dict: dict, second_dict: dict) -> bool:

    if list(first_dict.keys()) != list(second_dict.keys()):
        return False

    for k, v in first_dict.items():

        if isinstance(v, (dict, list)):
            if is_request_equal(v, second_dict[k]) is False:
                return False

        elif k == 'signature' or k == 'timestamp':
            continue

        elif v != second_dict[k]:
            return False

    return True
