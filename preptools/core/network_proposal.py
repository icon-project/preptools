# -*- coding: utf-8 -*-
# Copyright 2021 ICON Foundation
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

from enum import IntEnum
from typing import Any, Dict

import jsonschema


class ProposalType(IntEnum):
    Text = 0
    Revision = 1
    MaliciousScore = 2
    PRepDisqualification = 3
    StepPrice = 4
    IRep = 5
    StepCosts = 6
    RewardFundSetting = 7
    RewardFundAllocation = 8

    Last = 8


_schema = {
    ProposalType.Text: {
        "type": "object",
        "properties": {
            "value": {"type": "string"}
        },
        "required": ["value"],
        "additionalProperties": False,
    },
    ProposalType.Revision: {
        "type": "object",
        "properties": {
            "code": {"type": "number"},
            "name": {"type": "string"},
        },
        "required": ["code", "name"],
        "additionalProperties": False,
    },
    ProposalType.MaliciousScore: {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
            "type": {"type": "number"},
        },
        "required": ["address", "type"],
        "additionalProperties": False,
    },
    ProposalType.PRepDisqualification: {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
        },
        "required": ["address"],
        "additionalProperties": False,
    },
    ProposalType.StepPrice: {
        "type": "object",
        "properties": {
            "value": {"type": "number"},
        },
        "required": ["value"],
        "additionalProperties": False,
    },
    ProposalType.StepCosts: {
        "type": "object",
        "properties": {
            "costs": {
                "type": "object",
                "properties": {
                    "schema": {"type": "number"},
                    "default": {"type": "number"},
                    "contractCall": {"type": "number"},
                    "contractCreate": {"type": "number"},
                    "contractUpdate": {"type": "number"},
                    "contractSet": {"type": "number"},
                    "get": {"type": "number"},
                    "getBase": {"type": "number"},
                    "set": {"type": "number"},
                    "setBase": {"type": "number"},
                    "delete": {"type": "number"},
                    "deleteBase": {"type": "number"},
                    "input": {"type": "number"},
                    "log": {"type": "number"},
                    "logBase": {"type": "number"},
                    "apiCall": {"type": "number"},
                },
                "additionalProperties": False,
            },
        },
        "required": ["costs"],
        "additionalProperties": False,
    },
    ProposalType.RewardFundSetting: {
        "type": "object",
        "properties": {
            "iglobal": {"type": "number"},
        },
        "required": ["iglobal"],
        "additionalProperties": False,
    },
    ProposalType.RewardFundAllocation: {
        "type": "object",
        "properties": {
            "rewardFunds": {
                "type": "object",
                "properties": {
                    "iprep": {"type": "number"},
                    "icps": {"type": "number"},
                    "irelay": {"type": "number"},
                    "ivoter": {"type": "number"},
                },
                "required": ["iprep", "icps", "irelay", "ivoter"],
                "additionalProperties": False,
            }
        },
        "required": ["rewardFunds"],
        "additionalProperties": False,
    },
}


def validate_network_proposal(proposal_type: ProposalType, o: Dict[str, Any]):
    schema = _schema[proposal_type]
    jsonschema.validate(o, schema)
