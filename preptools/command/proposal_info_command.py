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

from preptools.core.prep import create_reader_by_args
from preptools.exception import InvalidArgumentException
from preptools.utils import str_to_int


def init(sub_parser, common_parent_parser):
    _init_for_get_proposal(sub_parser, common_parent_parser)
    _init_for_get_proposals(sub_parser, common_parent_parser)


def _init_for_get_proposal(sub_parser, common_parent_parser):
    name = "getProposal"
    desc = f"Query a proposal information with transaction hash"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "transaction_hash",
        type=str,
        help="hash of registerProposal transaction"
    )

    parser.set_defaults(func=_get_proposal)


def _get_proposal(args) -> dict:
    id = args.transaction_hash
    reader = create_reader_by_args(args)
    response = reader.get_proposal(id)

    return response


def _init_for_get_proposals(sub_parser, common_parent_parser):
    name = "getProposals"
    desc = f"Query multiple network proposals."

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "--type",
        type=str_to_int,
        required=False,
        nargs="?",
        help="Type of network proposal to filter"
    )

    parser.add_argument(
        "--status",
        type=str_to_int,
        choices=range(6),
        required=False,
        nargs="?",
        help=(
            "Status of network proposal to filter: \n"
            "0(all), 1(applied), 2(disapproved), 3(canceled), 4(approved), 5(expired)"
        ),
    )

    parser.add_argument(
        "--start",
        type=str_to_int,
        nargs="?",
        help="Starting index. 0 means the latest one",
    )

    parser.add_argument(
        "--size",
        type=str_to_int,
        nargs="?",
        help="Number of proposals to query. [1 ~ 10]",
    )

    parser.set_defaults(func=_get_proposals)


def _get_proposals(args) -> dict:
    params = _check_get_proposal_list_args(args)

    reader = create_reader_by_args(args)
    response = reader.get_proposals(params)

    return response


def _check_get_proposal_list_args(args):
    params = {}

    if hasattr(args, 'type') and args.type:
        params['type'] = args.type

    if hasattr(args, 'status') and args.status:
        params['status'] = args.status

    if hasattr(args, 'start') and isinstance(args.start, int):
        params['start'] = args.start

    if hasattr(args, 'size') and isinstance(args.size, int):
        if not (1 <= args.size <= 10):
            raise InvalidArgumentException("size out of range: min(1), max(10)")
        params['size'] = min(10, args.size)

    return params
