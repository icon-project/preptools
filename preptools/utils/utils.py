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

import json
from typing import TYPE_CHECKING, Union, Optional
from urllib.parse import urlparse

from .constants import COLUMN, PREDEFINED_URLS

if TYPE_CHECKING:
    from urllib.parse import ParseResult


def print_title(title: str, column: int = COLUMN, sep: str = "="):
    sep_count: int = max(0, column - len(title) - 3)
    print(f"[{title}] {sep * sep_count}")


def print_dict(data: dict):
    converted = {}

    for key in data:
        value = data[key]
        if isinstance(value, bytes):
            value = f"0x{value.hex()}"

        converted[key] = value

    print(json.dumps(converted, indent=4))


def print_response(content: Union[str, dict]):
    print_title("Response", COLUMN)

    if isinstance(content, dict):
        print_dict(content)
    else:
        print(content)

    print("")


def print_tx_result(tx_result: dict):
    print_title("Transaction Result")
    print_dict(tx_result)


def print_tx_by_hash(tx: dict):
    print_title("Transaction")
    print_dict(tx)


def is_url_valid(url: str) -> bool:
    ps: 'ParseResult' = urlparse(url)

    return ps.scheme in ("http", "https") \
        and len(ps.netloc) > 0 \
        and len(ps.path) > 0


def get_predefined_url(name: str) -> Optional[str]:
    return PREDEFINED_URLS.get(name)


def get_url(url: str) -> str:
    return url
    # predefined_url: str = get_predefined_url(url)
    #
    # if isinstance(predefined_url, str):
    #     return predefined_url
    #
    # if not is_url_valid(url):
    #     raise ValueError(f"Invalid url: {url}")
    #
    # return url
