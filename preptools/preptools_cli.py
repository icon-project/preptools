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
import json
import sys
import time
from typing import Optional

from preptools.command import prep_setting_command, prep_info_command, tx_info_command, wallet_command
from preptools.core.prep import create_icon_service
from preptools.exception import PRepToolsExceptionCode
from preptools.utils.constants import DEFAULT_NID, DEFAULT_URL, PREDEFINED_URLS
from preptools.utils.utils import print_tx_result, print_response


def main():
    handlers = [
        prep_setting_command.init,
        prep_info_command.init,
        tx_info_command.init,
        wallet_command.init
    ]

    parser = argparse.ArgumentParser(
        prog="preptools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="P-Rep management cli")
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
    except KeyboardInterrupt:
        print("\nexit")
        sys.exit(0)

    if isinstance(response, dict):
        if 'result' in response:
            print('request success.')
        else:
            print('Got an error response')

        print_response(json.dumps(response, indent=4))

    if isinstance(response, int) is False:
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
        help=f"node url default) {DEFAULT_URL}"
    )
    parent_parser.add_argument(
        "--nid", "-n",
        type=int,
        required=False,
        help=f"networkId default({DEFAULT_NID} ex) mainnet(1), testnet(2)"
    )
    parent_parser.add_argument(
        "--config", "-c",
        type=str,
        required=False,
        help="preptools config file path"
    )

    return parent_parser


if __name__ == "__main__":
    sys.exit(main())