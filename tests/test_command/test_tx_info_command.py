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
from tests.commons.constants import (
    TEST_KEYSTORE_PATH,
    TEST_KEYSTORE_PASSWORD,
    TEST_CONFIG_PATH
)
from prep.command.tx_info_command import _tx_by_hash, _tx_result
from prep.utils.utils import print_tx_result, print_tx_by_hash


class Container(object):
    pass


class TestPrep(unittest.TestCase):

    def setUp(self) -> None:
        self.args = Container()

        with open(TEST_CONFIG_PATH) as configure:
            conf = json.load(configure)

        self.args.url = conf['uri']
        self.args.nid = convert_hex_str_to_int(conf['nid'])
        self.args.keystore = TEST_KEYSTORE_PATH
        self.args.password = TEST_KEYSTORE_PASSWORD
        self.args.tx_hash = '0x5f7f339e35bf8dae2d11a3a43f0956fd703e4ce66c9eb91a44106d278c8fc840'
        self.args.yes = True

    def test_tx_result(self):
        response = _tx_result(self.args)
        print_tx_result(response)
        self.assertFalse(response.get('error', False))

    def test_tx_by_hash(self):
        response = _tx_by_hash(self.args)
        print_tx_by_hash(response)
        self.assertFalse(response.get('error', False))
