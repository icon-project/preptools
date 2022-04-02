# -*- coding: utf-8 -*-

# Copyright 2019 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
from typing import Dict, Any, Optional

from iconsdk.exception import IconServiceBaseException
from .command import *
from .exception import PRepToolsExceptionCode, PRepToolsBaseException
from .utils.constants import DEFAULT_NID, DEFAULT_URL
from .utils.utils import get_preptools_version
from .utils.utils import print_response


def main() -> Optional:
    handlers = (
        prep_setting_command.init,
        prep_info_command.init,

        proposal_setting_command.init,
        make_proposal_command.init,
        register_proposal2_command.init,
        proposal_info_command.init,

        bond_command.init,
        tx_info_command.init,
        common_command.init,
    )

    version = get_preptools_version()
    parser = argparse.ArgumentParser(
        prog="preptools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"P-Rep management command line interface v{version}")

    sub_parser = parser.add_subparsers(title="subcommands")

    common_parent_parser = create_common_parser()

    for handler in handlers:
        handler(sub_parser, common_parent_parser)

    exit_code: int = PRepToolsExceptionCode.OK.value
    try:
        args = parser.parse_args()
        if not hasattr(args, "func"):
            parser.print_help(sys.stderr)
            sys.exit(exit_code)

        response: Optional[dict, int, str] = args.func(args)
    except (PRepToolsBaseException, IconServiceBaseException) as e:
        response: Dict[str, Any] = e.message
        exit_code = e.code.value
    except Exception as e:
        response = str(e)
        exit_code = PRepToolsExceptionCode.COMMAND_ERROR.value
    except KeyboardInterrupt:
        response = "\nexit"
        exit_code = PRepToolsExceptionCode.COMMAND_ERROR.value

    print_response(response)
    sys.exit(exit_code)


def create_common_parser() -> argparse.ArgumentParser:
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--url", "-u",
        type=str,
        required=False,
        help=f"node url default({DEFAULT_URL})"
    )
    parent_parser.add_argument(
        "--nid", "-n",
        type=int,
        required=False,
        help=f"networkId default({DEFAULT_NID}) ex) mainnet(1), testnet(2)"
    )
    parent_parser.add_argument(
        "--config", "-c",
        type=str,
        required=False,
        default="preptools_config.json",
        help="preptools config file path"
    )
    parent_parser.add_argument(
        "--yes", "-y",
        help="Don't want to ask send transaction.",
        action='store_true',
        dest='yes'
    )
    parent_parser.add_argument(
        "--verbose", "-v",
        help="Verbose mode",
        action='store_true',
        dest='verbose'
    )

    return parent_parser


if __name__ == "__main__":
    sys.exit(main())
