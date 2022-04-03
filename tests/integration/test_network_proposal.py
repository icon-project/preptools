from __future__ import annotations

import json
import os
import subprocess
import time
from enum import IntEnum
from typing import Any, Dict, List, Tuple, Union
from iconsdk.utils.convert_type import convert_bytes_to_hex_str

import pytest

from preptools.utils.validation_checker import is_tx_hash

SYS_ADDRESS = "cx0000000000000000000000000000000000000000"
GOV_ADDRESS = "cx0000000000000000000000000000000000000001"


SIG_NETWORK_PROPOSAL_REGISTERED = "NetworkProposalRegistered(str,str,int,bytes,Address)"
SIG_NETWORK_PROPOSAL_VOTED = "NetworkProposalVoted(bytes,int,Address)"
SIG_NETWORK_PROPOSAL_APPLIED = "NetworkProposalApplied(bytes)"


class ReturnType(IntEnum):
    COMPLETE_PROCESS = 0
    STRING = 1
    DICT = 2


class Account:
    def __init__(self, name: str, address: str, keystore: str, password: str):
        self.name = name
        self.address = address
        self.keystore = keystore
        self.password = password

    def __str__(self):
        return (
            f"name={self.name}"
            f" address={self.address}"
            f" keystore={self.keystore}"
            f" password={self.password}"
        )


def getenv(key: str) -> str:
    return os.environ.get(f"PREPTOOLS_TEST_{key}")


def to_loop(icx: int) -> int:
    return icx * 10 ** 18


def create_account(name: str, path: str, password: str) -> Account:
    with open(path, "rt") as fp:
        keystore = json.load(fp)
        return Account(name, keystore["address"], path, password)


def get_string_from_cp(cp: subprocess.CompletedProcess) -> str:
    data: bytes = cp.stdout if cp.stdout else cp.stderr
    return normalize_result(data.decode('utf-8'))


def run_cmd(
        cmd: str,
        return_type: ReturnType = ReturnType.COMPLETE_PROCESS
) -> Union[subprocess.CompletedProcess, str, Dict[str, Any]]:
    print(cmd)
    args = cmd.split(sep=" ")
    cp = subprocess.run(args, capture_output=True)

    if return_type == ReturnType.COMPLETE_PROCESS:
        return cp

    text = get_string_from_cp(cp)
    if return_type == ReturnType.STRING:
        return text

    return json.loads(text)


def normalize_result(text: str) -> str:
    text = text.strip('"\n')
    return text.replace("'", '"')


def get_tx_result(ptools: PRepTools, tx_hash: str, *, retry: int) -> Dict[str, Any]:
    for i in range(retry):
        result: Dict[str, Any] = ptools.get_tx_result(tx_hash)
        if i < retry - 1 and ("code" in result and "message" in result):
            time.sleep(1)
            continue

        print(result)
        return result


def check_if_tx_succeeded(ptools: PRepTools, tx_hashes: Union[str, List[str]]) -> List[Dict[str, Any]]:
    tx_results = []

    if isinstance(tx_hashes, str):
        tx_hashes = [tx_hashes]

    for tx_hash in tx_hashes:
        result: Dict[str, Any] = get_tx_result(ptools, tx_hash, retry=5)
        print(result)
        assert result["status"] == 1
        tx_results.append(result)

    return tx_results


def vote_and_apply_proposal(ptools: PRepTools, _from: Account, proposal_id: str):
    # voteProposal with agree
    tx_hash = ptools.voteProposal(_from, proposal_id, vote=True)
    assert is_tx_hash(tx_hash)
    time.sleep(2)
    check_if_vote_proposal_tx_succeeded(ptools, tx_hash, proposal_id, _from)

    # applyProposal
    tx_hash = ptools.apply_proposal(_from, proposal_id)
    assert is_tx_hash(tx_hash)
    time.sleep(2)
    check_if_apply_proposal_tx_succeeded(ptools, tx_hash, proposal_id, _from)


