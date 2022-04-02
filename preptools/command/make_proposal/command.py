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
import json
from abc import (
    ABCMeta,
    abstractmethod,
)
from argparse import (
    ArgumentParser,
)
from typing import Any, Dict, Optional

from iconsdk.utils.typing.conversion import object_to_str

Value = Dict[str, Any]


class Command(metaclass=ABCMeta):
    _subclasses = []

    @abstractmethod
    def init(self, sub_parsers, parent_parser: ArgumentParser):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._subclasses.append(cls)

    @classmethod
    def _make_proposal(cls, name: str, value: Value) -> str:
        return json.dumps(
            object_to_str({"name": name, "value": value}),
            separators=(",", ":")
        )

    @classmethod
    def _write_proposal(cls, path: Optional[str], proposal: str):
        if path is not None:
            with open(path, "wt") as f:
                f.write(proposal)

    @classmethod
    def init_all(cls, sub_parsers, parent_parser: ArgumentParser):

        for subclass in cls._subclasses:
            cmd = subclass()
            cmd.init(sub_parsers, parent_parser)
