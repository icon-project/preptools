# P-Rep tools (preptools) Tutorial

This tutorial is intended to give an introduction to using preptools. this guide will walk you through the basics of setting up
your development environment and the the usage of preptools CLI commands.

## Building from source
First, clone this project. Then go to the project directory, create a virtualenv environment, and run build script. You can then install preptools with the .whl file.
```
$ python -m venv venv             # Crate a virtual environment.
$ source venv/bin/activate        # Enter the vitual environment.
(venv)$ ./build.sh                # run build script.
(venv)$ ls dist                   # check result wheel file.
preptools-1.0.0-py3-none-any.whl
```

## Installation
This chapter will explain how to install T-Bears on your system.

### Requirements

* OS: MacOS or Linux
  * Windows is not supported.

* Python
  * Make a virtualenv for Python 3.6.5+ (3.7 is also supported)
  * Check your Python version
    ```bash
    $ python3 -V
    ```
### Setup
In case of install, you can install with wheel file that you've built.
```
$ pip install dist/preptools-1.0.0-py3-none-any.whl
```

## How to use P-Rep tools

### Command-line Interfaces (CLIs)

#### Overview
Preptools provides 7 commands. Here is the available commands list.

#### Usage

```
usage: preptools [-h] command                 
                 ...

P-Rep management cli

optional arguments:
  -h, --help                show this help message and exit

subcommands:
    registerPRep        Register P-Rep
    unregisterPRep      Unregister P-Rep
    setPRep             Change enrolled P-Rep information
    setGovernanceVariables
                        Change Governance variables used in network operation
    getPRep             Inquire P-Rep information
    getPReps            Get live status of all registered P-Rep candidates
    txresult            Get transaction result by hash
    txbyhash            Get transaction by hash
    keystore            Create keystore file in the specified path.
    genconf             Create config file in the specified path.
```

#### Options

| shorthand, Name | default | Description                     |
| :-------------- | :------ | :------------------------------ |
| -h, --help      |         | Show this help message and exit |


### Preptools setting commands

Commands that setting the P-Rep info. There are four commands `preptools registerPRep`, `preptools unregisterPRep`, 
`preptools setPRep` and `preptools setGovernanceVariables`. 
Whenever this commands are called, it loads the configuration from `preptools_config.json`.
If you want to use other configuration file, you can specify the file location with the `-c` option.
#### preptools registerPRep

**Description**

Register P-Rep.   
There are three way of register P-Rep.   
  - Using command line option  
    You can input P-Rep information with --[OPT_NAME] OPT_VALUE.  
    The priority of json and command line is command line > json 
     
  - Using json file  
    You can input P-Rep information with --prep-json JSON_PATH.  
    
    
  - Using interactive mode  
    If any information that have to entered remain, interactive mode activate and get P-Rep information.

**Usage**

```bash
usage: preptools registerPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                              [--password PASSWORD] [--keystore KEYSTORE]
                              [--name NAME] [--country COUNTRY] [--city CITY]
                              [--email EMAIL] [--website WEBSITE]
                              [--details DETAILS] [--p2p-endpoint P2PENDPOINT]
                              [--prep-json PREP_JSON]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --name NAME           P-Rep name
  --country COUNTRY     P-Rep's country
  --city CITY           P-Rep's city
  --email EMAIL         P-Rep's email
  --website WEBSITE     P-Rep's homepage url
  --details DETAILS     P-Rep off-chain details
  --p2p-endpoint P2PENDPOINT
                        Network info used for connecting among P-Rep nodes
  --prep-json PREP_JSON
                        json file having P-Rep information
```

**Options**

| shorthand, Name | default                     | Description                                                           |
| :-------------- | :-------------------------- | :---------------------------------------------------------------------|
| -h, --help      |                             | show this help message and exit                                       |
| -u, --url       | http://127.0.0.1/api/v3     | node url                                                              |
| -n, --nid       | 3                           | network id                                                            |
| -c, --config    | ./preptools_config.json     | preptools config file path                                            |
| -p, --password  |                             | keystore password                                                     |
| -k, --keystore  |                             | keystore file path                                                    |
| --name          |                             | P-Rep name                                                            |
| --country       |                             | P-Rep's country. This require [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard.|
| --city          |                             | P-Rep's city.                                                         |
| --email         |                             | P-Rep's email.                ex) "example@iconloop.com"              |
| --website       |                             | P-Rep's homepage url.         ex) "https://node.example.com/"         |
| --details       |                             | P-Rep off chain details.      ex) "https://node.example.com/json"     |
| --p2p-endpoint  |                             | Network info used for connection among P-Rep nodes.                   |
|                 |                             |                               ex) “123.45.67.89:7100” or “node.example.com:7100”|
| --prep-json     |                             | json file having P-Rep information                                    |