def check_if_register_proposal_tx_succeeded(
        ptools: PRepTools, proposal_id: str, title: str, desc: str, _from: Account, value: str):
    result: Dict[str, Any] = get_tx_result(ptools, proposal_id, retry=5)
    check_register_proposal(result, title, desc, _from, f"[{value}]")


def check_register_proposal(
        tx_result: Dict[str, Any],
        title: str, desc: str,
        _from: Account, value: str):
    assert tx_result["status"] == 1

    success = 0
    event_logs = tx_result["eventLogs"]
    for event_log in event_logs:
        indexed: List[str] = event_log["indexed"]
        signature: str = indexed[0]

        if signature == SIG_NETWORK_PROPOSAL_REGISTERED:
            check_network_proposal_registered_event_log(
                event_log, title, desc, 9, value, _from)
            success += 1

    assert success == 1


def check_if_vote_proposal_tx_succeeded(
        ptools: PRepTools, tx_hash: str, proposal_id: str, _from: Account):
    result: Dict[str, Any] = get_tx_result(ptools, tx_hash, retry=5)
    check_vote_proposal(result, _from, proposal_id)


def check_vote_proposal(tx_result: Dict[str, Any], _from: Account, proposal_id: str):
    success = 0
    event_logs = tx_result["eventLogs"]
    for event_log in event_logs:
        indexed: List[str] = event_log["indexed"]
        signature: str = indexed[0]

        if signature == SIG_NETWORK_PROPOSAL_VOTED:
            check_network_proposal_voted_event_log(event_log, proposal_id, _from)
            success += 1

    assert success == 1


def check_if_apply_proposal_tx_succeeded(
        ptools: PRepTools, tx_hash: str, proposal_id: str, _from: Account):
    result: Dict[str, Any] = get_tx_result(ptools, tx_hash, retry=5)
    check_apply_proposal(result, _from, proposal_id)


def check_apply_proposal(tx_result: Dict[str, Any], _from: Account, proposal_id: str):
    success = 0
    event_logs = tx_result["eventLogs"]
    for event_log in event_logs:
        indexed: List[str] = event_log["indexed"]
        signature: str = indexed[0]

        if signature == SIG_NETWORK_PROPOSAL_APPLIED:
            check_network_proposal_applied_event_log(event_log, proposal_id)
            success += 1

    assert success == 1


def check_network_proposal_registered_event_log(
        event_log: Dict[str, Any],
        title: str, desc: str, _type: int, value: str, _from: Account):
    indexed: List[str] = event_log["indexed"]
    data: List[str] = event_log["data"]

    assert indexed[0] == SIG_NETWORK_PROPOSAL_REGISTERED
    assert data[0] == title
    assert data[1] == desc
    assert data[2] == hex(_type)
    assert data[3] == convert_bytes_to_hex_str(value.encode('utf-8'))
    assert data[4] == _from.address


def check_network_proposal_voted_event_log(event_log: Dict[str, Any], proposal_id: str, _from: Account):
    indexed: List[str] = event_log["indexed"]
    data: List[str] = event_log["data"]

    assert indexed[0] == SIG_NETWORK_PROPOSAL_VOTED
    assert data[0] == proposal_id
    assert data[1] == "0x1"
    assert data[2] == _from.address


def check_network_proposal_applied_event_log(event_log: Dict[str, Any], proposal_id: str):
    indexed: List[str] = event_log["indexed"]
    data: List[str] = event_log["data"]
    assert indexed[0] == SIG_NETWORK_PROPOSAL_APPLIED
    assert data[0] == proposal_id


