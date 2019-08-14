from iconsdk.wallet.wallet import KeyWallet
from preptools.core.prep import PRepToolsReader, PRepToolsWriter


class IconService:
    def __init__(self):
        """
            Iconservice for test.
        """

    def call(self, call, full_response:bool = False) -> dict:
        params = {
            "to": call.to,
            "dataType": "call",
            "data": {
                "method": call.method
            }
        }

        if call.from_ is not None:
            params["from"] = call.from_

        if isinstance(call.params, dict):
            params["data"]["params"] = call.params

        return self.make_request('icx_call', params)

    def send_transaction(self, signed_transaction, full_response:bool = False) -> dict:
        params = signed_transaction.signed_transaction_dict
        return self.make_request('icx_sendTransaction', params)

    def get_transaction_result(self, tx_hash: str, full_response: bool = False):
        params = {'txHash': tx_hash}
        result = self.make_request('icx_getTransactionResult', params)
        return result

    def get_transaction(self, tx_hash: str, full_response: bool = False):
        params = {'txHash': tx_hash}
        result = self.make_request('icx_getTransactionByHash', params)
        return result

    def estimate_step(self, transaction):
        return 10000000

    def make_request(self, method, params) -> dict:

        rpc_dict = {
            'jsonrpc': '2.0',
            'method': method,
            'id': 1234
        }

        if params:
            rpc_dict['params'] = params

        return rpc_dict


def create_writer(keystore_path, password):
    icon_service = IconService()
    wallet = KeyWallet.load(keystore_path, password)

    writer = PRepToolsWriter(icon_service, 3, wallet)
    writer.set_on_send_request(lambda x: True)

    return writer


def create_reader():
    icon_service = IconService()

    reader = PRepToolsReader(icon_service, 3)
    reader.set_on_send_request(lambda x: True)

    return reader