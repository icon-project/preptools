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
import re
from argparse import (
    ArgumentParser,
    Namespace,
)
from typing import List, Dict, Union

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
            help="Arguments information that pass to method(type and value. separate with comma)"
                 "\nex) str,hello Address,hx1234.. ",
        )
        parser.add_argument(
            "--fields",
            type=json_from_input,
            required=False,
            help="fields information. json string."
                 "\nex) {\"key1\":\"str\"} needed when params value is struct or []struct"
        )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace) -> str:
        self._validate(args)
        value = {"to": args.to, "method": args.method}
        if args.params:
            value["params"] = self.convert_params(args.params, args.fields)
        if args.fields:
            value["fields"] = args.fields
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
    def convert_params(params: List[str], fields: dict = None) -> List[Dict[str, str]]:
        new_params = []
        for i, p in enumerate(params):
            if "," not in p:
                raise InvalidArgumentException("invalid arguments information format. comma required")
            comma_index = p.index(',')
            t, v = p[:comma_index], p[comma_index+1:]
            if t == INT_TYPE:
                CallMethod._validate_int(v)
            elif t == STR_TYPE:
                pass
            elif t == ADDRESS_TYPE:
                if not is_valid_address(v):
                    raise InvalidArgumentException(f"invalid address: {v}")
            elif t == BOOL_TYPE:
                CallMethod._validate_bool(v)
            elif t == BYTES_TYPE:
                CallMethod._validate_bytes(v)
            elif t == STRUCT_TYPE:
                v = CallMethod._convert_struct(v, fields)
            elif t.startswith("[]"):
                v = CallMethod._convert_list(t, v, fields)
            else:
                raise InvalidArgumentException(f"invalid type : {t}")
            new_params.append({"type": t, "value": v})
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
        value = json_from_input(v)
        CallMethod._validate_struct(value, fields)
        return value

    @staticmethod
    def _convert_list(t: str, v: str, f: dict) -> list:
        value: list = json_from_input(v)
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


def json_from_input(s: str) -> Union[List, Dict]:
    quoted_str = re.sub(r'(\w+)', r'"\1"', s)
    return json.loads(quoted_str)