class PRepTools:
    def __init__(self, url: str, nid: int, god: Account):
        self._uri = url
        self._nid = nid
        self._god = god

    def register_prep(self, account: Account) -> str:
        name = account.name
        tokens = (
            f"preptools registerPRep --yes",
            f"--url {self._uri}",
            f"--nid {self._nid}",
            f"--name {name}",
            f"--country KOR",
            f"--city Seoul",
            f"--email {name}@mail.com",
            f"--website http://{name}.example.com",
            f"--details http://{name}.example.com/details",
            f"--p2p-endpoint {name}.example.com:1234",
            f"--node-address {account.address}",
            f"--keystore {account.keystore}",
            f"--password {account.password}",
        )
        return run_cmd(" ".join(tokens), ReturnType.STRING)

    def set_stake(self, _from: Account, amount: int) -> str:
        tokens = (
            f"preptools setStake --yes",
            f"--url {self._uri}",
            f"--nid {self._nid}",
            f"--keystore {_from.keystore}",
            f"--password {_from.password}",
            f"{amount}",
        )
        return run_cmd(" ".join(tokens), ReturnType.STRING)

    def set_bond(self, _from: Account, amount: int):
        tokens = (
            f"preptools setBond --yes",
            f"--url {self._uri}",
            f"--nid {self._nid}",
            f"--keystore {_from.keystore}",
            f"--password {_from.password}",
            f"{_from.address},{amount}",
        )
        return run_cmd(" ".join(tokens), ReturnType.STRING)

    def set_bonder_list(self, account: Account, bonders: List[str]) -> str:
        tokens = (
            f"preptools setBonderList --yes",
            f"--url {self._uri}",
            f"--nid {self._nid}",
            f"--keystore {account.keystore}",
            f"--password {account.password}",
            f"--bonder-list {','.join(bonders)}",
        )
        return run_cmd(" ".join(tokens), ReturnType.STRING)

    def get_tx_result(self, tx_hash: str) -> Dict[str, Any]:
        tokens = (
            "preptools txresult",
            f"--url {self._uri}",
            f"--nid {self._nid}",
            f"{tx_hash}",
        )
        return run_cmd(" ".join(tokens), ReturnType.DICT)

    def register_proposal2(self, _from: Account, title: str, desc: str, proposals: List[str]) -> str:
        tokens = [
            "preptools registerProposal2 --yes",
            f"--url {self._uri}",
            f"--nid {self._nid}",
            f"--keystore {_from.keystore}",
            f"--password {_from.password}",
            f"--title {title}",
            f"--desc {desc}",
            f"--proposals",
        ]
        tokens += proposals
        return run_cmd(" ".join(tokens), ReturnType.STRING)

    @staticmethod
    def make_proposal(name: str, options: str) -> str:
        cmd = f"preptools makeProposal {name} {options}"
        return run_cmd(cmd, ReturnType.STRING)

    def voteProposal(self, _from: Account, tx_hash: str, vote: bool) -> str:
        cmd = (
            f"preptools voteProposal --yes "
            f"--url {self._uri} "
            f"--nid {self._nid} "
            f"--keystore {_from.keystore} "
            f"--password {_from.password} "
            f"--id {tx_hash} "
            f"--vote {int(vote)}"
        )
        return run_cmd(cmd, ReturnType.STRING)

    def apply_proposal(self, _from: Account, tx_hash: str) -> str:
        cmd = (
            f"preptools applyProposal --yes "
            f"--url {self._uri} "
            f"--nid {self._nid} "
            f"--keystore {_from.keystore} "
            f"--password {_from.password} "
            f"{tx_hash}"
        )
        return run_cmd(cmd, ReturnType.STRING)


