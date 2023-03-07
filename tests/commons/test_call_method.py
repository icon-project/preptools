#
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
#
from preptools.command.make_proposal.call_method import json_from_input


class TestCallMethod:
    def test_json_from_str(self):
        fields = '{key1:str,key2:Address}'
        expected = {"key1": "str", "key2": "Address"}
        converted = json_from_input(fields)
        assert expected == converted

        struct_list1 = '[{key1:abcd,key2:cx1234123412341234123412341234123412341234}]'
        expected = [{"key1": "abcd", "key2": f"cx{'1234'*10}"}]
        converted = json_from_input(struct_list1)
        assert expected == converted

        struct_list2 = '[' \
                       '{key1:abcd,key2:cx1234123412341234123412341234123412341234},' \
                       '{key1:efgh,key2:cx3456345634563456345634563456345634563456}' \
                       ']'
        expected = [
            {"key1": "abcd", "key2": "cx1234123412341234123412341234123412341234"},
            {"key1": "efgh", "key2": "cx3456345634563456345634563456345634563456"}
        ]
        converted = json_from_input(struct_list2)
        assert expected == converted

        address_list = '[cx1234123412341234123412341234123412341234,cx3456345634563456345634563456345634563456]'
        expected = ["cx1234123412341234123412341234123412341234", "cx3456345634563456345634563456345634563456"]
        converted = json_from_input(address_list)
        assert expected == converted
