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

from preptools.preptools_exception import InvalidFormatException
from tests.commons.constants import TEST_SET_JSON_PATH, TEST_REGISTER_JSON_PATH, TEST_KEYSTORE_PATH
from preptools.utils.format_checker import (
    _validate_country,
    _validate_email,
    _validate_p2p_endpoint,
    _validate_uri,
    validate_prep_data
)


class TestFormatChecker(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_check_email_format(self):
        # with valid param
        email = "iconproject@iconloop.com"
        try:
            _validate_email(email)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        email = "icon-project'@iconloop.com"
        self.assertRaises(InvalidFormatException, _validate_email, email)

        email = "icon-project@iconloop."
        self.assertRaises(InvalidFormatException, _validate_email, email)

    def test_check_url(self):
        # with valid param
        website = "http://www.naver.co.kr:9231/"
        try:
            _validate_uri(website)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        website = "http://www.naver.co.kr:9231"
        try:
            _validate_uri(website)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        # with valid param
        details = "http://www.naver.co.kr:9231/api/v3"
        try:
            _validate_uri(details)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        details = "http://www.n,aver.co.kr:9231/api/v3"
        self.assertRaises(InvalidFormatException, _validate_uri, details)

        details = "http://www.naver.co.kr:923,1/a|p|i/v3?asdfe\_#"
        self.assertRaises(InvalidFormatException, _validate_uri, details)

    def test_check_country(self):
        # with valid param
        country = "KOR"
        try:
            _validate_country(country)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        country = "KOREA"
        self.assertRaises(InvalidFormatException, _validate_country, country)

    def test_check_p2pEndpoint(self):
        # with valid param
        p2p_endpoint = "127.0.0.1:9000"
        try:
            _validate_p2p_endpoint(p2p_endpoint)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        p2p_endpoint = "www.naver.co.kr:9231"
        try:
            _validate_p2p_endpoint(p2p_endpoint)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        p2p_endpoint = "http://www.naver.co.kr:9231"
        self.assertRaises(InvalidFormatException, _validate_p2p_endpoint, p2p_endpoint)

    def test_check_prep(self):
        # with set_prep.json file
        with open(TEST_SET_JSON_PATH) as set_json:
            param = json.load(set_json)

        try:
            validate_prep_data(param, True)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        # with register_prep.json file
        with open(TEST_REGISTER_JSON_PATH) as register_json:
            param = json.load(register_json)

        try:
            validate_prep_data(param)
        except InvalidFormatException as e:
            self.fail(e.args[0])

        # with invalid file
        with open(TEST_KEYSTORE_PATH) as keystore:
            param = json.load(keystore)

        self.assertRaises(InvalidFormatException, validate_prep_data, param)

