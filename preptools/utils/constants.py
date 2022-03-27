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
from typing import Optional

DIR_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_PATH = os.path.abspath(os.path.join(DIR_PATH, '..', '..'))

EOA_ADDRESS = "hx1234567890123456789012345678901234567890"
GOVERNANCE_ADDRESS = "cx0000000000000000000000000000000000000001"
ZERO_ADDRESS = "cx0000000000000000000000000000000000000000"

DEFAULT_URL = "http://127.0.0.1:9000/api/v3"
DEFAULT_NID = 3

COLUMN = 80
NETWORK_PROPOSAL_FEE = 100 * 10 ** 18  # 100 ICX


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
    ["value_value"],                    # type 4
    ["value_value"],                    # type 5
    ["value_costs"],                    # type 6
    ["value_iglobal"],                  # type 7
    ["value_rewardFunds"],              # type 8
]


# api endpoint and nid
_PREDEFINED_URLS = {
    "berlin": ("https://berlin.net.solidwallet.io/api/v3", 7),
    "lisbon": ("https://lisbon.net.solidwallet.io/api/v3", 2),
    "mainnet": ("https://ctz.solidwallet.io/api/v3", 1),
}

SYSTEM_SCORE_ADDRESS = "cx0000000000000000000000000000000000000000"
GOVERNANCE_SCORE_ADDRESS = "cx0000000000000000000000000000000000000001"
TREASURY_ADDRESS = "hx1000000000000000000000000000000000000000"

_PREDEFINED_ADDRESSES = {
    "governance": GOVERNANCE_SCORE_ADDRESS,
    "gov": GOVERNANCE_SCORE_ADDRESS,
    "chain": SYSTEM_SCORE_ADDRESS,
    "system": SYSTEM_SCORE_ADDRESS,
    "sys": SYSTEM_SCORE_ADDRESS,
    "treasury": TREASURY_ADDRESS,
}


def get_predefined_url(name: str) -> Optional[str]:
    info = _PREDEFINED_URLS.get(name)
    if info is None:
        return None
    return info[0]


def get_predefined_nid(name: str) -> int:
    info = _PREDEFINED_URLS.get(name)
    if info is None:
        return 0
    return info[1]


def get_predefined_address(name: str) -> Optional[str]:
    return _PREDEFINED_ADDRESSES.get(name)


def resolve_url(url: str) -> str:
    new_url = get_predefined_url(url)
    if new_url:
        return new_url
    return url
