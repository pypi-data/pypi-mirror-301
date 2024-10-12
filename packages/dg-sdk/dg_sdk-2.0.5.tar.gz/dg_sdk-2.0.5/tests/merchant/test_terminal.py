import unittest
from tests.conftest import *


class TestTerminal(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_terminal_add(self):
        terminal_info_list = [{
            "sn": "sn1",
            "tusn": "tusn",
            "dev_model_code": "01"
        }]
        result = dg_sdk.Terminal.add(terminal_info_list=json.dumps(terminal_info_list))
        assert result["resp_code"] == "00000007"

    def test_terminal_cancel(self):
        result = dg_sdk.Terminal.cancel("device_id")

        assert result["resp_code"] == "00000007"

    def test_terminal_list(self):
        result = dg_sdk.Terminal.query_list()

        assert result["resp_code"] == "00000000"
