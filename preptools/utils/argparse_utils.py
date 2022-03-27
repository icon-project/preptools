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

from argparse import Action


class FileReadAction(Action):
    """
    If an argument starts with '@',
    then it is assumed as filepath and its contents are used instead of its original value.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        new_values = []
        for value in values:
            if value.startswith("@"):
                path = value[1:]
                with open(path, "rt") as f:
                    value: str = f.read()
            new_values.append(value)

        setattr(namespace, self.dest, new_values)


class FileReadHexAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        new_values = []
        for value in values:
            if value.startswith("@"):
                path = value[1:]
                value = self._get_content_from_path(path)
            new_values.append(value)

        setattr(namespace, self.dest, new_values)

    @staticmethod
    def _get_content_from_path(path) -> str:
        with open(path, "rb") as f:
            data: bytes = f.read()
            return f"0x{data.hex()}"
