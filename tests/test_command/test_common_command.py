# -*- coding: utf-8 -*-
# Copyright 2017-2018 ICON Foundation
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

import json
import os
import unittest

from iconsdk.exception import KeyStoreException
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.utils.convert_type import convert_hex_str_to_bytes

from preptools.utils.preptools_config import FN_CLI_CONF
from preptools.command.common_command import _genconf, _keystore


class Container(object):
    pass


def key_from_key_store(file_path, password):
    wallet = KeyWallet.load(file_path, password)
    return convert_hex_str_to_bytes(wallet.get_private_key())


class TestKeyStore(unittest.TestCase):

    def setUp(self) -> None:

        self.args = Container()

    def test_private_key(self):

        self.args.path = 'keystoretest'
        self.args.password = 'qwer1234%'

        _keystore(self.args)

        # get private key from keystore file
        written_key = key_from_key_store(file_path=self.args.path, password=self.args.password)
        self.assertTrue(isinstance(written_key, bytes))

        # wrong password
        self.assertRaises(KeyStoreException, key_from_key_store, self.args.path, 'wrongpasswd')

        # wrong path
        self.assertRaises(KeyStoreException, key_from_key_store, 'wrongpath', self.args.password)
        os.remove(self.args.path)

    def test_genconf(self):

        _genconf(self.args)
        self.assertTrue(os.path.exists(FN_CLI_CONF))

        with open(FN_CLI_CONF) as f:
            tmp_conf = json.load(f)
        self.assertTrue(tmp_conf.get('url', False) is not False)
        self.assertTrue(tmp_conf.get('nid', False) is not False)
        self.assertTrue(tmp_conf.get('keystore', False) is not False)

        os.remove(FN_CLI_CONF)

