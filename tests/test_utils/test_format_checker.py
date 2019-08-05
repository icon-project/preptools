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

from preptools.preptools_exception import PrepToolsStringFormatException
from tests.commons.constants import TEST_SET_JSON_PATH, TEST_REGISTER_JSON_PATH, TEST_KEYSTORE_PATH
from preptools.utils.format_checker import (
    check_p2p_endpoint_format,
    check_details_format,
    check_website_format,
    check_email_format,
    check_country_format,
    check_name_format,
    check_city_format,
    check_prep
)


class TestFormatChecker(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_check_email_format(self):
        # with valid param
        email = "icon-project@iconloop.com"
        try:
            check_email_format(email)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        email = "icon-project'@iconloop.com"
        self.assertRaises(PrepToolsStringFormatException, check_email_format, email)

        email = "icon-project@iconloop."
        self.assertRaises(PrepToolsStringFormatException, check_email_format, email)

    def test_check_name(self):
        # with valid param
        name = "Kwangwon Choi"
        try:
            check_name_format(name)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        name = "Kwang-won Choi"
        self.assertRaises(PrepToolsStringFormatException, check_name_format, name)

        name = "Kwangwon-Choi"
        self.assertRaises(PrepToolsStringFormatException, check_name_format, name)

    def test_check_website(self):
        # with valid param
        website = "http://www.naver.co.kr:9231/"
        try:
            check_website_format(website)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        website = "http://www.naver.co.kr:9231"
        try:
            check_website_format(website)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        website = "http://www.naver.com:9010/api/v3"
        self.assertRaises(PrepToolsStringFormatException, check_website_format, website)

    def test_check_country(self):
        # with valid param
        country = "KOR"
        try:
            check_country_format(country)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        country = "KOREA"
        self.assertRaises(PrepToolsStringFormatException, check_country_format, country)

    def test_check_city(self):
        # with valid param
        city = "SEOUL"
        try:
            check_city_format(city)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        city = "SE0UL"
        self.assertRaises(PrepToolsStringFormatException, check_city_format, city)

    def test_check_details(self):
        # with valid param
        details = "http://www.naver.co.kr:9231/api/v3"
        try:
            check_details_format(details)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        details = "http://www.n,aver.co.kr:9231/api/v3"
        self.assertRaises(PrepToolsStringFormatException, check_details_format, details)

        details = "http://www.naver.co.kr:923,1/a|p|i/v3?asdfe\_#"
        self.assertRaises(PrepToolsStringFormatException, check_details_format, details)

    def test_check_p2pEndpoint(self):
        # with valid param
        p2p_endpoint = "127.0.0.1:9000"
        try:
            check_p2p_endpoint_format(p2p_endpoint)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        p2p_endpoint = "www.naver.co.kr:9231"
        try:
            check_p2p_endpoint_format(p2p_endpoint)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid param
        p2p_endpoint = "http://www.naver.co.kr:9231"
        self.assertRaises(PrepToolsStringFormatException, check_p2p_endpoint_format, p2p_endpoint)

    def test_check_prep(self):
        # with set_prep.json file
        with open(TEST_SET_JSON_PATH) as set_json:
            param = json.load(set_json)

        try:
            check_prep(param)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with register_prep.json file
        with open(TEST_REGISTER_JSON_PATH) as register_json:
            param = json.load(register_json)

        try:
            check_prep(param)
        except PrepToolsStringFormatException as e:
            self.fail(e.args[0])

        # with invalid file
        with open(TEST_KEYSTORE_PATH) as keystore:
            param = json.load(keystore)

        self.assertRaises(PrepToolsStringFormatException, check_prep, param)