class Goloop:
    DEFAULT_STEP_LIMIT = 500_000

    def __init__(self, url: str, nid: int):
        self._uri = url
        self._nid = nid

    def query_call(self, to: str, method: str, params: List[str] = None) -> str:
        tokens = [
            "goloop rpc call",
            f"--uri {self._uri}",
            f"--to {to}",
            f"--method {method}",
        ]
        if params:
            tokens.append(f"--param {','.join(params)}")
        return run_cmd(" ".join(tokens), ReturnType.STRING)

    def invoke_call(
            self,
            _from: Account,
            to: str,
            method: str,
            step_limit: int = DEFAULT_STEP_LIMIT,
            params: List[str] = None
    ) -> str:
        tokens = [
            "goloop rpc sendtx call",
            f"--uri {self._uri}",
            f"--nid {self._nid}",
            f"--key_store {_from.keystore}",
            f"--key_password {_from.password}",
            f"--step_limit {step_limit}",
            f"--to {to}",
            f"--method {method}",
        ]

        if isinstance(params, list) and len(params) > 0:
            tokens.append(f"--param {','.join(params)}")

        cmd = " ".join(tokens)
        return run_cmd(cmd, ReturnType.STRING)

    def transfer(self, _from: Account, to: Union[str, Account], amount: int, step_limit: int = 100_000):
        if isinstance(to, Account):
            to = to.address

        cmd = (
            "goloop rpc sendtx transfer"
            f" --uri {self._uri}"
            f" --nid {self._nid}"
            f" --key_store {_from.keystore}"
            f" --key_password {_from.password}"
            f" --step_limit {step_limit}"
            f" --to {to}"
            f" --value {amount}"
        )
        return run_cmd(cmd, ReturnType.STRING)

    def deploy_java_score(
            self,
            _from: Account,
            path: str,
            to: str = SYS_ADDRESS,
            params: List[str] = None,
            step_limit: int = 2_000_000_000,
    ) -> str:
        tokens = [
            f"goloop rpc sendtx deploy",
            f"--uri {self._uri}",
            f"--nid {self._nid}",
            f"--key_store {_from.keystore}",
            f"--key_password {_from.password}",
            f"--to {to}",
            f"--content_type application/java",
            f"--step_limit {step_limit}",
            f"{path}",
        ]

        if isinstance(params, list) and len(params) > 0:
            tokens.append(f"--param {','.join(params)}")

        return run_cmd(" ".join(tokens), ReturnType.STRING)

    def set_score_owner(self, _from: Account, score_address: str, owner: str, step_limit: int = 200_000) -> str:
        params = [
            f"score={score_address}",
            f"owner={owner}",
        ]
        return self.invoke_call(
            _from, SYS_ADDRESS, "setScoreOwner", step_limit, params
        )

    def get_network_scores(self) -> Dict[str, Any]:
        ret = self.query_call(SYS_ADDRESS, "getNetworkScores")
        return json.loads(ret)

    def get_score_owner(self) -> str:
        return self.query_call(SYS_ADDRESS, "getScoreOwner")

    def get_revision(self) -> int:
        revision: str = self.query_call(SYS_ADDRESS, "getRevision")
        return int(revision, base=0)

    def get_step_price(self) -> int:
        step_price: str = self.query_call(GOV_ADDRESS, "getStepPrice")
        return int(step_price, base=0)

    def get_step_costs(self) -> Dict[str, Any]:
        ret: str = self.query_call(GOV_ADDRESS, "getStepCosts")
        return json.loads(ret)

    def get_prep_term(self) -> Dict[str, Any]:
        ret: str = self.query_call(SYS_ADDRESS, "getPRepTerm")
        return json.loads(ret)