**Examples**
```bash
(venv) $ cat registerPRep.json 
{
    "name": "banana node",
    "country": "USA",
    "city": "New York",
    "email": "banana@example.com",
    "website": "https://icon.banana.com",
    "details": "https://icon.banana.com/json",
    "p2pEndpoint": "node.example.com:7100"
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
        "p2pEndpoint": "node.example.com:7100"
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
    "p2pEndpoint": "node.example.com:7100"
}

(venv) preptools registerPRep -k test_keystore --prep-json registerPRep.json --name "kokoa node"
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

#### preptools unregisterPRep

**Description**

Unregister P-Rep.  


**Usage**
```bash
usage: preptools unregisterPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                                [--password PASSWORD] [--keystore KEYSTORE]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
```

**Options**

| shorthand, Name | default                     | Description                                          |
| :-------------- | :-------------------------- | :--------------------------------------------------- |
| -h, --help      |                             | show this help message and exit                      |
| -u, --url       | http://127.0.0.1/api/v3     | node url                                             |
| -n, --nid       | 3                           | network id                                           |
| -c, --config    | ./preptools_config.json     | preptools config file path                           |
| -p, --password  |                             | keystore password                                    |
| -k, --keystore  |                             | keystore file path                                   |


**Examples**

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

#### preptools setPRep

**Description**  

Change enrolled P-Rep information.  
There are three way of set P-Rep.   
  - Using command line option  
    You can input P-Rep information with --[OPT_NAME] OPT_VALUE.  
    The priority of json and command line is command line > json 
     
  - Using json file  
    You can input P-Rep information with --prep-json JSON_PATH.  
    
    
  - Using interactive mode [--i]  
    Activate interactive mode and input P-Rep info what you want.   
    If you don't want to input, just enter.

**Usage**

```bash
usage: preptools setPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                         [--password PASSWORD] [--keystore KEYSTORE] [-i]
                         [--name NAME] [--country COUNTRY] [--city CITY]
                         [--email EMAIL] [--website WEBSITE]
                         [--details DETAILS] [--p2p-endpoint P2PENDPOINT]
                         [--prep-json PREP_JSON]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  -i, --interactive     Activate interactive mode when prep fields are blank.
  --name NAME           PRep name
  --country COUNTRY     P-Rep's country
  --city CITY           P-Rep's city
  --email EMAIL         P-Rep's email
  --website WEBSITE     P-Rep's homepage url
  --details DETAILS     P-Rep off-chain details
  --p2p-endpoint P2PENDPOINT
                        Network info used for connecting among P-Rep nodes
  --prep-json PREP_JSON
                        json file having prepInfo
