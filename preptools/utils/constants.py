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
import os

DIR_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(DIR_PATH, '..', '..'))

EOA_ADDRESS = "hx1234567890123456789012345678901234567890"
GOVERNANCE_ADDRESS = "cx0000000000000000000000000000000000000001"
ZERO_ADDRESS = "cx0000000000000000000000000000000000000000"

DEFAULT_URL = "http://127.0.0.1:9000/api/v3"
DEFAULT_NID = 3

COLUMN = 80

PREDEFINED_URLS = {}


class ConstantKeys:
    NAME = "name"
    COUNTRY = "country"
    CITY = "city"
    EMAIL = 'email'
    WEBSITE = 'website'
    DETAILS = 'details'
    P2P_ENDPOINT = 'p2pEndpoint'
    IREP = "irep"
    NODE_ADDRESS = "nodeAddress"


fields_to_validate = (
            ConstantKeys.NAME,
            ConstantKeys.COUNTRY,
            ConstantKeys.CITY,
            ConstantKeys.EMAIL,
            ConstantKeys.WEBSITE,
            ConstantKeys.DETAILS,
            ConstantKeys.P2P_ENDPOINT,
            ConstantKeys.NODE_ADDRESS
        )


proposal_param_by_type = [
    ["value_value"],                    # type 0
    ["value_code", "value_name"],       # type 1
    ["value_address", "value_type"],    # type 2
    ["value_address"],                  # type 3
    ["value_value"]                     # type 4
]