class Env:
    def __init__(self):
        os.putenv("GOLOOP_RPC_DEBUG", "false")

        port = 9082
        self._uri = f"http://localhost:{port}/api/v3"
        self._nid = 3
        self._gov_score_path = \
            "/Users/goldworm/work/icon/governance2/governance/build/libs/governance-2.1.0-optimized.jar"
        self._god = create_account(
            "prep00",
            "/Users/goldworm/work/icon/run/cli/proposals/local/godWallet.json",
            "gochain",
        )
        prep01 = create_account(
            "prep01",
            "/Users/goldworm/work/icon/run/cli/proposals/local/devnet_builtin_score_owner.key",
            "qwer1234%",
        )
        self._preps = self._god, prep01

        self._stakes = (to_loop(10 ** 8), to_loop(5 ** 8))
        self._bonds = self._stakes

        self._ptools = PRepTools(self._uri, self._nid, self._god)
        self._goloop = Goloop(self._uri, self._nid)
        self._cps_score_path = \
            "/Users/goldworm/work/icon/java-score-examples/hello-world/build/libs/hello-world-0.1.0-optimized.jar"
        self._cache = {}
        self._name_to_score = {
            "sys": SYS_ADDRESS,
            "gov": GOV_ADDRESS,
        }

    @property
    def preps(self) -> Tuple[Account, Account]:
        return self._preps

    @property
    def god(self) -> Account:
        return self._god

    @property
    def ptools(self) -> PRepTools:
        return self._ptools

    @property
    def goloop(self) -> Goloop:
        return self._goloop

    @property
    def stakes(self) -> Tuple[int, int]:
        return self._stakes

    @property
    def bonds(self) -> Tuple[int, int]:
        return self._bonds

    @property
    def gov_score_path(self) -> str:
        return self._gov_score_path

    @property
    def cps_score_path(self) -> str:
        return self._cps_score_path

    @property
    def cache(self) -> Dict[str, Any]:
        return self._cache

    @property
    def cps_address(self) -> str:
        return self._name_to_score["cps"]

    def put_score_address(self, name: str, address: str):
        self._name_to_score[name] = address

    def get_score_address(self, name: str) -> str:
        return self._name_to_score[name]


@pytest.fixture(scope="class")
def env() -> Env:
    return Env()


@pytest.fixture(scope="function")
def ptools(env: Env) -> PRepTools:
    return env.ptools


