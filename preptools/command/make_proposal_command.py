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

import functools
from argparse import ArgumentParser
from sys import stderr

from .make_proposal.command import Command


def init(parent_sub_parsers, _: ArgumentParser):
    name = "makeProposal"
    desc = f"Make contents of a given network proposal"

    parser = parent_sub_parsers.add_parser(name=name, help=desc)

    func = functools.partial(_run, parser=parser)
    parser.set_defaults(func=func)
    sub_parsers = parser.add_subparsers()

    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="filepath to save proposal contents",
    )

    Command.init_all(sub_parsers, parent_parser)


def _run(*args, **kwargs):
    parser = kwargs["parser"]
    parser.print_help(stderr)
