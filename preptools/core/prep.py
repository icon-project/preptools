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

import functools
import getpass
import json
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Union,
)

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.exception import DataTypeException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet
from ..exception import (
    InvalidKeyStoreException,
    InvalidFileReadException,
    InvalidDataTypeException,
)
from ..utils.constants import EOA_ADDRESS, ZERO_ADDRESS, COLUMN, GOVERNANCE_ADDRESS
from ..utils.preptools_config import get_default_config
from ..utils.utils import print_title, print_dict
from ..utils.validation_checker import check_enough_balance


def _print_request(title: str, content: dict):
    print_title(title, COLUMN)
    print_dict(content)
    print()


class TxHandler:
    def __init__(self, service, nid: int, on_send_request: callable(dict)):
        self._icon_service = service
        self._nid = nid
        self._on_send_request = on_send_request

    def _call_tx(self, transaction, owner) -> Union[str, dict]:
        ret = self._call_on_send_request(transaction.to_dict())
        if not ret:
            return

        return self._icon_service.send_transaction(
            SignedTransaction(transaction, owner), full_response=False
        )

    def _call_on_send_request(self, content: dict) -> bool:
        if self._on_send_request:
            listeners = self._on_send_request
            ret = True
            for listener in listeners:
                ret = ret and listener(content)
            return ret

        return False

    def call(self, owner, to, method, params=None, limit=None, value: int = 0, margin: int = 0) -> str:
        transaction = CallTransactionBuilder() \
            .from_(owner.get_address()) \
            .to(to) \
            .version(3) \
            .nid(self._nid) \
            .method(method) \
            .params(params) \
            .value(value)
        if limit is None:
            step_omit_tx = transaction.build()
            estimated_step: int = self._icon_service.estimate_step(step_omit_tx)
            if margin == 0:
                margin = estimated_step // 10
            transaction.step_limit(estimated_step + margin)
        else:
            transaction.step_limit(limit)
        return self._call_tx(transaction.build(), owner)


class PRepToolsListener(object):
    def __init__(self):
        self._listeners = None

    def set_listeners(self, func: List[Callable[[dict], bool]]):
        self._listeners = func

    @property
    def listeners(self) -> List[Callable[[dict], bool]]:
        return self._listeners


class PRepToolsWriter(PRepToolsListener):
    def __init__(self, service, nid: int, owner, step_limit, step_margin):
        super().__init__()

        self._icon_service = service
        self._owner = owner
        self._nid = nid
        self._step_limit = step_limit
        self._step_margin = step_margin

    def _call(self, method: str, params: dict, to: str = ZERO_ADDRESS, value: int = 0) -> str:
        tx_handler = self._create_tx_handler()
        return tx_handler.call(
            owner=self._owner,
            to=to,
            limit=self._step_limit,
            method=method,
            params=params,
            value=value,
            margin=self._step_margin
        )

    def _create_tx_handler(self) -> TxHandler:
        return TxHandler(self._icon_service, self._nid, self.listeners)

    def register_prep(self, params) -> Union[str, Dict[str, Any]]:
        method = "registerPRep"
        return self._call(method, params, value=2000*10**18)

    def unregister_prep(self) -> Union[str, dict]:
        method = "unregisterPRep"
        return self._call(method, {})

    def register_proposal(self, params, value) -> Union[str, dict]:
        method = "registerProposal"
        return self._call(method, params, to=GOVERNANCE_ADDRESS, value=value)

    def cancel_proposal(self, params) -> Union[str, dict]:
        method = "cancelProposal"
        return self._call(method, params, to=GOVERNANCE_ADDRESS)

    def vote_proposal(self, params) -> Union[str, dict]:
        method = "voteProposal"
        return self._call(method, params, to=GOVERNANCE_ADDRESS)

    def apply_proposal(self, params) -> Union[str, dict]:
        method = "applyProposal"
        return self._call(method, params, to=GOVERNANCE_ADDRESS)

    def set_prep(self, params) -> Union[str, dict]:
        method = "setPRep"
        return self._call(method, params)

    def set_governance_variables(self, params) -> Union[str, dict]:
        method = "setGovernanceVariables"
        return self._call(method, params)

    def set_bonder_list(self, params) -> Union[str, dict]:
        method = "setBonderList"
        return self._call(method, params)

    def set_stake(self, params) -> Union[str, dict]:
        method = "setStake"
        return self._call(method, params)

    def set_bond(self, params) -> Union[str, dict]:
        method = "setBond"
        return self._call(method, params)