@pytest.mark.skip(reason="Need to prepare for gochain-local environment")
class TestPRepTools:

    def test_init(self, env: Env):
        ptools = env.ptools
        goloop = env.goloop
        god: Account = env.god
        preps: Tuple[Account, Account] = env.preps
        stakes = env.stakes
        bonds = env.bonds

        tx_hash: str = goloop.transfer(god, preps[1], to_loop(10 ** 8))
        time.sleep(2)
        check_if_tx_succeeded(ptools, tx_hash)

        tx_hashes = []
        for prep in preps:
            tx_hash: str = ptools.register_prep(prep)
            tx_hashes.append(tx_hash)

        time.sleep(2)
        check_if_tx_succeeded(ptools, tx_hashes)

        # Wait until this term is over.
        time.sleep(100)

        # setStake
        tx_hashes = []
        for i, prep in enumerate(preps):
            tx_hash: str = ptools.set_stake(prep, stakes[i])
            tx_hashes.append(tx_hash)
        time.sleep(2)
        check_if_tx_succeeded(ptools, tx_hashes)

        # setBonderList
        tx_hashes = []
        for prep in preps:
            tx_hash: str = ptools.set_bonder_list(prep, [prep.address])
            tx_hashes.append(tx_hash)
        time.sleep(2)
        check_if_tx_succeeded(ptools, tx_hashes)

        # setBond
        tx_hashes = []
        for i, prep in enumerate(preps):
            tx_hash: str = ptools.set_bond(prep, bonds[i])
            tx_hashes.append(tx_hash)

        # Deploy gov2 score
        tx_hash: str = goloop.deploy_java_score(god, env.gov_score_path, GOV_ADDRESS)
        tx_hashes.append(tx_hash)
        time.sleep(2)
        check_if_tx_succeeded(ptools, tx_hashes)

        # Deploy cps score
        tx_hash: str = goloop.deploy_java_score(
            god, env.cps_score_path, SYS_ADDRESS,
            params=["name=Alice"],
        )
        time.sleep(2)
        tx_result: Dict[str, Any] = get_tx_result(ptools, tx_hash, retry=5)
        assert tx_result["status"] == 1
        cps_address: str = tx_result["scoreAddress"]
        env.put_score_address("cps", cps_address)
        print(f"cps_address={cps_address}")

        # Wait until this term is over.
        time.sleep(100)

    def test_revision_proposal(self, env: Env):
        ptools = env.ptools
        goloop = env.goloop
        _from = env.god

        name = "revision"
        revision = goloop.get_revision() + 1

        proposal: str = ptools.make_proposal(name, options=f"{revision}")
        print(proposal)
        obj = json.loads(proposal)
        assert obj["name"] == name
        assert obj["value"]["revision"] == hex(revision)

        # registerProposal2
        title, desc = "title", "desc"
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

        assert goloop.get_revision() == revision

    def test_text_proposal(self, env: Env):
        _from = env.god
        ptools = env.ptools
        title = "title"
        desc = "desc"
        name = "text"
        text = "text_proposal_contents"

        proposal: str = ptools.make_proposal(name, text)
        print(proposal)
        obj = json.loads(proposal)
        assert obj["name"] == name
        value = obj["value"]
        assert value["text"] == text

        # registerProposal2
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal with agree and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

    def test_network_score_designation_proposal(self, env: Env):
        _from = env.god
        goloop = env.goloop
        ptools = env.ptools
        name = "networkScoreDesignation"
        cps_address: str = env.cache.get("cps", env.cps_address)
        title, desc = "title", "desc"

        # Change cps ownership to gov
        tx_hash: str = goloop.set_score_owner(_from, cps_address, GOV_ADDRESS)
        time.sleep(2)
        check_if_tx_succeeded(ptools, tx_hash)

        ret: str = goloop.query_call(SYS_ADDRESS, "getScoreOwner", [f"score={cps_address}"])
        assert ret == GOV_ADDRESS

        # makeProposal
        proposal: str = ptools.make_proposal(name, f"--cps {cps_address}")
        print(proposal)
        obj = json.loads(proposal)
        assert obj["name"] == name
        network_scores: List[Dict[str, str]] = obj["value"]["networkScores"]
        assert len(network_scores) == 1
        assert network_scores[0]["role"] == "cps"
        assert network_scores[0]["address"] == cps_address

        # registerProposal2
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal with agree and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

        ret: Dict[str, Any] = goloop.get_network_scores()
        assert ret["cps"] == cps_address
        assert ret["governance"] == GOV_ADDRESS

    def test_malicious_score_proposal(self, env: Env):
        ptools = env.ptools
        goloop = env.goloop
        _from = env.god
        name = "maliciousScore"
        address = env.cps_address
        title, desc = "title", "desc"

        for _type in (0, 1):
            # makeProposal
            proposal: str = ptools.make_proposal(name, f"{address} {_type}")
            obj = json.loads(proposal)
            assert obj["name"] == name
            value: Dict[str, str] = obj["value"]
            assert value["address"] == address
            assert value["type"] == hex(_type)

            # registerProposal2
            proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
            time.sleep(2)
            check_if_register_proposal_tx_succeeded(
                ptools, proposal_id, title, desc, _from, proposal,
            )

            # voteProposal and applyProposal
            vote_and_apply_proposal(ptools, _from, proposal_id)

            # getScoreStatus
            ret: str = goloop.query_call(
                to=GOV_ADDRESS,
                method="getScoreStatus",
                params=[f"address={address}"]
            )
            result: Dict[str, Any] = json.loads(ret)
            assert result["blocked"] == hex(not _type)

    def test_prep_disqualification_proposal(self, env: Env):
        ptools = env.ptools
        _from: Account = env.preps[0]
        prep: Account = env.preps[1]
        name = "prepDisqualification"
        title, desc = "title", "desc"

        # makeProposal
        proposal: str = ptools.make_proposal(name, prep.address)
        obj = json.loads(proposal)
        assert obj["name"] == name
        assert obj["value"]["address"] == prep.address

        # registerProposal2
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

    def test_accumulated_validation_failure_slashing_rate_proposal(self, env: Env):
        ptools = env.ptools
        _from = env.god

        name = "accumulatedValidationFailureSlashingRate"
        slashing_rate = 1
        proposal: str = ptools.make_proposal(name, options=f"{slashing_rate}")
        obj = json.loads(proposal)
        assert obj["name"] == name
        assert obj["value"]["slashingRate"] == hex(slashing_rate)

        # registerProposal2
        title, desc = "title", "desc"
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

    def test_missed_network_proposal_slashing_rate_proposal(self, env: Env):
        ptools = env.ptools
        _from = env.god

        name = "missedNetworkProposalSlashingRate"
        slashing_rate = 1
        proposal: str = ptools.make_proposal(name, options=f"{slashing_rate}")
        obj = json.loads(proposal)
        assert obj["name"] == name
        assert obj["value"]["slashingRate"] == hex(slashing_rate)

        # registerProposal2
        title, desc = "title", "desc"
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

        # TODO: Need to check if "SlashingRateChanged" eventlog si recorded

    def test_step_price_proposal(self, env: Env):
        ptools = env.ptools
        goloop = env.goloop
        _from = env.god

        name = "stepPrice"
        step_price = goloop.get_step_price() + 1

        # makeProposal
        proposal: str = ptools.make_proposal(name, options=f"{step_price}")
        print(proposal)
        obj = json.loads(proposal)
        assert obj["name"] == name
        assert obj["value"]["stepPrice"] == hex(step_price)

        # registerProposal2
        title, desc = "title", "desc"
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

        assert goloop.get_step_price() == step_price

    def test_step_costs_proposal(self, env: Env):
        ptools = env.ptools
        goloop = env.goloop
        _from = env.god

        name = "stepCosts"
        step_costs = goloop.get_step_costs()
        default = int(step_costs["default"], base=0) + 1
        get = int(step_costs["get"], base=0) + 1
        get_base = int(step_costs["getBase"], base=0) + 1

        options = (
            f"--get {get} "
            f"--get-base {get_base} "
            f"--default {default}"
        )
        proposal: str = ptools.make_proposal(name, options)
        print(proposal)
        obj = json.loads(proposal)
        step_costs = obj["value"]["costs"]
        assert obj["name"] == name
        assert step_costs["get"] == hex(get)
        assert step_costs["getBase"] == hex(get_base)
        assert step_costs["default"] == hex(default)

        # registerProposal2
        title, desc = "title", "desc"
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

        step_costs: Dict[str, str] = goloop.get_step_costs()
        assert int(step_costs["get"], base=0) == get
        assert int(step_costs["getBase"], base=0) == get_base
        assert int(step_costs["default"], base=0) == default

    def test_reward_fund_proposal(self, env: Env):
        ptools = env.ptools
        goloop = env.goloop
        _from = env.god

        term: Dict[str, Any] = goloop.get_prep_term()

        name = "rewardFund"
        iglobal = int(term["rewardFund"]["Iglobal"], base=0) + 1

        proposal: str = ptools.make_proposal(name, options=f"{iglobal}")
        print(proposal)
        obj = json.loads(proposal)
        assert obj["name"] == name
        assert obj["value"]["iglobal"] == hex(iglobal)

        # registerProposal2
        title, desc = "title", "desc"
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)

    def test_reward_funds_allocation_proposal(self, env: Env):
        ptools = env.ptools
        _from = env.god

        name = "rewardFundsAllocation"
        icps, iprep, irelay, ivoter = 25, 25, 25, 25
        options = (
            f"--icps {icps} "
            f"--iprep {iprep} "
            f"--irelay {irelay} "
            f"--ivoter {ivoter}"
        )

        proposal: str = ptools.make_proposal(name, options)
        print(proposal)
        obj = json.loads(proposal)
        assert obj["name"] == name
        reward_funds: Dict[str, str] = obj["value"]["rewardFunds"]
        assert reward_funds["icps"] == hex(icps)
        assert reward_funds["iprep"] == hex(iprep)
        assert reward_funds["irelay"] == hex(irelay)
        assert reward_funds["ivoter"] == hex(ivoter)

        # registerProposal2
        title, desc = "title", "desc"
        proposal_id: str = ptools.register_proposal2(_from, title, desc, [proposal])
        assert is_tx_hash(proposal_id)
        time.sleep(2)
        check_if_register_proposal_tx_succeeded(
            ptools, proposal_id, title, desc, _from, proposal,
        )

        # voteProposal and applyProposal
        vote_and_apply_proposal(ptools, _from, proposal_id)
