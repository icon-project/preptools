[![unittest](https://img.shields.io/github/actions/workflow/status/icon-project/preptools/preptools-workflow.yml?branch=master&label=unittest&logo=github)](https://github.com/icon-project/preptools/actions/workflows/preptools-workflow.yml)
[![PyPI - latest](https://img.shields.io/pypi/v/preptools?label=latest&logo=pypi)](https://pypi.org/project/preptools)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/preptools?logo=pypi)](https://pypi.org/project/preptools)

# P-Rep tools (preptools) Tutorial

* This document is intended to explain how to use preptools.
* This guide will walk through the basics of setting up the development environment and the usage of preptools CLI commands.

## Building from source

First, clone this project. Then go to the project directory, create a virtualenv environment, and run the build script. Then install preptools with the .whl file.
```bash
$ python -m venv venv             # Create a virtual environment.
$ source venv/bin/activate        # Enter the virtual environment.
(venv) $ ./build.sh                # run build script.
(venv) $ ls dist                   # check result wheel file.
preptools-x.y.z-py3-none-any.whl
```

## Installation

This chapter explains how to install P-Rep Tools on your system.

### Requirements

* OS: MacOS or Linux
* Windows is not supported.
* Python
  * Make a virtualenv for Python 3.7+
  * Check your Python version
    ```bash
    $ python3 -V
    ```

### Setup

#### Install dependencies

Some native tools and libraries are needed to install preptools without any errors.

```bash
$ sudo apt-get install -y libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev libyaml-cpp-dev
$ sudo apt-get install -y python3.7-dev libsecp256k1-dev python3-pip 
```

#### Install preptools

Install the preptools with the .whl file as below.

```bash
(venv) $ pip install dist/preptools-x.x.x-py3-none-any.whl
```

Install the preptools with pypi
```bash
(venv) $ pip install preptools
```

## How to use P-Rep tools

### Usage

```bash
(venv) $ preptools --help
usage: preptools [-h] command ...

P-Rep management command line interface v1.3.2

optional arguments:
  -h, --help         show this help message and exit

Available commands:
  command
    registerPRep     Register P-Rep (WARNING: A registration fee of 2000 ICX is required)
    unregisterPRep   Unregister P-Rep (WARNING: Unregistering P-Rep does not return the registration fee)
    setPRep          Update the P-Rep information
    getPRep          Get the P-Rep information
    getPReps         Get status of all registered P-Rep candidates
    cancelProposal   Cancel Proposal
    voteProposal     Vote Proposal
    applyProposal    Apply the approved network proposal indicated by id to the network
    makeProposal     Make contents of a given network proposal
    registerProposal2
                     Register network proposals in a new format (WARNING: A submission fee of 100 ICX is required)
    getProposal      Query a proposal information with transaction hash
    getProposals     Query multiple network proposals.
    setStake         Set stake value
    getStake         Get stake value
    setBond          Set bond configuration
    getBond          Get bond configuration
    setBonderList    Set allowed bonder list of P-Rep
    getBonderList    Get allowed bonder list of P-Rep
    txresult         Get transaction result by hash
    txbyhash         Get transaction by hash
    keystore         Create keystore file in the specified path.
    genconf          Create config file in the specified path.
```

### Common options

This table explains common options used in most of the commands.

| shorthand, Name   | default                      | Description                                                                                                                                     |
|:------------------|:-----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|
| -h, --help        |                              | show this help message and exit                                                                                                                 |
| -u, --url         | http://127.0.0.1:9000/api/v3 | node url                                                                                                                                        |
| -n, --nid         | 3                            | network id                                                                                                                                      |
| -c, --config      | ./preptools_config.json      | preptools config file path                                                                                                                      |
| -y, --yes         |                              | Do not confirm if you want to send request                                                                                                      |
| -v, --verbose     |                              | verbose mode flag                                                                                                                               |
| -p, --password    |                              | keystore password                                                                                                                               |
| -k, --keystore    |                              | keystore file path                                                                                                                              |
| -s, --step-limit  | estimated step               | step limit to set. If not exists, preptools will estimate stepLimit properly.                                                                   |
| -m, --step-margin |                              | Can be used when step-limit option is not given. If step-margin is given, `estimated step + step-margin` will be used as step-limit internally. |

### P-Rep commands

* There are 3 commands to set up the P-Rep information:
`registerPRep`, `unregisterPRep`, and `setPRep`.
* Whenever the commands are called, they load the configuration from `preptools_config.json`.
* In order to use other configuration file, please specify the file location with the `-c` option.

#### registerPRep

*Description*

* Registers P-Rep.
* There are two ways of registering a P-Rep.   
  * Using command line option  
    Input P-Rep information with --[OPT_NAME] OPT_VALUE.  
    The order of priority is command line > json 
  * Using json file  
    Input P-Rep information with --prep-json JSON_PATH.

*Usage*
    
```bash
usage: preptools registerPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                              [--yes] [--verbose] [--password PASSWORD]
                              [--keystore KEYSTORE]
                              [--step-limit STEP_LIMIT, -s STEP_LIMIT] [--name [NAME]]
                              [--country COUNTRY] [--city CITY]
                              [--email EMAIL] [--website WEBSITE]
                              [--details DETAILS] [--p2p-endpoint P2PENDPOINT]
                              [--node-address NODEADDRESS]
                              [--prep-json [PREP_JSON]]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
  --name [NAME]         P-Rep name
  --country COUNTRY     P-Rep's country
  --city CITY           P-Rep's city
  --email EMAIL         P-Rep's email
  --website WEBSITE     P-Rep's homepage url
  --details DETAILS     json url including P-Rep detailed information
  --p2p-endpoint P2PENDPOINT
                        Network info used for connecting among P-Rep nodes
  --node-address NODEADDRESS
                        PRep Node Key
  --prep-json [PREP_JSON]
                        json file having P-Rep information
```

*Options*

| shorthand, Name | default | Description                                                                                                           |
|:----------------|:--------|:----------------------------------------------------------------------------------------------------------------------|
| --name          |         | P-Rep name                                                                                                            |
| --country       |         | P-Rep's country<br>See [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard                |
| --city          |         | P-Rep's city<br>ex) Seoul, Tokyo, "New York"                                                                          |
| --email         |         | P-Rep's email<br>ex) "example@iconloop.com"                                                                           |
| --website       |         | P-Rep's homepage url<br>ex) "https://node.example.com/"                                                               |
| --details       |         | json url including P-Rep detailed information<br>ex) "https://node.example.com/json"                                  |
| --p2p-endpoint  |         | `Deprecated` Network info used for connection among P-Rep nodes<br>ex) “123.45.67.89:7100” or “node.example.com:7100” |
| --node-address  |         | PRep Node Key (default: Operator Key)                                                                                 |
| --prep-json     |         | json file having P-Rep information                                                                                    |

*Example*

```bash
(venv) $ cat registerPRep.json 
{
    "name": "banana node",
    "country": "USA",
    "city": "New York",
    "email": "banana@example.com",
    "website": "https://icon.banana.com",
    "details": "https://icon.banana.com/json",
    "p2pEndpoint": "node.example.com:7100",
    "nodeAddress": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
}

(venv) $ preptools registerPRep -k test_keystore --prep-json registerPRep.json 
> Password: 
[Request] ======================================================================
{
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 2000000000000000000000,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "registerPRep",
    "data_type": "call",
    "params": {
        "name": "banana node",
        "country": "USA",
        "city": "New York",
        "email": "banana@example.com",
        "website": "https://icon.banana.com",
        "details": "https://icon.banana.com/json",
        "p2pEndpoint": "node.example.com:7100",
        "nodeAddress": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d400"
    }
}

> Continue? [Y/n]
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0xe667b8de967e4c5e2cc5f4fc2775766f87517935e0875a8c4d0b9c8c2ce01846",
    "id": 1234
}

(venv) $ cat registerPRep.json 
{
    "email": "banana@example.com",
    "website": "https://icon.banana.com",
    "details": "https://icon.banana.com/json",
    "p2pEndpoint": "node.example.com:7100",
    "nodeAddress": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d400"
}

(venv) $ preptools registerPRep -k test_keystore --prep-json registerPRep.json --name "kokoa node"
> Password: 
 > country : USA
 > city : New York
[Request] ======================================================================
{
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 2000000000000000000000,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "registerPRep",
    "data_type": "call",
    "params": {
        "email": "banana@example.com",
        "website": "https://icon.banana.com",
        "details": "https://icon.banana.com/json",
        "p2pEndpoint": "node.example.com:7100",
        "name": "kokoa node",
        "country": "USA",
        "city": "New York"
    }
}

> Continue? [Y/n]
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0xeb00ea0ad9ee155067f37015d2403067904649a76a35dd06197600e408d30e3e",
    "id": 1234
}
```

#### unregisterPRep

*Description*

Unregisters a P-Rep.  

*Usage*

```bash
usage: preptools unregisterPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                                [--yes] [--verbose] [--password PASSWORD]
                                [--keystore KEYSTORE]
                                [--step-limit STEP_LIMIT, -s STEP_LIMIT]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
```

*Example*

```bash
(venv) $ preptools unregisterPRep -k test_keystore 
> Password: 
[Request] ======================================================================
{
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "unregisterPRep",
    "data_type": "call",
    "params": {}
}

> Continue? [Y/n]
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0x027038296f595aedd1bfa680de2e20c3fd133816f9c74807e440bf6c548fb9aa",
    "id": 1234
}
```

#### setPRep

*Description*  

* Change enrolled P-Rep information.  
* There are three ways of set P-Rep.   
  - Using command line option  
    You can input P-Rep information with --[OPT_NAME] OPT_VALUE.  
    The order of priority is command line > json. 
    
  - Using json file  
    You can input P-Rep information with --prep-json JSON_PATH.  
    
  - Using interactive mode [--i]  
    Activate interactive mode and input P-Rep info what you want.   
    If you don't want to input, just enter.

*Usage*

```bash
usage: preptools setPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                         [--yes] [--verbose] [--password PASSWORD]
                         [--keystore KEYSTORE] [--step-limit STEP_LIMIT, -s STEP_LIMIT]
                         [-i] [--name NAME] [--country COUNTRY] [--city CITY]
                         [--email EMAIL] [--website WEBSITE]
                         [--details DETAILS] [--p2p-endpoint P2PENDPOINT]
                         [--node-address NODEADDRESS]
                         [--prep-json PREP_JSON]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
  -i, --interactive     Activate interactive mode when prep fields are blank.
  --name NAME           PRep name
  --country COUNTRY     P-Rep's country
  --city CITY           P-Rep's city
  --email EMAIL         P-Rep's email
  --website WEBSITE     P-Rep's homepage url
  --details DETAILS     json url including P-Rep details information
  --p2p-endpoint P2PENDPOINT
                        Network info used for connecting among P-Rep nodes
  --node-address NODEADDRESS
                        PRep Node Key (Default: Own Address)
  --prep-json PREP_JSON
                        json file including P-Rep information
```

*Options*

Refer to [registerPRep options](#registerprep)

*Example*

```bash
(venv) $ cat setPRep.json 
{
    "name": "kokoa node",
    "country": "USA",
    "website": "https://icon.kokoa.com",
    "details": "https://icon.kokoa.com/json",
    "p2pEndpoint": "node.example.com:7100",
    "nodeAddress": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d400"
}

(venv) $ preptools setPRep -k test_keystore --prep-json setPRep.json 
> Password: 
[Request] ======================================================================
{
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "setPRep",
    "data_type": "call",
    "params": {
        "name": "kokoa node",
        "country": "USA",
        "website": "https://icon.kokoa.com",
        "details": "https://icon.kokoa.com/json",
        "p2pEndpoint": "node.example.com:7100",
	"nodeAddress": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d400"
    }
}

> Continue? [Y/n]
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0xc8456053128897a0941dab4c79428db91dda5a2899e3813698146ac25808c4c9",
    "id": 1234
}

(venv) $ preptools setPRep -k test_keystore --prep-json setPRep.json -i
> Password: 
 > city : New York
 > email : 
[Request] ======================================================================
{
    "from_": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "setPRep",
    "data_type": "call",
    "params": {
        "name": "kokoa node",
        "country": "USA",
        "website": "https://icon.kokoa.com",
        "details": "https://icon.kokoa.com/json",
        "p2pEndpoint": "node.example.com:7100",
        "city": "New York",
	"nodeAddress": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d400"
    }
}

> Continue? [Y/n]
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0xff0c4b603a2ae5ba50f658e0d0188210a5afeec559e44df29b55806342fa4563",
    "id": 1234
}
```

#### setBonderList

*Description*

Sets bonderList up to 10 addresses which can post the bond

*Usage*

```bash
usage: preptools setBonderList [-h] [--url URL] [--nid NID] [--config CONFIG]
                               [--yes] [--verbose] [--password PASSWORD]
                               [--keystore KEYSTORE] [--step-limit STEP_LIMIT]
                               --bonder-list BONDERLIST

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
  --bonder-list BONDERLIST
                        list of address. separator is ','
```

*Example*

```bash
(venv) $ preptools setBonderList --bonder-list hxf1ba1be02ff3a15c5b5c63f2bdba810fefb6f0b5,hx7101544346685b37c7bbb56c2c9b8ed56f2895e2,hxa101544346685b37c7bbb56c2c9b8ed56f2895e1
[Request] ======================================================================
{
    "from_": "hx7101544346685b37c7bbb56c2c9b8ed56f2895e2",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 1342177280,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "setBonderList",
    "data_type": "call",
    "params": {
        "bonderList": [
            "hxf1ba1be02ff3a15c5b5c63f2bdba810fefb6f0b5",
            "hx7101544346685b37c7bbb56c2c9b8ed56f2895e2",
            "hxa101544346685b37c7bbb56c2c9b8ed56f2895e1"
        ]
    }
}

> Continue? [Y/n]
[Response] =====================================================================
txHash : {'jsonrpc': '2.0', 'result': '0x3825c983b50e42477ba17382d18ddf6e82de59b0b9d2c4813a392d0d758193b7', 'id': 1636530159}
```

### P-Rep information commands

Commands that show the P-Rep information.

#### getPRep

*Description*

Queries P-Rep information

*Usage*

```bash
usage: preptools getPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                         address

positional arguments:
  address               Address of P-Rep you are looking for

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
```

*Example*

```bash
(venv) $ preptools getPRep hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getPRep",
    "params": {
        "address": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
    }
}

request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "status": "0x1",
        "grade": "0x2",
        "name": "kokoa node",
        "country": "USA",
        "city": "New York",
        "stake": "0x0",
        "delegated": "0x0",
        "totalBlocks": "0x0",
        "validatedBlocks": "0x0",
        "irep": "0xa968163f0a57b400000",
        "irepUpdateBlockHeight": "0x58f",
        "lastGenerateBlockHeight": "-0x1",
        "email": "rhkddnjs99@hotmail.com",
        "website": "https://icon.kokoa.com",
        "details": "https://icon.kokoa.com/json",
        "p2pEndpoint": "node.example.com:7100",
        "nodeAddress": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d400"
    },
    "id": 1234
}
```

#### getBonderList

*Description*  

Gets the list of bonders which can post the bond

*Usage*

```bash
usage: preptools getBonderList [-h] [--url URL] [--nid NID] [--config CONFIG]
                               [--yes] [--verbose]
                               address

positional arguments:
  address               Address of P-Rep you are looking for

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
```

*Example*

```bash
(venv) $ preptools getBonderList hx7101544346685b37c7bbb56c2c9b8ed56f2895e2
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getBonderList",
    "params": {
        "address": "hx7101544346685b37c7bbb56c2c9b8ed56f2895e2"
    }
}

[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "bonderList": [
            "hxf1ba1be02ff3a15c5b5c63f2bdba810fefb6f0b5",
            "hx7101544346685b37c7bbb56c2c9b8ed56f2895e2",
            "hxa101544346685b37c7bbb56c2c9b8ed56f2895e1"
        ]
    },
    "id": 1636530914
} 
```

#### getPReps

*Description*  

Gets live status of all registered P-Rep candidates

*Usage*

```bash
usage: preptools getPReps [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [--start-ranking START_RANKING]
                          [--end-ranking END_RANKING]
                          [--block-height BLOCK_HEIGHT]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --start-ranking START_RANKING
                        Get P-Rep list which starts from start ranking
  --end-ranking END_RANKING
                        Get P-Rep list which ends with end ranking, inclusive
  --block-height BLOCK_HEIGHT
                        Block height which ranking formed
```

*Options*

| shorthand, Name | default | Description                                                             |
|:----------------|:--------|:------------------------------------------------------------------------|
| --start-ranking |         | Get P-Rep list which starts from start ranking<br>minimum ranking is 1. |
| --end-ranking   |         | Get P-Rep list which ends with end ranking, inclusive                   |
| --block-height  |         | Block height when ranking formed                                        |

*Example*

```bash
(venv) $ preptools getPReps
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getPReps",
    "params": null
}

request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "blockHeight": "0x1e3f3",
        "startRanking": "0x0",
        "totalDelegated": "0x0",
        "totalStake": "0x0",
        "preps": [
            {
                "name": "Banana node",
                "country": "USA",
                "city": "New York",
                "grade": "0x0",
                "address": "hx8f21e5c54f006b6a5d5fe65486908592151a7c57",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1200",
                "lastGenerateBlockHeight": "-0x1",
                "stake": "0x21e19e0c9bab2400000",
                "delegated": "0x204fce5e3e25026110000000",
                "totalBlocks": "0x2710",
                "validatedBlocks": "0x2328"
            },
            ...
        ]
    },
    "id": 1234
}

(venv) $ preptools getPReps --start-ranking "0x1" --end-ranking "0x8" --block-height "0x1234"
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getPReps",
    "params": {
        "startRanking": "0x1",
        "endRanking": "0x8",
        "blockHeight": "0x1234"
    }
}

request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "blockHeight": "0x1e452",
        "startRanking": "0x0",
        "totalDelegated": "0x0",
        "totalStake": "0x0",
        "preps": [
            {
                "name": "Banana node",
                "country": "USA",
                "city": "New York",
                "grade": "0x0",
                "address": "hx8f21e5c54f006b6a5d5fe65486908592151a7c57",
                "irep": "0xc350",
                "irepUpdateBlockHeight": "0x1200",
                "lastGenerateBlockHeight": "-0x1",
                "stake": "0x21e19e0c9bab2400000",
                "delegated": "0x204fce5e3e25026110000000",
                "totalBlocks": "0x2710",
                "validatedBlocks": "0x2328"
            },
            ...
        ]
    },
    "id": 1234
}
```

### Network Proposal commands

* These commands are designed for network proposal handling.
* Whenever the commands are called, they load the configuration from `preptools_config.json` by default.
* In order to use other configuration file, please specify the file location with the `-c` option.


#### registerProposal2

* The command is used to register network protocols in a new format supported by governance-2.x.x score.
* CAUTION: a proposer must pay a fee of `100 ICX` to submit a proposal to blockchain.
* For more detail on the new protocol specification, refer to [governance2 score registerProposal format](https://github.com/icon-project/governance2#registerproposal).
* The new proposal format will make main P-Reps possible handle multiple proposals with a transaction. 

*Usage*

```bash
(venv) $ preptools registerProposal2 -h                                                                                                                       [14:37:44]
usage: preptools registerProposal2 [-h] [--url URL] [--nid NID]
                                   [--config CONFIG] [--yes] [--verbose]
                                   [--password PASSWORD] [--keystore KEYSTORE]
                                   [--step-limit STEP_LIMIT]
                                   [--step-margin STEP_MARGIN]
                                   [title] [desc] proposals [proposals ...]

positional arguments:
  title                 Proposal title
  desc                  Proposal description
  proposals             Proposal contents in governance2 score format or
                        filepath with '@' prefix, which includes proposal
                        contents

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
  --step-margin STEP_MARGIN, -m STEP_MARGIN
                        Can be used when step-limit option is not given. Set
                        step-limit value to estimated Step + this value(step-
                        margin)
                        
(venv) $ preptools registerProposal2 -c preptools_config.json -k prep_keys0 -p qwer1234% "proposal title" "proposal description" '{"name":"text","value":{"text":"text proposal sample"}' @step_price_proposal.json @reward_fund.json @step_costs.json

(venv) $ cat step_price_proposal.json
{"name":"stepPrice","value":{"stepPrice":"0x2e90edd00"}}

(venv) $ cat reward_fund.json
{"name":"rewardFund","value":{"iglobal":"0x1e8480"}}

(venv) $ cat step_costs.json
{"name":"stepCosts","value":{"get":"0x19","getBase":"0xc8","input":"0xc8"}}
```

#### makeProposal

* This command is used to make a variety of network proposal contents easily.
* Note that it does not have any connection to blockchain while making the content of a specific network proposal.
* The created proposal content is used as a parameter of [registerProposal2](#registerproposal2) command.

*Usage*

```bash
(venv) $ preptools makeProposal -h
usage: preptools makeProposal [-h] proposal ...

optional arguments:
  -h, --help            show this help message and exit

Available proposals:
  proposal
    text                text network proposal
    revision            revision network proposal
    maliciousScore      maliciousScore network proposal
    prepDisqualification
                        prepDisqualification network proposal
    stepPrice           stepPrice network proposal
    stepCosts           stepCosts network proposal
    rewardFund          rewardFund network proposal for Monthly Reward Fund Setting
    rewardFundsAllocation
                        rewardFundsAllocation network proposal to determine the allocation of the monthly reward fund
    networkScoreDesignation
                        networkScoreDesignation network proposal
    networkScoreUpdate  networkScoreUpdate network proposal
    accumulatedValidationFailureSlashingRate
                        accumulatedValidationFailureSlashingRate network proposal
    missedNetworkProposalVoteSlashingRate
                        missedNetworkProposalVoteSlashingRate network proposal
    call                call network proposal
```  
  
*Example*

```bash
(venv) $ preptools makeProposal call -h
usage: preptools makeProposal call [-h] [-o OUTPUT] [--params PARAMS [PARAMS ...]] to method

positional arguments:
  to                    SCORE address
  method                method name to call

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        filepath to save proposal contents
  --params PARAMS [PARAMS ...]
                        Arguments information to be passed to method (TYPE@VALUE[@FIELDS], FIELDS required if parameter is struct or []struct)

(venv) $ preptools makeProposal call cx0000000000000000000000000000000000000000 openBTPNetwork \
    --params str@eth str@sepolia Address@cxf1b0808f09138fffdb890772315aeabb37072a8a
{"name":"call","value":{"to":"cx0000000000000000000000000000000000000000","method":"openBTPNetwork","params":[{"type":"str","value":"eth"},{"type":"str","value":"sepolia"},{"type":"Address","value":"cxf1b0808f09138fffdb890772315aeabb37072a8a"}]}}
```

#### voteProposal

*Description*

* Votes for Network-proposal.
* Refer to [voteProposal request format](https://github.com/icon-project/governance2#voteproposal) for details.

*Usage*

```bash
usage: preptools voteProposal [-h] [--url URL] [--nid NID] [--config CONFIG]
                              [--yes] [--verbose] [--password PASSWORD]
                              [--keystore KEYSTORE]
                              [--step-limit STEP_LIMIT, -s STEP_LIMIT] --id ID --vote VOTE

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
  --id ID               hash of registerProposal TX
  --vote VOTE           0 : disagree, 1 : agree

```

*Example*

```bash
(venv) $ preptools voteProposal -k prep_keys1 --id 0x515d0c7470e56358a6085ca93d305c4c28d004c10d110b26570dadc34bf2e492 --vote 0
> Password:
[Request] ======================================================================
{
    "from_": "hx85d62b91d70bc2390b636a8d64136a413e671e3a",
    "to": "cx0000000000000000000000000000000000000001",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "voteProposal",
    "data_type": "call",
    "params": {
        "id": "0x515d0c7470e56358a6085ca93d305c4c28d004c10d110b26570dadc34bf2e492",
        "vote": 0
    }
}

> Continue? [Y/n]Y
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0x22ca6eb228586ed2a00924f18bc57f1819214bf0d5c5d305b03d72a931360cc8",
    "id": 1234
}
```

#### cancelProposal

*Description*

* Cancels network proposal within the voting period.
* Refer to [cancelProposal request format](https://github.com/icon-project/governance2#cancelproposal) for details.

*Usage*

```bash
usage: preptools cancelProposal [-h] [--url URL] [--nid NID] [--config CONFIG]
                                [--yes] [--verbose] [--password PASSWORD]
                                [--keystore KEYSTORE]
                                [--step-limit STEP_LIMIT, -s STEP_LIMIT] --id [ID]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
  --id [ID]             hash of registerProposal TX
```

*Example*

```bash
(venv) $ preptools cancelProposal -k prep_keys0 --id 0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4
> Password:
[Request] ======================================================================
{
    "from_": "hxb74e29fba1809a105fdec433040a4e713bbe91fe",
    "to": "cx0000000000000000000000000000000000000001",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "cancelProposal",
    "data_type": "call",
    "params": {
        "id": "0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4"
    }
}

> Continue? [Y/n]Y
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0x344887e8b9b30e523991e44602eee51857fd7a55e5437b34a7e8d0f2ede8c019",
    "id": 1234
}
```

#### applyProposal

*Description*

* Applies an approved network proposal to the network.
* It should be executed within the voting period, otherwise the proposal will be expired and cannot be applied anymore.
* Refer to [applyProposal request format](https://github.com/icon-project/governance2#applyproposal) for details.

*Usage*

```bash
(venv) $ preptools applyProposal -h                                                                                                                                                                                                                                           [12:07:48]
usage: preptools applyProposal [-h] [--url URL] [--nid NID] [--config CONFIG]
                               [--yes] [--verbose] [--password PASSWORD]
                               [--keystore KEYSTORE] [--step-limit STEP_LIMIT]
                               [--step-margin STEP_MARGIN]
                               id

positional arguments:
  id                    hash of registerProposal TX

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
  --step-margin STEP_MARGIN, -m STEP_MARGIN
                        Can be used when step-limit option is not given. Set
                        step-limit value to estimated Step + this value(step-
                        margin)
```

*Example*

```bash
(venv) $ preptools applyProposal -k prep_keys0 0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4
> Password:
[Request] ======================================================================
{
    "from_": "hxb74e29fba1809a105fdec433040a4e713bbe91fe",
    "to": "cx0000000000000000000000000000000000000001",
    "value": 0,
    "step_limit": 268435456,
    "nid": 3,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "applyProposal",
    "data_type": "call",
    "params": {
        "id": "0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4"
    }
}

> Continue? [Y/n]Y
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0x344887e8b9b30e523991e44602eee51857fd7a55e5437b34a7e8d0f2ede8c019",
    "id": 1234
}
```

### Querying Network Proposal commands

* There are 2 commands for network proposal querying: `getProposal` and `getProposals`.
* Whenever the commands are called, they load the configuration from `preptools_config.json`.
* In order to use other configuration file, please specify the file location with the `-c` option.

#### getProposal

*Description*

* Querying network proposal information with given proposal-id  
* Refer to [getProposal request format](https://github.com/icon-project/governance2#getproposal).

*Usage*

```bash
usage: preptools getProposal [-h] [--url URL] [--nid NID] [--config CONFIG]
                             [--yes] [--verbose]
                             transaction_hash

positional arguments:
  transaction_hash      hash of registerProposal transaction

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
```

*Example*
```bash
(venv) $ preptools getProposal 0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000001",
    "method": "getProposal",
    "params": {
        "id": "0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4"
    }
}

request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "id": "0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4",
        "proposer": "hxb74e29fba1809a105fdec433040a4e713bbe91fe",
        "proposerName": "nodehxb74e29fba1809a105fdec433040a4e713bbe91fe",
        "status": "0x0",
        "startBlockHeight": "0x2c",
        "endBlockHeight": "0x2f",
        "contents": {
            "title": "pro0",
            "description": "first proposal",
            "type": "0x4",
            "value": {
                "value": "1234"
            }
        },
        "vote": {
            "agree": {
                "list": [],
                "amount": "0x0"
            },
            "disagree": {
                "list": [],
                "amount": "0x0"
            },
            "noVote": {
                "list": [
                    "hxb74e29fba1809a105fdec433040a4e713bbe91fe",
                    "hx85d62b91d70bc2390b636a8d64136a413e671e3a",
                    "hxd891096dd01c1af790c29d55022a35357684643c",
                    "hx44ae89b457ccfb1bacbe35d278933ba887373b1b",
                    "hxf2c6b56e6dfcfe7c3b9fbd3d1ca1d08973b8d363",
                    "hxe54bdf4b25affa59c8963f1e4a6c45183aee167f",
                    "hx02ccb9e378a35e11a65b5c60e796fded98383b37",
                    "hx064c3d9b4982aae0253b9a8b3dd106823c107c25",
                    "hxcd294f136f39232d97081f2dfa22886c76f45afb",
                    "hxd685153db2a09347115cf0d8d1c5f9ab174bd802",
                    "hx383b555e0301b77b1c326815bccaaaf382ecd238",
                    "hxb0bfb180fb60ac68a0d3dbcadf509af07dd1f501",
                    "hxa5861173d2bd05dd9bfc5c5d74faa654f8d37c7b",
                    "hxee194a44eb4d06fb7c8a9515f74eb41735046be2",
                    "hx6e220a1b6c0fc12b2d3cc6122fccf2e9ec3d1406",
                    "hxa46f74425c0e588be8c93bbabf1be2c67da12066",
                    "hx81c5db07cd6c1c569e0a5abebdb7b108157d80b5",
                    "hx46ca63475e630e7c3a8c3f8c0e2981b675f32919",
                    "hxffa3675581c0209c2adcc598767c77d43f999a33",
                    "hx9259b69bbdea01f32e97d91401ada24d12965ae3",
                    "hx282c3778a572d4d0d1eb8e65ab53daaedea3f68e",
                    "hx25b84c8fe8bfabda4fb30523a1923a79cc304af5"
                ],
                "amount": "0x10658da4dff32a862400000"
            }
        }
    },
    "id": 1234
}
```

#### getProposals

*Description*

* Queries multiple network proposals 
* Proposals are listed starting with the most recently registered.
* Refer to [getProposals request format](https://github.com/icon-project/governance2#getproposals)

*Usage*

```bash
usage: preptools getProposals [-h] [--url URL] [--nid NID] [--config CONFIG]
                              [--yes] [--verbose] [--type [TYPE]]
                              [--status [STATUS]]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --type [TYPE]         type of network proposal to filter
  --status [STATUS]     status of network proposal to filter
```

*Options*

| shorthand, Name | default | Description                                                                                                                       |
|:----------------|:--------|:----------------------------------------------------------------------------------------------------------------------------------|
| --type          |         | [Type](https://github.com/icon-project/governance#available-values-for-the-type) of network proposal to filter                    |
| --status        |         | [Status](https://github.com/icon-project/governance/blob/master/governance/network_proposal.py#L15) of network proposal to filter |
| --start         | 0       | Refer to [getProposals/Parameters](https://github.com/icon-project/governance2#parameters-7)                                      |
| --size          | 10      | Number of proposals to query. Refer to [getProposals/Parameters](https://github.com/icon-project/governance2#parameters-7)        |

*Example*

```bash
(venv) $ preptools getProposals
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000001",
    "method": "getProposals",
    "params": null
}

request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "proposals": [
            {
                "id": "0x02221f9346f9c9b3322ea33e67a1ca0fbe9491e0ea3aefb5154a43e2ea829fa4",
                "proposer": "hxb74e29fba1809a105fdec433040a4e713bbe91fe",
                "proposerName": "nodehxb74e29fba1809a105fdec433040a4e713bbe91fe",
                "status": "0x0",
                "startBlockHeight": "0x2c",
                "endBlockHeight": "0x2f",
                "contents": {
                    "title": "pro0",
                    "description": "first proposal",
                    "type": "0x4",
                    "value": {
                        "value": "1234"
                    }
                },
                "vote": {
                    "agree": {
                        "count": "0x0",
                        "amount": "0x0"
                    },
                    "disagree": {
                        "count": "0x0",
                        "amount": "0x0"
                    },
                    "noVote": {
                        "count": "0x16",
                        "amount": "0x10658da4dff32a862400000"
                    }
                }
            },
            {
                "id": "0x515d0c7470e56358a6085ca93d305c4c28d004c10d110b26570dadc34bf2e492",
                "proposer": "hxb74e29fba1809a105fdec433040a4e713bbe91fe",
                "proposerName": "nodehxb74e29fba1809a105fdec433040a4e713bbe91fe",
                "status": "0x0",
                "startBlockHeight": "0x2c",
                "endBlockHeight": "0x2f",
                "contents": {
                    "title": "pro1",
                    "description": "second proposal",
                    "type": "0x4",
                    "value": {
                        "value": "1234"
                    }
                },
                "vote": {
                    "agree": {
                        "count": "0x0",
                        "amount": "0x0"
                    },
                    "disagree": {
                        "count": "0x1",
                        "amount": "0xbecc41ad16b07a7600000"
                    },
                    "noVote": {
                        "count": "0x15",
                        "amount": "0xfa6c16332dc7a0bae00000"
                    }
                }
            }
        ]
    },
    "id": 1234
}
```

### Bond commands

* There are 2 commands to bond: `setStake` and `setBond`.
* Whenever the commands are called, they load the configuration from `preptools_config.json`.
* In order to use other configuration file, please specify the file location with the `-c` option.

#### setStake

*Description*

* Sets stake value of the account

*Usage*

```bash
usage: preptools setStake [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [--yes] [--verbose] [--password PASSWORD]
                          [--keystore KEYSTORE] [--step-limit STEP_LIMIT]
                          value

positional arguments:
  value                 Stake value

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
```

*Example*

```bash
(venv) $ preptools setStake 10000
[Request] ======================================================================
{
    "from_": "hxcad9055c936192554141a0f5f4bb554a97f4d8e1",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 1342177280,
    "nid": 7,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "setStake",
    "data_type": "call",
    "params": {
        "value": 10000
    }
}

> Continue? [Y/n]y
[Response] =====================================================================
txHash : {'jsonrpc': '2.0', 'result': '0xfab066b43f06596fd1bea3ab6effb154fdab3abcff21e4d75a70a62dbbc86053', 'id': 1637130230}
```

#### setBond

*Description*

Sets bond configuration of the account

*Usage*

```bash
usage: preptools setBond [-h] [--url URL] [--nid NID] [--config CONFIG]
                         [--yes] [--verbose] [--password PASSWORD]
                         [--keystore KEYSTORE] [--step-limit STEP_LIMIT]
                         bond [bond ...]

positional arguments:
  bond                  Bond configurations. PREP_ADDRESS,VALUE (Max: 100)

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --step-limit STEP_LIMIT, -s STEP_LIMIT
                        step limit to set
```

*Example*

```bash
(venv) $ preptools setBond hx4ffe89ff27a21276a3c7e23eef2ced3d3072d7c9,500 hx7ded18f4c3d1740137684d8109cf8444f89053e5,500
[Request] ======================================================================
{
    "from_": "hxcad9055c936192554141a0f5f4bb554a97f4d8e1",
    "to": "cx0000000000000000000000000000000000000000",
    "value": 0,
    "step_limit": 1342177280,
    "nid": 7,
    "nonce": null,
    "version": 3,
    "timestamp": null,
    "method": "setBond",
    "data_type": "call",
    "params": {
        "bonds": [
            {
                "address": "hx4ffe89ff27a21276a3c7e23eef2ced3d3072d7c9",
                "value": "0x1f4"
            },
            {
                "address": "hx7ded18f4c3d1740137684d8109cf8444f89053e5",
                "value": "0x1f4"
            }
        ]
    }
}

> Continue? [Y/n]
[Response] =====================================================================
txHash : {'jsonrpc': '2.0', 'result': '0xd2bb1dfbf03a68adaa36a35a8544e90035b93e293fa60611aa0f815420895e9b', 'id': 1637130338}
```

### Querying bond commands

#### getStake

*Description*

Get stake value of the account

*Usage*

```bash
usage: preptools getStake [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [--yes] [--verbose]
                          address

positional arguments:
  address               Address of you are looking for

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
```

*Example*

```bash
(venv) $ preptools getStake hxcad9055c936192554141a0f5f4bb554a97f4d8e1                                                         *[master]
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getStake",
    "params": {
        "address": "hxcad9055c936192554141a0f5f4bb554a97f4d8e1"
    }
}

[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "stake": "0x2710",
        "unstakes": []
    },
    "id": 1637130254
}
```

#### getBond

*Description*

Gets bond configuration of the account

*Usage*

```bash
usage: preptools getBond [-h] [--url URL] [--nid NID] [--config CONFIG]
                         [--yes] [--verbose]
                         address

positional arguments:
  address               Address of you are looking for

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --yes, -y             Don't want to ask send transaction.
  --verbose, -v         Verbose mode
```

*Example*

```bash
(venv) $ preptools getBond hxcad9055c936192554141a0f5f4bb554a97f4d8e1                                                          *[master]
[Request] ======================================================================
{
    "from_": "hx1234567890123456789012345678901234567890",
    "to": "cx0000000000000000000000000000000000000000",
    "method": "getBond",
    "params": {
        "address": "hxcad9055c936192554141a0f5f4bb554a97f4d8e1"
    }
}

[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "bonds": [
            {
                "address": "hx4ffe89ff27a21276a3c7e23eef2ced3d3072d7c9",
                "value": "0x1f4"
            },
            {
                "address": "hx7ded18f4c3d1740137684d8109cf8444f89053e5",
                "value": "0x1f4"
            }
        ],
        "unbonds": []
    },
    "id": 1637131982
}
```

### Preptools Common commands

Commands that generate configuration file and keystore file. There are two commands `keystore` and `genconf`.

#### keystore

*Description*

Creates a keystore file in the given path.

*Usage*

```bash
usage: preptools keystore [-h] [-p PASSWORD] path

positional arguments:
  path                  Path of keystore file.

optional arguments:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        Keystore file's password
```

*Example*

```bash
(venv) $ preptools keystore keystore_file
Input your keystore password:
Retype your keystore password:
Made file successfully
```

#### genconf

*Description*

Generates P-Rep tools config file.

*Usage*

```bash
usage: preptools genconf [-h] [--path PATH]

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  Path of configue file. default(./preptools_config.json)
```

*Example*

```bash
(venv) $ preptools genconf
Made ./preptools_config.json successfully
(venv) $ cat ./preptools_config.json
{
    "url": "http://127.0.0.1:9000/api/v3",
    "nid": 3,
    "keystore": null
}
```

### Preptools Other commands

Commands that are related to transaction. There are two commands `txresult` and `txbyhash`.

#### txresult

*Description*

Gets transaction result by transaction hash.

*Usage*

```bash
usage: preptools txresult [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [tx_hash]

positional arguments:
  tx_hash               Enter the transaction hash

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
```

*Example*

```bash
(venv) $ preptools txresult 0xc8456053128897a0941dab4c79428db91dda5a2899e3813698146ac25808c4c9
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "txHash": "0xc8456053128897a0941dab4c79428db91dda5a2899e3813698146ac25808c4c9",
        "blockHeight": "0x1d980",
        "blockHash": "0xa7354fb9427308239e56482916dd4e31988ce1f207091cdf81c656f89a066c5f",
        "txIndex": "0x0",
        "to": "cx0000000000000000000000000000000000000000",
        "stepUsed": "0x21340",
        "stepPrice": "0x2540be400",
        "cumulativeStepUsed": "0x21340",
        "eventLogs": [
            {
                "scoreAddress": "cx0000000000000000000000000000000000000000",
                "indexed": [
                    "PRepSet(Address)"
                ],
                "data": [
                    "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6"
                ]
            }
        ],
        "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000080000000000000000000000000000000000000000000000000000000000020000000000000008000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "status": "0x1"
    },
    "id": 1234
}
```

#### txbyhash

*Description*

Gets transaction by transaction hash

*Usage*

```bash
usage: preptools txbyhash [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [tx_hash]

positional arguments:
  tx_hash               Enter the transaction hash

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default(http://127.0.0.1:9000/api/v3)
  --nid NID, -n NID     networkId default(3) ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
```

*Example*

```bash
(venv) $ preptools txbyhash 0xc8456053128897a0941dab4c79428db91dda5a2899e3813698146ac25808c4c9
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": {
        "version": "0x3",
        "from": "hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6",
        "to": "cx0000000000000000000000000000000000000000",
        "stepLimit": "0x10000000",
        "timestamp": "0x58fa97a48ad43",
        "nid": "0x3",
        "value": "0x0",
        "dataType": "call",
        "data": {
            "method": "setPRep",
            "params": {
                "name": "kokoa node",
                "country": "USA",
                "website": "https://icon.kokoa.com",
                "details": "https://icon.kokoa.com/json",
                "p2pEndpoint": "node.example.com:7100"
            }
        },
        "signature": "4krblW9KtQr6KNIJOVa22B3JFDQD6vaxepDSjMET91oua3Qeiq3UFMIHiucWiIrKGt3zaSo2K+mVW7Ge5rOtPwE=",
        "txHash": "0xc8456053128897a0941dab4c79428db91dda5a2899e3813698146ac25808c4c9",
        "txIndex": "0x0",
        "blockHeight": "0x1d980",
        "blockHash": "0xa7354fb9427308239e56482916dd4e31988ce1f207091cdf81c656f89a066c5f"
    },
    "id": 1234
}
```

### Configuration Files

#### preptools_config.json

* For every P-Rep tools CLI commands except `genconf` and `keystore`, this file is used to configure the default parameters and initial settings.
* In this configuration file, you can define default options values for some CLI commands. 

```json
{
    "uri": "http://127.0.0.1:9000/api/v3",
    "nid": 3,
    "keyStore": null
}
```

| Field    | Data  type | Description                                |
|:---------|:-----------|:-------------------------------------------|
| uri      | string     | URI to send the request.                   |
| nid      | int        | Network ID. 3 is reserved for P-Rep tools. |
| keyStore | string     | Keystore file path.                        |

## JSON Standard for Public Representative Detailed Information 

This is the JSON standard for detailed information about the P-Rep. P-Rep can submit the url of detailed information via the `registerPRep` and `setPRep` action on the ICON Blockchain. We strongly recommend that you register this information.

```json
{
    "representative": {
        "logo": {
            "logo_256": "https://icon.foundation/img/img-256.png",
            "logo_1024": "https://icon.foundation/img/img-1024.png",
            "logo_svg": "https://icon.foundation/img/img-logo.svg"
        },
        "media": {
            "steemit": "",
            "twitter": "",
            "youtube": "",
            "facebook": "",
            "github": "",
            "reddit": "",
            "keybase": "",
            "telegram": "",
            "wechat": ""
        }
    },
    "server": {
        "location": {
            "country": "",
            "city": ""
        },
        "server_type": "",
        "api_endpoint": ""
    }
}
```

- representative: Basic information of Public Representative
  - logo: Logo images of P-Rep
    -  logo_256: image 256x256px
    -  logo_1024: image 1024x1024px
    -  logo_sgv: image svg
  - media: URL and username of social media
    -  steemit: Steemit URL
    -  twitter: Twitter URL
    -  youtube: Youtube URL
    -  Facebook: Facebook URL
    -  github: Github URL
    -  reddit: Raddit URL
    -  keybase: Username
    -  telegram: Username
    -  wechat: Username
- server: Server information of Public Representative
  - location: Server location
    -  name: Node location in human-readable format [City, State]
    -  country: Node country code [XX]
  - server_type: Type of server ‘cloud, on-premise, hybrid’
  - api_endpoint: HTTP endpoint `http://host:port`

### How to use

Create a JSON file and upload it to your domain server. When you call the `registerPRep` or `setPRep` function, input the url of this file into the `details` field.

## References

- [ICON Chain SCORE API](https://github.com/icon-project/goloop/blob/master/doc/icon_chainscore_api.md)
- [Governance-2.x SCORE](https://github.com/icon-project/governance2)
- [ICON SDK PYTHON](https://github.com/icon-project/icon-sdk-python)

## License

This project follows the Apache 2.0 License. Please refer to [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) for details.
