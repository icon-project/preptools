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
    _init_for_get_prep(sub_parser, common_parent_parser)
    _init_for_get_preps(sub_parser, common_parent_parser)


def _init_for_get_prep(sub_parser, common_parent_parser):
    name = "getPRep"
    desc = f"Inquire P-Rep information"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "address",
        type=str,
        help="Address of P-Rep you are looking for"
    )

    parser.set_defaults(func=_get_prep)


def _get_prep(args):
    address = args.address

    reader = create_reader_by_args(args)
    response = reader.get_prep(address)

    return response


def _init_for_get_preps(sub_parser, common_parent_parser):
    name = "getPReps"
    desc = f"Get live status of all registered P-Rep candidates"

    parser = sub_parser.add_parser(
        name,
        parents=[common_parent_parser],
        help=desc)

    parser.add_argument(
        "--start-ranking",
        type=str,
        required=False,
        help="Get P-Rep list which starts from start ranking"
    )

    parser.add_argument(
        "--end-ranking",
        type=str,
        required=False,
        help="Get P-Rep list which ends with end ranking, inclusive"
    )

    parser.add_argument(
        "--block-height",
        type=str,
        required=False,
        help="Block height which ranking formed"
    )

    parser.set_defaults(func=_get_preps)


def _get_preps(args):
    params = _check_get_preps_args(args)

    reader = create_reader_by_args(args)
    response = reader.get_preps(params)

    return response


def _check_get_preps_args(args):
    params = dict()

    if hasattr(args, 'start_ranking') and args.start_ranking:
        params['startRanking'] = args.start_ranking

    if hasattr(args, 'end_ranking') and args.end_ranking:
        params['endRanking'] = args.end_ranking

    if hasattr(args, 'block_height') and args.block_height:
        params['blockHeight'] = args.block_height

    return params
