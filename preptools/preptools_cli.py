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
import time
from typing import Optional

from iconsdk.exception import IconServiceBaseException

from preptools.command import (
    prep_setting_command,
    proposal_setting_command,
    prep_info_command,
    proposal_info_command,
    tx_info_command,
    common_command
)
from preptools.core.prep import create_icon_service
from preptools.exception import PRepToolsExceptionCode, PRepToolsBaseException
from preptools.utils.constants import DEFAULT_NID, DEFAULT_URL, PREDEFINED_URLS
from preptools.utils.utils import get_preptools_version
from preptools.utils.utils import print_tx_result, print_response


def main() -> Optional:
    handlers = [
        prep_setting_command.init,
        proposal_setting_command.init,
        prep_info_command.init,
        proposal_info_command.init,
        tx_info_command.init,
        common_command.init
    ]

    version = get_preptools_version()
    parser = argparse.ArgumentParser(
        prog="preptools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"P-Rep management command line interface v{version}")

    sub_parser = parser.add_subparsers(title="subcommands")

    common_parent_parser = create_common_parser()

    for handler in handlers:
        handler(sub_parser, common_parent_parser)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    args = parser.parse_args()

    try:
        response: Optional[dict, int] = args.func(args)
    except (PRepToolsBaseException, IconServiceBaseException) as e:
        print(e)
        response = e.code.value
    except Exception as e:
        print(f"Exception : {e}")
        response = PRepToolsExceptionCode.COMMAND_ERROR.value
    except KeyboardInterrupt:
        print("\nexit")
        response = 0

    if isinstance(response, int) is False and response:
        print_response(response)
        sys.exit(PRepToolsExceptionCode.OK.value)

    sys.exit(response)


def _print_tx_result(args, tx_hash: str) -> int:
    if tx_hash.startswith("0x") and len(tx_hash) == 66:
        time.sleep(2)
        icon_service = create_icon_service(args.url)
        tx_result: dict = icon_service.get_transaction_result(tx_hash)
        print_tx_result(tx_result)
        ret = tx_result["status"]
    else:
        # tx_hash is not tx hash format
        print(tx_hash)
        ret = 1

    print("")

    return ret


def _get_epilog() -> str:
    words = ["predefined urls:"]

    for key, value in PREDEFINED_URLS.items():
        words.append(f"    {key}: {value}")

    return "\n".join(words)


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
