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

from preptools.command.prep_setting_command import (
    _register_prep,
    _unregister_prep,
    _set_prep,
    _set_governance_variables
)
from tests.commons.constants import (
    TEST_KEYSTORE_PATH,
    TEST_KEYSTORE_PASSWORD,
    TEST_REGISTER_JSON_PATH,
    TEST_SET_JSON_PATH,
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
        self.args.interactive = False

    def test_register_prep(self):
        self.args.prep_json = TEST_REGISTER_JSON_PATH
        response = _register_prep(self.args)
        print(response)
        self.assertFalse(response.get('error', False))

    def test_unregister_prep(self):
        response = _unregister_prep(self.args)
        print(response)
        self.assertFalse(response.get('error', False))

    def test_set_prep(self):
        self.args.prep_json = TEST_SET_JSON_PATH
        response = _set_prep(self.args)
        print(response)
        self.assertFalse(response.get('error', False))

    def test_governance_variables(self):
        self.args.irep = "0x0x21e19e0c9bab2400000"

        response = _set_governance_variables(self.args)
        self.assertFalse(response.get('error', False))