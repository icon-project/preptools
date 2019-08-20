# -*- coding: utf-8 -*-

# Copyright 2019 ICON Foundation
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

from ..core.prep import create_reader_by_args


def init(sub_parser, common_parent_parser):
    _init_for_tx_result(sub_parser, common_parent_parser)
    _init_for_tx_by_hash(sub_parser, common_parent_parser)


def _init_for_tx_result(sub_parser, common_parent_parser):
    name = "txresult"
    desc = f"Get transaction result by hash"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "tx_hash",
        type=str,
        help="transaction hash to get transaction result"
    )

    parser.set_defaults(func=_tx_result)


def _tx_result(args):

    reader = create_reader_by_args(args)
    response = reader.get_tx_result(args.tx_hash)

    return response


def _init_for_tx_by_hash(sub_parser, common_parent_parser):
    name = "txbyhash"
    desc = f"Get transaction by hash"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "tx_hash",
        type=str,
        help="transaction hash to get transaction information"
    )

    parser.set_defaults(func=_tx_by_hash)


def _tx_by_hash(args):

    reader = create_reader_by_args(args)
    response = reader.get_tx_by_hash(args.tx_hash)

    return response
