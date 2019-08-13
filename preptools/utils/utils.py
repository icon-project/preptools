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
import os

from typing import TYPE_CHECKING, Union, Optional
from urllib.parse import urlparse

from .constants import COLUMN, PREDEFINED_URLS
from preptools.exception import InvalidFileWriteException

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


def print_proposal_value(params: dict):
    print_title("Value")
    print_dict(params)


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


def write_file(parent_directory: str, file_name: str, contents: str, overwrite: bool = False) -> None:
    """Create file with the contents in the parents directory.

    :param parent_directory: Location to create the file.
    :param file_name: File name
    :param contents: Contents of file.
    """
    try:
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        if os.path.exists(f'{parent_directory}/{file_name}') and not overwrite:
            return
        with open(f'{parent_directory}/{file_name}', mode='w') as file:
            file.write(contents)
    except (PermissionError, IsADirectoryError) as e:
        raise InvalidFileWriteException(f"Can't write file {parent_directory}/{file_name}. {e}")

