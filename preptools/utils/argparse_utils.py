# Copyright 2022 ICON Foundation
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
__all__ = ("FileReadAction", "FileReadHexAction")

from argparse import Action
from typing import List, Union

from preptools.exception import InvalidArgumentException


class FileReadAction(Action):
    """
    If an argument starts with '@',
    then it is assumed as filepath and its contents are used instead of its original value.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        _validate(values)

        if isinstance(values, str):
            new_value: str = self._handle_str_value(values)
        else:
            new_value: List[str] = self._handle_list_of_str_value(values)

        setattr(namespace, self.dest, new_value)

    @staticmethod
    def _handle_str_value(value: str) -> str:
        return _get_content_from_value(value, hex_format=False)

    @staticmethod
    def _handle_list_of_str_value(values: List[str]) -> List[str]:
        return [
            _get_content_from_value(value, hex_format=False)
            for value in values
        ]


class FileReadHexAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        _validate(values)

        if isinstance(values, str):
            new_value: str = self._handle_str_value(values)
        else:
            new_value: List[str] = self._handle_list_of_str_value(values)

        setattr(namespace, self.dest, new_value)

    @staticmethod
    def _handle_str_value(value: str) -> str:
        return _get_content_from_value(value, hex_format=True)

    @staticmethod
    def _handle_list_of_str_value(values: List[str]) -> List[str]:
        return [
            _get_content_from_value(value, hex_format=True)
            for value in values
        ]


def _validate(values: Union[str, List[str]]):
    if isinstance(values, str):
        return

    if isinstance(values, list):
        for value in values:
            if not isinstance(value, str):
                raise InvalidArgumentException(f"Unsupported type: {value}")


def _get_content_from_value(value: str, *, hex_format: bool) -> str:
    if value.startswith("@"):
        path = value[1:]
        value = _get_content_from_path(path, hex_format=hex_format)

    return value


def _get_content_from_path(path: str, hex_format: bool) -> str:
    with open(path, "rb") as f:
        data: bytes = f.read()

    return f"0x{data.hex()}" if hex_format else data.decode('utf-8')
