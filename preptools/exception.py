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

    # Exceptions in SDK
    # KEY_STORE_ERROR = 1
    # ADDRESS_ERROR = 2
    # BALANCE_ERROR = 3
    # DATA_TYPE_ERROR = 4
    # JSON_RPC_ERROR = 5
    # ZIP_MEMORY_ERROR = 6
    # URL_ERROR = 7

    COMMAND_ERROR = 8
    STRING_FORMAT_ERROR = 9
    FILE_WRITE_ERROR = 10
    FILE_READ_ERROR = 11

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


class InvalidCommandException(PRepToolsBaseException):
    """Invalid Command"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.COMMAND_ERROR)


class InvalidFormatException(PRepToolsBaseException):
    """Invalid string format for preptools"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.STRING_FORMAT_ERROR)


class InvalidFileWriteException(PRepToolsBaseException):
    """Invalid file write"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.FILE_WRITE_ERROR)


class InvalidFileReadException(PRepToolsBaseException):
    """Invalid file read"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.FILE_READ_ERROR)


class InvalidKeyStoreException(PRepToolsBaseException):
    """Invalid Keystore"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.KEYSTORE_ERROR)


class InvalidDataTypeException(PRepToolsBaseException):
    """Invalid Keystore"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.DATA_TYPE_ERROR)


class InvalidArgumentException(PRepToolsBaseException):
    """INvalid Argument"""
    def __init__(self, message: Optional[str]):
        super().__init__(message, PRepToolsExceptionCode.ARGUMENT_ERROR)