```

**Options**

| shorthand, Name | default                     | Description                                                           |
| :-------------- | :-------------------------- | :---------------------------------------------------------------------|
| -h, --help      |                             | show this help message and exit                                       |
| -u, --url       | http://127.0.0.1/api/v3     | node url                                                              |
| -n, --nid       | 3                           | network id                                                            |
| -c, --config    | ./preptools_config.json     | preptools config file path                                            |
| -p, --password  |                             | keystore password                                                     |
| -k, --keystore  |                             | keystore file path                                                    |
| -i, --interactive|                            | Activate interactive mode when prep fields are blank.                 |
| --name          |                             | P-Rep name                                                            |
| --country       |                             | P-Rep's country. This require [ISO 3166-1 alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) standard.|
| --city          |                             | P-Rep's city.                                                         |
| --email         |                             | P-Rep's email.                ex) "example@iconloop.com"              |
| --website       |                             | P-Rep's homepage url.         ex) "https://node.example.com/"         |
| --details       |                             | P-Rep off chain details.      ex) "https://node.example.com/json"     |
| --p2p-endpoint  |                             | Network info used for connection among P-Rep nodes.                   |
|                 |                             |                               ex) “123.45.67.89:7100” or “node.example.com:7100”|
| --prep-json     |                             | json file having P-Rep information                                    |


**Examples**
```bash
(venv) $ cat setPRep.json 
{
    "name": "kokoa node",
    "country": "USA",
    "website": "https://icon.kokoa.com",
    "details": "https://icon.kokoa.com/json",
    "p2pEndpoint": "node.example.com:7100"
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
        "p2pEndpoint": "node.example.com:7100"
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
        "city": "New York"
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

#### preptools setGovernanceVariables

**Description**  

Change Governance variables used in network operation  
You can only change it once per term.  
Other items besides irep may be added later.  



**Usage**
```bash
usage: preptools setGovernanceVariables [-h] [--url URL] [--nid NID]
                                        [--config CONFIG]
                                        [--password PASSWORD]
                                        [--keystore KEYSTORE] --irep IREP

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --password PASSWORD, -p PASSWORD
                        keystore password
  --keystore KEYSTORE, -k KEYSTORE
                        keystore file path
  --irep IREP           amounts of irep
```

**Options**

| shorthand, Name | default                     | Description                                          |
| :-------------- | :-------------------------- | :--------------------------------------------------- |
| -h, --help      |                             | show this help message and exit                      |
| -u, --url       | http://127.0.0.1/api/v3     | node url                                             |
| -n, --nid       | 3                           | network id                                           |
| -c, --config    | ./preptools_config.json     | preptools config file path                           |
| -p, --password  |                             | keystore password                                    |
| -k, --keystore  |                             | keystore file path                                   |
| --irep          |                             | amounts of irep                                      |

**Examples**

```bash
(venv) $ preptools setGovernanceVariables --irep 0x0x21e19e0c9bab2400000
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
    "method": "setGovernanceVariables",
    "data_type": "call",
    "params": {
        "irep": "0x0x21e19e0c9bab2400000"
    }
}

> Continue? [Y/n]
request success.
[Response] =====================================================================
{
    "jsonrpc": "2.0",
    "result": "0xc15b6989cd39e01b3d4bb65b72e6f7fcbc009020779b7f9fc60d59da4df7b091",
    "id": 1234
}
```

### Preptools information commands

Commands that show the P-Rep information. There are two commands `preptools getPRep` and `preptools getPReps`.

#### preptools getPRep
**Description**  

Inquire P-Rep information

**Usage**
```bash
usage: preptools getPRep [-h] [--url URL] [--nid NID] [--config CONFIG]
                         address

positional arguments:
  address               Address of P-Rep you are looking for

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
```

**Options**

| shorthand, Name | default                     | Description                                          |
| :-------------- | :-------------------------- | :--------------------------------------------------- |
| -h, --help      |                             | show this help message and exit                      |
| -u, --url       | http://127.0.0.1/api/v3     | node url                                             |
| -n, --nid       | 3                           | network id                                           |
| -c, --config    | ./preptools_config.json     | preptools config file path                           |
| address         |                             | Address of P-Rep you are looking for                 |

**Examples**
```bash
venv) $ preptools getPRep hxef73db5d0ad02eb1fadb37d0041be96bfa56d4e6
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
        "publicKey": "0x040d60ccc4fd29307304a8e84715e6e1a2e643bcff14fbf90d9099dfc84585a6f6f0b6944594efebe433a12a005ba56d215d6e51697a3360b5d741f8db89955c66"
    },
    "id": 1234
}
```

#### preptools getPReps
**Description**  

Get live status of all registered P-Rep candidates

**Usage**
```bash
usage: preptools getPReps [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [--start-ranking START_RANKING]
                          [--end-ranking END_RANKING]
                          [--block-height BLOCK_HEIGHT]

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
  --start-ranking START_RANKING
                        Get P-Rep list which starts from start ranking
  --end-ranking END_RANKING
                        Get P-Rep list which ends with end ranking, inclusive
  --block-height BLOCK_HEIGHT
                        Block height which ranking formed
```

**Options**

| shorthand, Name | default                     | Description                                          |
| :-------------- | :-------------------------- | :--------------------------------------------------- |
| -h, --help      |                             | show this help message and exit                      |
| -u, --url       | http://127.0.0.1/api/v3     | node url                                             |
| -n, --nid       | 3                           | network id                                           |
| -c, --config    | ./preptools_config.json     | preptools config file path                           |
| --start-ranking |                             | Get P-Rep list which starts from start ranking       |
| --end-ranking   |                             | Get P-Rep list which ends with end ranking, inclusive|
| --block-height  |                             | Block height which ranking formed                    |

**Examples**
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

### Preptools Common commands

Commands that generate configuration file and keystore file.

#### preptools keystore

**Description**

Create a keystore file in the given path.

**Usage**

```bash
usage: preptools keystore [-h] [-p PASSWORD] path

positional arguments:
  path                  Path of keystore file.

optional arguments:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        Keystore file's password
```

**Options**

| shorthand, Name | default | Description                              |
| :-------------- | :------ | :--------------------------------------- |
| path            |         | a keystore file path that is to be generated |
| -h, --help      |         | show this help message and exit          |
| -p, --password  |         | Keystore file's password                 |
| path            |         | Path of keystore file                    |

**Examples**

```bash
(work) $ preptools keystore keystore_file
Input your keystore password:
Retype your keystore password:
Made file successfully
```

#### preptools genconf

**Description**

Generate P-Rep tools config file.
 
```bash
usage: preptools genconf [-h] [--path PATH]

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  Path of configue file. default = /preptools_config.json
```

**Options**

| shorthand, Name | default               | Description                     |
| :-------------- | :------               | :------------------------------ |
| -h, --help      |                       | show this help message and exit |
| --path          | preptools_config.json | Path of configue file.          |

**Examples**

```bash
(work) $ preptools genconf
Made ./preptools_config.json successfully
```

### Preptools Other commands

Commands that are related to transaction.

#### preptools txresult

**Description**

Get transaction result by transaction hash.

**Usage**

```bash
usage: preptools txresult [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [tx_hash]

positional arguments:
  tx_hash               Enter the transaction hash

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
```

**Options**

| shorthand, Name | default                      | Description                                                  |
| :-------------- | :--------------------------- | :----------------------------------------------------------- |
| tx_hash         |                              | Hash of the transaction to be queried                        |
| -h, --help      |                              | show this help message and exit                              |
| -u, --url       | http://127.0.0.1:9000/api/v3 | node url                                                     |
| -n, --nid       | 3                            | network id                                                   |
| -c, --config    | ./preptools_config.json      | preptools config file path                                   |

**Examples**

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

#### tbears txbyhash

**Description**

Get transaction by transaction hash

**Usage**

```bash
usage: preptools txbyhash [-h] [--url URL] [--nid NID] [--config CONFIG]
                          [tx_hash]

positional arguments:
  tx_hash               Enter the transaction hash

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -u URL     node url default) http://127.0.0.1:9000/api/v3
  --nid NID, -n NID     networkId default(3 ex) mainnet(1), testnet(2)
  --config CONFIG, -c CONFIG
                        preptools config file path
```

**Options**

| shorthand, Name | default                      | Description                                                  |
| :-------------- | :--------------------------- | :----------------------------------------------------------- |
| tx_hash         |                              | Hash of the transaction to be queried                        |
| -h, --help      |                              | show this help message and exit                              |
| -u, --url       | http://127.0.0.1:9000/api/v3 | node url                                                     |
| -n, --nid       | 3                            | network id                                                   |
| -c, --config    | ./preptools_config.json      | preptools config file path                                   |

**Examples**

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

For every P-Rep tools CLI commands except `genconf` and `keystore`, this file is used to configure the default parameters and initial settings.

In this configuration file, you can define default options values for some CLI commands. 

```json
{
    "uri": "http://127.0.0.1:9000/api/v3",
    "nid": 3,
    "keyStore": null
}
```

| Field              | Data  type | Description                                                  |
| ------------------ | :--------- | :----------------------------------------------------------- |
| uri                | string     | URI to send the request.                                     |
| nid                | int        | Network ID. 3 is reserved for P-Rep tools.                     |
| keyStore           | string     | Keystore file path.                                          |

## References
- [ICON JSON-RPC API v3](https://github.com/icon-project/icon-rpc-server/blob/master/docs/icon-json-rpc-v3.md)
- [ICON Sdk Python](https://github.com/icon-project/icon-sdk-python)

## License

This project follows the Apache 2.0 License. Please refer to [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) for details.