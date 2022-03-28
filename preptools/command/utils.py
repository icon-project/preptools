# Copyright 2020 ICON Foundation
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

import argparse

from ..utils import str_to_int


def create_tx_parser() -> argparse.ArgumentParser:
    """Common options for invoke commands

    :return:
    """

    parent_parser = argparse.ArgumentParser(add_help=False)

    parent_parser.add_argument(
        "--password", "-p",
        type=str,
        required=False,
        default=None,
        help="keystore password"
    )

    parent_parser.add_argument(
        "--keystore", "-k",
        type=str,
        required=False,
        help="keystore file path"
    )

    parent_parser.add_argument(
        "--step-limit", "-s",
        type=str_to_int,
        required=False,
        default=None,
        dest="step_limit",
        help="step limit to set"
    )

    parent_parser.add_argument(
        "--step-margin", "-m",
        type=str_to_int,
        required=False,
        default="0",
        dest="step_margin",
        help="Can be used when step-limit option is not given.\n"
             "Set step-limit value to estimated Step + this value(step-margin)"
    )

    return parent_parser
