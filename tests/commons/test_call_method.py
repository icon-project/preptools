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
import unittest

from preptools.command.make_proposal.call_method import CallMethod


class TestCallMethod(unittest.TestCase):

    def test_get_type_value_fields(self):
        params1 = "str@value"
        type1, value1, fields1 = CallMethod.get_type_value_fields(params1)
        assert type1 == "str"
        assert value1 == "value"
        assert fields1 is None

        params2 = "int@0x12"
        type2, value2, fields2 = CallMethod.get_type_value_fields(params2)
        assert type2 == "int"
        assert value2 == "0x12"
        assert fields2 is None

        params3 = "[]int@[\"0x12\",\"0x13\"]"
        type3, value3, fields3 = CallMethod.get_type_value_fields(params3)
        assert type3 == "[]int"
        assert value3 == "[\"0x12\",\"0x13\"]"
        assert fields3 is None

        params4 = "struct@{\"key1\":\"value1\",\"key2\":\"value2\"}@{\"key1\":\"str\",\"key2\":\"str\"}"
        type4, value4, fields4 = CallMethod.get_type_value_fields(params4)
        assert type4 == "struct"
        assert value4 == "{\"key1\":\"value1\",\"key2\":\"value2\"}"
        assert fields4 == {"key1": "str", "key2": "str"}

        params5 = "[]struct@[{\"key1\":\"value1\",\"key2\":\"value2\"},{\"key1\":\"value3\",\"key2\":\"value4\"}]" \
                  "@{\"key1\":\"str\",\"key2\":\"str\"}"
        type5, value5, fields5 = CallMethod.get_type_value_fields(params5)
        assert type5 == "[]struct"
        assert value5 == "[{\"key1\":\"value1\",\"key2\":\"value2\"},{\"key1\":\"value3\",\"key2\":\"value4\"}]"
        assert fields5 == {"key1": "str", "key2": "str"}
