# P-Rep tools (preptools) Tutorial

This tutorial is intended to give an introduction to using preptools. this guide will walk you through the basics of setting up
your development environment and the the usage of preptools CLI commands.

## Building from source
First, clone this project. Then go to the project directory, create a virtualenv environment, and run build script. You can then install preptools with the .whl file.
```
$ python -m venv venv       # Crate a virtual environment.
$ source venv/bin/activate  # Enter the vitual environment.
(venv)$ ./build.sh                # run build script.
(venv)$ ls dist                   # check result wheel file.
preptools-0.0.1-py3-none-any.whl
```

## Installation
In case of Installation, you can install with wheel file that you've built.
```
$ pip install dist/prep-0.0.1-py3-none-any.whl
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
  -h, --help            show this help message and exit

subcommands:
    registerPrep            Register P-Rep
    unregisterPrep          Unregister P-Rep
    setPrep                 Change enrolled P-Rep information
    setGovernanceVariables  Change Governance variables used in network operation
    getPRep                 Inquire P-Rep information
    getPReps                Get live status of all registered P-Rep candidates
    txresult                Get transaction result by transaction hash
    txbyhash                Get transaction by hash
```

#### Options


### Example

```bash
$ cat prep1.json
{       "name": "banana node",
        "email": "banana@example.com",
        "website": "https://icon.banana.com",
        "details": "https://icon.banana.com/json",
        "p2pEndPoint": "123.45.67.89:7100",
}

$ prep register -k ./keystore_test1 -p test1_Account -j ./prep1.json -u http://localhost:9000/api/v3
result:  0x081ea7b7df689ca7a95e33d61eda473c3a238b05829a62d42303b7958f355bf5

$ prep unregister -k ./keystore_test1 -p test1_Account -u http://localhost:9000/api/v3
result:  0x9444ebbfdc4cb552db6cc52a2e95104525466e110eb52ff1215fc43cf32ecad0
```


## Prep 해지

Prep unregister 명령어를 실행하기 위해선 키스토어 파일만 있으면 된다.

### Usage

```bash
$ prep unregister -k [키스토어경로] -p [키스토어 비밀번호(옵셔널)]  -u [노드url(기본값: http:localhost:9000/api/v3)] -a [삭제할 P-rep 주소(builtin-score-owner를 위한 옵션)] -n [nid(기본값:3)] -s [stepLimit(기본값: 200만)]
```

### Example

```bash
$ prep unregister -k keystore_file.json -p password123 -u http://localhost:9000/api/v3
result:  0x9444ebbfdc4cb552db6cc52a2e95104525466e110eb52ff1215fc43cf32ecad0
```


## Prep list 출력

등록되어 있는 PRep들을 출력한다.(j옵션을 사용하지 않는다면 모든 PRep을 출력하고, 사용한다면 설정한만큼의 PRep들만을 출력한다.)

### Usage

```bash
$ prep preps -u [노드url(기본값: http://localhost:9000/api/v3)] -j [참조할 json경로]
```

참조할 json은 getPRepCandidateList 메서드에 파라미터로 넘길 대한 정보를 가지고 있으며, 이 옵션에 값을 넘겨주지 않으면 빈 딕셔너리를 파라미터로 넘긴다.

- json file 예
```json
{
  "startRanking": "0x1",
  "endRanking": "0x10"
}
```

### Example

```bash
$ prep preps -u http://localhost:9000/api/v3
result :  {'startRanking': '0x1', 'totalDelegated': '0x1bc16d674ec80000', 'preps': [{'address': 'hxdc8d79453ba6516bc140b7f53b6b9a012da7ff10', 'delegated': '0x1bc16d674ec80000'}]}
```