class PRepToolsReader(PRepToolsListener):
    def __init__(self, service, nid: int, address: str = EOA_ADDRESS):
        super().__init__()

        self._icon_service = service
        self._nid = nid
        self._from = address

    def _call(self, method, params=None, to: str = ZERO_ADDRESS) -> dict:
        call = CallBuilder() \
            .from_(self._from) \
            .to(to) \
            .method(method) \
            .params(params) \
            .build()

        for listener in self.listeners:
            listener(call.to_dict())

        return self._icon_service.call(call, True)

    def _tx_result(self, tx_hash: str):
        try:
            return self._icon_service.get_transaction_result(tx_hash, False)
        except DataTypeException:
            raise InvalidDataTypeException("This hash value is unrecognized.")

    def _tx_by_hash(self, tx_hash):
        try:
            return self._icon_service.get_transaction(tx_hash, False)
        except DataTypeException:
            raise InvalidDataTypeException("This hash value is unrecognized.")

    def get_prep(self, address: str) -> dict:
        params = {"address": address}
        return self._call("getPRep", params)

    def get_bonder_list(self, address: str) -> dict:
        params = {"address": address}
        return self._call("getBonderList", params)

    def get_preps(self, params) -> dict:
        return self._call("getPReps", params)

    def get_proposal(self, _id: str) -> dict:
        params = {"id": _id}
        return self._call("getProposal", params, to=GOVERNANCE_ADDRESS)

    def get_proposals(self, params) -> dict:
        return self._call("getProposals", params, to=GOVERNANCE_ADDRESS)

    def get_tx_result(self, tx_hash: str) -> dict:
        return self._tx_result(tx_hash)

    def get_tx_by_hash(self, tx_hash: str) -> dict:
        return self._tx_by_hash(tx_hash)

    def get_stake(self, address: str) -> dict:
        params = {"address": address}
        return self._call("getStake", params)

    def get_bond(self, address: str) -> dict:
        params = {"address": address}
        return self._call("getBond", params)


def create_reader_by_args(args) -> PRepToolsReader:
    url, nid, _ = _get_common_args(args)
    reader = create_reader(url, nid)

    callback = functools.partial(_print_request, "Request")
    reader.set_listeners([callback])

    return reader


def create_reader(url: str, nid: int) -> PRepToolsReader:
    icon_service = IconService(HTTPProvider(url))
    return PRepToolsReader(icon_service, nid)


def _confirm_callback(content: dict, yes: bool, verbose: bool) -> bool:
    if not yes or verbose:
        _print_request("Request", content)

    if not yes:
        ret: str = input("> Continue? [Y/n]")
        if ret == "n":
            return False

    return True


def create_writer_by_args(args, confirm_callback=_confirm_callback) -> PRepToolsWriter:
    url, nid, keystore_path = _get_common_args(args)
    password: str = args.password

    if keystore_path is None:
        raise InvalidKeyStoreException("There's no keystore path in cmdline, configure.")

    if password is None:
        password = getpass.getpass("> Password: ")
    writer = create_writer(
        url, nid, keystore_path, password, getattr(args, "step_limit"), getattr(args, "step_margin", 0))

    callback1 = functools.partial(confirm_callback, yes=args.yes, verbose=args.verbose)
    callback2 = functools.partial(check_enough_balance, url)
    writer.set_listeners([callback1, callback2])

    return writer


def create_writer(
        url: str, nid: int, keystore_path: str, password: str, step_limit: int, step_margin: int) -> PRepToolsWriter:
    owner_wallet = KeyWallet.load(keystore_path, password)
    service = IconService(HTTPProvider(url))
    return PRepToolsWriter(service, nid, owner_wallet, step_limit, step_margin)


def create_icon_service(url: str) -> IconService:
    return IconService(HTTPProvider(url))


def confirm_callback_for_registerPRep(content: dict, yes: bool, verbose: bool) -> bool:
    if not yes or verbose:
        _print_request("Request", content)

    if not yes:
        ret: str = input("> Once you have registered PRep, you can not get the fee back, Continue? [Y/n]")
        if ret == "n":
            return False

    return True


def _get_common_args(args):
    conf = get_default_config()

    if hasattr(args, 'config') \
            and args.config is not None:
        try:
            with open(args.config) as f:
                tmp_conf = json.load(f)

            for k in tmp_conf:
                conf[k] = tmp_conf[k]

        except (FileNotFoundError, IsADirectoryError):
            if args.config != 'preptools_config.json':
                raise InvalidFileReadException(f"Cannot read configure file, file path : {args.config}")

    url: str = _replace_attribute('url', args, conf)
    nid: int = _replace_attribute('nid', args, conf)
    keystore_path = _replace_attribute('keystore', args, conf)

    return url, nid, keystore_path


def _replace_attribute(attr, args, conf):
    if hasattr(args, attr):
        return getattr(args, attr) if getattr(args, attr) is not None \
            else conf[attr]

    return conf[attr]
