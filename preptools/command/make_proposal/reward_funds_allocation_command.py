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

from argparse import (
    ArgumentParser,
    Namespace,
)

from .command import Command
from ...exception import InvalidArgumentException


class RewardFundsAllocationCommand(Command):
    def __init__(self):
        self._name = "rewardFundsAllocation"
        self._help = f"{self._name} network proposal to determine the allocation of the monthly reward fund"
        self._options = ("iprep", "icps", "irelay", "ivoter")

    def init(self, sub_parsers, parent_parser: ArgumentParser):
        parser = sub_parsers.add_parser(
            name=self._name,
            help=self._help,
            parents=(parent_parser,),
        )
        for option in self._options:
            parser.add_argument(
                option,
                type=int,
                default=0,
                help=f"{option} in percent [0 ~ 100]",
            )
        parser.set_defaults(func=self._run)

    def _run(self, args: Namespace):
        self._validate(args)

        value = {
            "rewardFunds": {
                option: getattr(args, option)
                for option in self._options
            }
        }
        proposal: str = self._make_proposal(self._name, value)
        self._write_proposal(args.output, proposal)

    def _validate(self, args: Namespace):
        total = 0
        for option in self._options:
            percent = getattr(args, option)
            if 0 <= percent < 100:
                total += percent
            else:
                raise InvalidArgumentException(f"Invalid {option}: {percent}")

        if total != 100:
            values = (f"{option}={getattr(args, option)}" for option in self._options)
            raise InvalidArgumentException(
                f"Total rewardFundsAllocation is not 100: {' '.join(values)}"
            )
