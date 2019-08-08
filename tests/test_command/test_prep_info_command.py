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

from iconsdk.utils.convert_type import convert_hex_str_to_int

from preptools.command.prep_info_command import _get_prep, _get_preps
from preptools.utils.utils import print_tx_result
from tests.commons.constants import (
    TEST_KEYSTORE_PATH,
    TEST_KEYSTORE_PASSWORD,
    TEST_CONFIG_PATH
)


class Container(object):
    pass


class TestPRep(unittest.TestCase):

    def setUp(self) -> None:
        self.args = Container()

        with open(TEST_CONFIG_PATH) as configure:
            conf = json.load(configure)

        self.args.url = conf['url']
        self.args.nid = conf['nid']
        self.args.keystore = TEST_KEYSTORE_PATH
        self.args.password = TEST_KEYSTORE_PASSWORD
        self.args.yes = True

    def test_get_prep(self):
        # success
        self.args.address = "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"

        response = _get_prep(self.args)
        print_tx_result(response)
        self.assertFalse(response.get('error', False))

        # with wrong address
        self.args.address = "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e5"
        response = _get_prep(self.args)
        print_tx_result(response)
        self.assertFalse(response.get('message', False))

    def test_get_preps(self):
        response = _get_preps(self.args)
        print_tx_result(response)
        self.assertFalse(response.get('error', False))

        self.args.startRanking = '0x0'
        response = _get_preps(self.args)
        print_tx_result(response)
        self.assertFalse(response.get('error', False))

        self.args.endRanking = '0x100'
        response = _get_preps(self.args)
        print_tx_result(response)
        self.assertFalse(response.get('error', False))

        self.args.blockHeight = '0x1234'
        response = _get_preps(self.args)
        print_tx_result(response)
        self.assertFalse(response.get('error', False))
