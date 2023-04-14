# Copyright 2023 ICON Foundation
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
from argparse import (
    ArgumentParser,
    Namespace,
)
from typing import List, Dict, Union, Optional

from .command import Command
from ...exception import InvalidArgumentException
from ...utils.validation_checker import is_valid_address


INT_TYPE = "int"
STR_TYPE = "str"
ADDRESS_TYPE = "Address"
BOOL_TYPE = "bool"
BYTES_TYPE = "bytes"
STRUCT_TYPE = "struct"


class CallMethod(Command):
    def __init__(self):
        self._name = "call"
        self._help = f"{self._name} network proposal"

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        parser.add_argument(
            "to",
            type=str,
            help="SCORE address"
        )
        parser.add_argument(
            "method",
            type=str,
            help="method name to call"
        )
        parser.add_argument(
            "--params",
            type=str,
            nargs="+",
            required=False,
            help="Arguments information to be passed to method (TYPE@VALUE[@FIELDS], "
                 "FIELDS required if parameter is struct or []struct)",
        )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        self._validate(args)
        value = {"to": args.to, "method": args.method}
        if args.params:
            value["params"] = self.convert_params(args.params)
        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)
        return proposal

    @staticmethod
    def _validate(args: Namespace):
        if "method" not in args:
            raise InvalidArgumentException(f"method required.")
        if not is_valid_address(args.to):
            raise InvalidArgumentException(f"Invalid address: {args.to}")

    @staticmethod
    def get_type_value_fields(param: str) -> (str, str, Optional[Dict[str, str]]):
        first_at_index = param.index("@")
        type_ = param[:first_at_index]
        if type_ in (STRUCT_TYPE, f"[]{STRUCT_TYPE}"):
            last_at_index = param.rindex("@")
            if first_at_index == last_at_index:
                raise InvalidArgumentException("FIELD information required")
            fields = param[last_at_index+1:]
            value = param[first_at_index+1:last_at_index]
            return type_, value, json.loads(fields)
        value = param[first_at_index+1:]
        return type_, value, None

    @staticmethod
    def convert_params(params: List[str]) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        new_params = []
        for i, param in enumerate(params):
            if "@" not in param:
                raise InvalidArgumentException("invalid arguments information format. at(@) required")
            type_, value, fields = CallMethod.get_type_value_fields(param)
            new_param = {}
            if fields is not None:
                new_param["fields"] = fields
            if type_ == INT_TYPE:
                CallMethod._validate_int(value)
            elif type_ == STR_TYPE:
                pass
            elif type_ == ADDRESS_TYPE:
                if not is_valid_address(value):
                    raise InvalidArgumentException(f"invalid address: {value}")
            elif type_ == BOOL_TYPE:
                CallMethod._validate_bool(value)
            elif type_ == BYTES_TYPE:
                CallMethod._validate_bytes(value)
            elif type_ == STRUCT_TYPE:
                value = CallMethod._convert_struct(value, fields)
            elif type_.startswith("[]"):
                value = CallMethod._convert_list(type_, value, fields)
            else:
                raise InvalidArgumentException(f"invalid type : {type_}")
            new_param["type"] = type_
            new_param["value"] = value
            new_params.append(new_param)
        return new_params

    @staticmethod
    def _validate_int(v: str):
        try:
            int(v, 16)
        except Exception:
            raise InvalidArgumentException(f"invalid address: {v}")

    @staticmethod
    def _validate_bool(v: str):
        if v not in ("0x1", "0x0"):
            raise InvalidArgumentException(f"invalid bool value: {v}")

    @staticmethod
    def _validate_bytes(v: str):
        if not v.startswith("0x"):
            raise InvalidArgumentException(f"invalid bytes value: {v}")
        try:
            bytes.fromhex(v[2:])
        except ValueError:
            raise InvalidArgumentException(f"invalid bytes value: {v}")

    @staticmethod
    def _validate_address(v: str):
        if not is_valid_address(v):
            raise InvalidArgumentException(f"invalid address: {v}")

    @staticmethod
    def _validate_struct(v: dict, fields: dict):
        if not fields:
            raise InvalidArgumentException("FIELD information required")
        for f in fields:
            if fields[f] == INT_TYPE:
                CallMethod._validate_int(v[f])
            elif fields[f] == STR_TYPE:
                continue
            elif fields[f] == ADDRESS_TYPE:
                CallMethod._validate_address(v[f])
            elif fields[f] == BOOL_TYPE:
                CallMethod._validate_bool(v[f])
            elif fields[f] == BYTES_TYPE:
                CallMethod._validate_bytes(v[f])
            else:
                raise InvalidArgumentException(f"Invalid type: {fields[f]}")

    @staticmethod
    def _convert_struct(v: str, fields: dict) -> dict:
        value = json.loads(v)
        CallMethod._validate_struct(value, fields)
        return value

    @staticmethod
    def _convert_list(t: str, v: str, f: dict) -> list:
        value: list = json.loads(v)
        if not isinstance(value, list):
            raise InvalidArgumentException(f"invalid list: {v}")
        elements_type = t[2:]
        for i, e in enumerate(value):
            if elements_type == INT_TYPE:
                CallMethod._validate_int(e)
            elif elements_type == STR_TYPE:
                pass
            elif elements_type == ADDRESS_TYPE:
                CallMethod._validate_address(e)
            elif elements_type == BOOL_TYPE:
                CallMethod._validate_bool(e)
            elif elements_type == BYTES_TYPE:
                CallMethod._validate_bytes(e)
            elif elements_type == STRUCT_TYPE:
                CallMethod._validate_struct(e, f)
            else:
                raise InvalidArgumentException(f"invalid type : {elements_type}")
        return value
