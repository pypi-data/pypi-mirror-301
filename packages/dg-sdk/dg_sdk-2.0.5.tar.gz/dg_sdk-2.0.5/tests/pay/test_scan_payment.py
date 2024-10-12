import unittest

import dg_sdk
from tests.conftest import *


class TestScanPayment(unittest.TestCase):

    def setUp(self):

        huifu_id = "6666000108854952"
        sys_id = "6666000108854952"
        product_id = "YYZY"
        private_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxtfk3rjwdpBV81WBy5jIMcDLFdvHckhjGXkmWfaBn7euPRyetEhS4inpr7EvQ5KDUXNBPljI2NVhG/LEGZKvau1MW8j3t7dJ3gWafuVGsCiLJHU79sIRHf11nKOTykX5WxB/7MMwRnZsECuaZyCk7WPuSAlznqbDJdrZTzHhjQzMhjto1qD6+vc0OxyaBFlOY9piBtEfecsvD+6GfQ8exFqwzblJm9iZPYw02DaeUDLFO9Umn7i7gShlj/1Hh8nEM7YitpF/p26o+MC9LHWbIjgzjvNVhSRVmbvWys+3S11Zm/vux6Yzfk0H3fqrksAKSEkLEtEoYKS4wKjHdecztAgMBAAECggEACy1g4WmqCks5tsJM8K0d1L5x0w2qJK9js4ZWpop8Pk0ulbJqAm6ysvCyxnr0Qc0/eFvmFjtiKRqt1LksATTvwjAqB7Vww7hDlpSi+cTUKDfy/CdFwpsJlt2h6E0gKUmRYq+vO0NUcn8xMs3ktyNpxHvSRtqzMTbxEZrP2PFxWPzUKGNyk53FTlJ64YCoGQqWeGhA5LO6QLPHlAxIrvRf9B5dtXQr5XZXVqS9MwjtsRPvQPWiFXxlzvhJRcL/wXehcNextHzpMMgX/idB3HIpIl6XXLKiFUR4rBDJIMiQjQvS6zz2l1zpiJ0vWujVa3IY+PNefRA2ttg1DeC19GYa2QKBgQDh7AkJ7wut7p4qYAdcFEDVhFgP5mnSRyOBGWmClHYE4RIFplPiv4yO0fttAjFuCg4Zaxq49BuV3zshWOEIr72VK6wMa6Z+QbfXNr/1DT6nW+ktgXTw2G9Ts/nZiMrpcsbl7qvwChfJAPvEwnyP7Ckmd9t2WbQisuYZc+Vu8znO7wKBgQDJXskTiExEipQSOcVH5cX/ExVyj9MoLjmJhy3WTTDzGafgEoOPOfej2ZCgF6gCwugXJr+rtgdOpASk8WPACaCePdjdgQ2NVhSfV3op3TtvhgAPf3iI/zCVkZM4I1iZs6KjdHstLCKyAzCFBsowkPbfZBlFX4eO7Bk6XcIZ6x2h4wKBgQDcH64C5s4bb2beZOhm2Dj/kU54V4l93+CBFjCOkXaYdG+p35DWWspqEcCHSt68l8F7FLdZxEbodTPY3w+L9iejI4UkKPN1CzVD1U2dR4VnbY85zmwRiuCVzsM/KCCE61dOi4ktfbgFGhc1dEYHuROzLo8/tlFkiajW3eyLeSM3MwKBgATL3iw57d8gEeDRQXKx9WJa+QLOjDAD0dkFwEC/e+/+Z3I93qZVsiFT+E7n4VeXfuG2SZB0eH4WCApJuZ+EWzAJtxWnkkQQjdMxyTYgD99bKLs1xRA2S9j0K7aFmQGoNrJ//sMXrwfgbZJtk/lOKqMthjCR0u/DjeJHA22MnRsTAoGADXzJs/of0JExvQWwfdIUnSEPs/PgTrrJpo+CAdXnagYHF+InrmvIcNwx6ZzIs+9aGwUt0d/YsSpJkHMfAtTwZjB7sSw8Cg5DZ179Jy3YkKhFPvZv2ZCANa5J74HZNQUrUUL6O4FouZUiLwFlq8YuUPRtkAjYwyS/jwUbhJzqZhQ="
        public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkMX8p3GyMw3gk6x72h20NOk3L9+Nn9mOVP6+YoBwCe7Zs4QmYrA/etFRZw2TQrSc51wgtCkJi1/x8Wl7maPL1uH2+77JFlPv7H/F4Lr2I2LXgnllg6PtwOSw/qvGYInVVB4kL85VQl0/8ObyxBUdJ43I0z/u8hJb2gwujSudOGizbeqQXAYrwcNy+e+cjodpPy9unpJjBfa4Wz2eVLLvUYYKZKdRn6pZR2cQsMBvL30K4cFlZqlJ9iP2hTG3gaiZJ9JrjTigwki0g9pbTDXiPACfuF1nOeObvLD22zBbgn1kwgfsqoG67z7g84u2jvfUFCzX1JRgd0xfNorTRkS2RQIDAQAB"

        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)

        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_payment_create(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")
        assert result["resp_code"] == "00000100"

    def test_payment_query(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.query(org_req_date=result["req_date"],
                                          org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "00000000"

    def test_payment_close(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.close(org_req_date=result["req_date"],
                                          org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "20000001"

    def test_payment_close_query(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")
        result = dg_sdk.ScanPayment.close(org_req_date=result["req_date"],
                                          org_req_seq_id=result["req_seq_id"])
        result = dg_sdk.ScanPayment.close_query(org_req_date=result["req_date"],
                                                org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000001"

    def test_payment_refund(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.refund(ord_amt="0.01",
                                           org_req_date=result["req_date"],
                                           org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000000"

    def test_payment_refund_query(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.refund(ord_amt="0.01",
                                           org_req_date=result["req_date"],
                                           org_req_seq_id=result["req_seq_id"])
        result = dg_sdk.ScanPayment.refund_query(org_req_date=result["req_date"],
                                                 org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000001"

    def test_union_user_id(self):
        result = dg_sdk.ScanPayment.union_user_id("fadsfa/tTBQ==")
        assert result["data"]["resp_code"] == "90000000"

    def test_micro_create(self):
        result = dg_sdk.ScanPayment.micro_create("0.10",
                                                 "test",
                                                 "12212312312312",
                                                 risk_check_data)
        assert result["resp_code"] == "10000000"

    def test_confirm(self):
        result = dg_sdk.ScanPayment.confirm(org_req_date="20220401",
                                            org_req_seq_id="22121212121221")
        assert result["resp_code"] == "23000001"

    def test_confirm_query(self):
        result = dg_sdk.ScanPayment.confirm_query(org_req_date="20220401",
                                                  org_req_seq_id="22121212121221")
        assert result["resp_code"] == "23000001"

    def test_confirm_refund(self):
        result = dg_sdk.ScanPayment.confirm_refund(org_req_date="20220401",
                                                   org_req_seq_id="22121212121221")
        assert result["resp_code"] == "23000001"

    def test_preorder_create1(self):
        hosting_data = {
            "project_title": "project_title",
            "project_id": "project_id",
            "private_info": "private_info",
            "callback_url": "https://paas.huifu.com/partners/api/#/cpjs/api_cpjs_hosting"
        }
        result = dg_sdk.ScanPayment.preorder_create(pre_order_type="1",
                                                    trans_amt="1.01",
                                                    goods_desc="goods_desc",
                                                    hosting_data=json.dumps(hosting_data))
        assert result["resp_code"] == "40000001"

    def test_preorder_create2(self):
        app_data = {
            "app_schema": "app_schema",
        }
        result = dg_sdk.ScanPayment.preorder_create(pre_order_type="2",
                                                    trans_amt="1.01",
                                                    goods_desc="goods_desc",
                                                    app_data=json.dumps(app_data))
        assert result["resp_code"] == "00000000"

    def test_preorder_create3(self):
        miniapp_data = {
            "seq_id": "",
        }
        result = dg_sdk.ScanPayment.preorder_create(pre_order_type="3",
                                                    trans_amt="1.01",
                                                    goods_desc="goods_desc",
                                                    miniapp_data=json.dumps(miniapp_data))
        assert result["resp_code"] == "00000000"
