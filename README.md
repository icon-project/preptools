# Prep 사용법

## 설치
```
$ python -m venv venv # 가상환경 만듬
$ source venv/bin/activate # 가상환경 활성화
$ ./build.sh # build스크립트 실행
$ ls dist # build 확인
prep-0.0.1-py3-none-any.whl
$ pip install dist/prep-0.0.1-py3-none-any.whl # 설치

```
설치하고 나면, prep이라는 커맨드를 사용하여 P-rep을 등록 또는 삭제할 수 있다.
제공하는 명령어는 register, unregister, preps 세 가지이며 사용법은 다음과 같다.

## Prep 등록

Prep register 명령어를 실행하기 위해선 keystore파일과 json파일이 추가적으로 필요하다(prep 정보가 있는 json파일, prep의 public-key는 keystore file로 추출하기 때문에 생략한다.)

### Usage

```bash
$ prep register -k [키스토어경로] -p [키스토어 비밀번호(옵셔널)] -j [참조할 json경로] -u [노드url(기본값: http://localhost:9000/api/v3)] -n [nid(기본값:3)] -s [stepLimit(기본값: 200만)]
```

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
