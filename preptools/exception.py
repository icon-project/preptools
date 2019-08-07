# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
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
from enum import IntEnum, unique
from typing import Optional


@unique
class PRepToolsExceptionCode(IntEnum):
    """Result code enumeration

    Refer to http://www.simple-is-better.org/json-rpc/jsonrpc20.html#examples
    """
    OK = 0
    STRING_FORMAT_ERROR = 1

    def __str__(self) -> str:
        return str(self.name).capitalize().replace('_', ' ')


class PRepToolsBaseException(BaseException):

    def __init__(self, message: Optional[str], code: PRepToolsExceptionCode = PRepToolsExceptionCode.OK):
        if message is None:
            message = str(code)
        self.__message = message
        self.__code = code

    @property
    def message(self):
        return self.__message

    @property
    def code(self):
        return self.__code

    def __str__(self):
        return f'{self.message}'


class InvalidFormatException(PRepToolsBaseException):
    """Invalid string format for preptools"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.STRING_FORMAT_ERROR)
