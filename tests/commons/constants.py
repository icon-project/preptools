import os

from preptools.utils.constants import PROJECT_ROOT_PATH

TEST_DIRECTORY = os.path.abspath(os.path.join(PROJECT_ROOT_PATH, 'tests'))
TEST_UTIL_DIRECTORY = os.path.join(TEST_DIRECTORY, 'commons')
IN_MEMORY_ZIP_TEST_DIRECTORY = os.path.join(TEST_UTIL_DIRECTORY, 'test_in_memory_zip')

TEST_CONFIG_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'preptools_config.json')
TEST_KEYSTORE_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'test_keystore')
TEST_KEYSTORE_PASSWORD = 'qwer1234%'
TEST_REGISTER_JSON_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'registerPRep.json')
TEST_SET_JSON_PATH = os.path.join(TEST_UTIL_DIRECTORY, 'setPRep.json')
