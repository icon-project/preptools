import getpass
import json
import sys
from argparse import ArgumentParser

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet

ZERO_ADDRESS = f"cx{'0'*40}"


def get_parser():
    arg_parser = ArgumentParser()
    subparsers = arg_parser.add_subparsers(title='Available commands', metavar='command',
                                           description='If you want to see help message of commands,'
                                                       'use "prep command -h"')
    subparsers.dest = 'command'
    subparsers.reqired = True

    parser_reg = subparsers.add_parser('register', help="register prep")
    parser_reg.add_argument('-j', '--json', required=True, help="Json file path."
                                                                "The json file has prep register information")
    parser_reg.add_argument('-p', '--password', required=False, help="password of keystore file")
    parser_reg.add_argument('-k', '--key', required=True, help="keystore file path")
    parser_reg.add_argument('-u', '--url', default="http://localhost:9000/api/v3", help="node uri")
    parser_reg.add_argument('-n', '--nid', default=3, help="nid default(3)")
    parser_reg.add_argument('-s', '--stepLimit', default=2_000_000)

    parser_unreg = subparsers.add_parser('unregister', help="unregister prep")
    parser_unreg.add_argument('-k', '--key', required=True, help="keystore file path")
    parser_unreg.add_argument('-p', '--password', required=False, help="password of keystore file, optional")
    parser_unreg.add_argument('-a', '--address', required=False, help="address to unregister."
                                                                      "only builtinOwner can "
                                                                      "unregister using address parameter")
    parser_unreg.add_argument('-u', '--url', default="http://localhost:9000/api/v3", help="node uri")
    parser_unreg.add_argument('-n', '--nid', default=3, help="nid default(3)")
    parser_unreg.add_argument('-s', '--stepLimit', default=2_000_000)

    parser_candidate = subparsers.add_parser('preps', help="get PRep list")
    parser_candidate.add_argument('-u', '--url', default="http://localhost:9000/api/v3", help="node uri")
    parser_candidate.add_argument('-j', '--json', required=False, help="json file path."
                                                                       "The json file has"
                                                                       " startRanking, endRanking information ")

    return arg_parser


def get_wallet(args: dict) -> KeyWallet:
    key_path = args.get('key')
    password = args.get('password')
    if password is None:
        getpass.getpass('Enter password : ')
    try:
        wallet = KeyWallet.load(key_path, password)
        return wallet
    except:
        print('invalid keystore file or wrong password')
        sys.exit(1)


def main():
    cmd_args = sys.argv[1:]
    parser = get_parser()

    args = vars(parser.parse_args(cmd_args))
    command = args.get('command')
    url = args.get('url')
    step_limit = int(args.get('stepLimit', 0))
    nid = int(args.get('nid', 0))
    icon_service = IconService(HTTPProvider(url))

    try:
        if command == 'register':
            wallet = get_wallet(args)
            json_path = args.get('json')
            with open(json_path, mode='r') as prep_info:
                reg_info = json.load(prep_info)
            public_key = wallet.bytes_public_key
            reg_info['publicKey'] = f"0x{public_key.hex()}"

            register_fee: int = 2000 * 10 ** 18
            tx = CallTransactionBuilder(). \
                from_(wallet.get_address()). \
                to(ZERO_ADDRESS). \
                step_limit(step_limit). \
                value(register_fee). \
                nid(nid). \
                nonce(100). \
                method("registerPRep"). \
                params(reg_info). \
                build()
            signed_data = SignedTransaction(tx, wallet)
            result = icon_service.send_transaction(signed_data)
        elif command == 'unregister':
            wallet = get_wallet(args)
            params = {}
            if args.get('address'):
                params['address'] = args['address']
            tx = CallTransactionBuilder().from_(wallet.get_address()).to(ZERO_ADDRESS). \
                step_limit(step_limit).nid(nid).nonce(100).method("unregisterPRep").\
                params(params).value(0).build()
            signed_data = SignedTransaction(tx, wallet)
            result = icon_service.send_transaction(signed_data)
        elif command == 'preps':
            json_path = args.get('json')
            if json_path is not None:
                with open(json_path, mode='r') as prep_info:
                    params = json.load(prep_info)
            else:
                params = {}
            call_data = CallBuilder(from_=f"hx{'0'*40}", to=ZERO_ADDRESS,
                                    method="getPReps").params(params).build()
            result = icon_service.call(call_data)
        else:
            print('unknown command')
            sys.exit(2)
        print('result : ', result)
        return 0
    except BaseException as e:
        print(e)
        sys.exit(3)


if __name__ == '__main__':
    main()
