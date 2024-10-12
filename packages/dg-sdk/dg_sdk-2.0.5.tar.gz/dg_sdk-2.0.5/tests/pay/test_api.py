import unittest
import requests
import ujson
from Crypto.Hash import MD5
import dg_sdk
from tests.conftest import *


class TestDGApi(unittest.TestCase):

    def setUp(self):
        huifu_id1 = "6666000120254152"
        sys_id1 = "6666000120254152"
        product_id = "YYZY"
        private_key1 = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDZBr2JmycRODc2KwyejpG+6GE0ww3V+2hoEY7zfHtzVVLJy0P2XfcFngTXLXS9q/5GF6KTgANXfZlHpx1dzDA7ZQg2edIFdPYccmjJMPVlUT1tpmPgMb30DPy/Shte19+ZK2eWlBGXPkUVHxbD+5dKjqSZijdil9caZqPMEeOwcXDMXCQvDlkolqVVTTY/Ph/Za/cQGbjqy8OCpkwxCfWHJ9Ij6w/FatZ8rjzibLTRow3vERC88BNYBJQmdEeCMnGHGdssgX8QbJVSMgDfkhBKFSKNPOXQBQkzAV0nJJZ8wUGDH38fHIESl0u5UKtVloHBfx4s4f6co1Im6a3yl+WBAgMBAAECggEBAKkP/CSvDb73SONUo878hwLt6ZN9g1C3OX0geHiq90xAIm76fmX0ixMAJwss6O08h6c4kDhRF8lXGUndIB5KiyQprz0opvgDRhmg8ooQLooPwEejv9gNR8lPOLEXXL0Ec7XRPy/pBs8H/i7W+hgP7Kpy9jx5lG2klTeGz4CQSwvN06mkZN9XlUj4gJ2egt9lvFTKaKGSsgBuxaxpJdhaDHSccS7JmLme5fDBG8FZpHbep8yLkmdtxrCYdtYa4KoTmjpWlsi3jYLaO/Y5aHNBrS/tv8dzrdPbcXjyg1o6+caebogwdxSr4WtH1dvq8cj8Wn8uY/pv07Cl5YdQwTOGjLUCgYEA9RVWDUioTw/fD3zl/n5L2/ujPVnH/+ADWHzfgc5si7O2BqyXsIdFxK0TkAT/8ZwUtGWEAf4S6LEjU7b3vjbz+4+RK4+PVfXmie1cEbHgNlW/fDKuPLQ0k/CjugI/0d26xqs5YzCXoA1nNiMOLOxyNa9Wf0sxEKYF+/vE22taXn8CgYEA4rF4+gsgc5Yu9ILyfDSn0A0bMzst1kAWST1aG3SaIUJiL54VQtrr+50sli1xTndqH1WOC7Jh14lQcZvcPLq1KkPPD/u00XwqTAmFi4yTllef/V4YWsGJ6zsilMtQlmuqtKLckgPbAsV39wpdM7OZkQGU5pVVNzDy+0qjSbLzu/8CgYB8ldsHp66/eh73PZOhGkyvyCyETHaJ0TOCMQBheTDel31pySTXPPyvbRgrtw7woFo6FfzUEndESH/f13v6+u5uK94tGa5QkU8fQET0TcrfdBmCJjVCcIzlw4dHUEtnAOMoiPQEQzhgyU91Sr6zAYNRXQ+IaA3KG8ug+6xnqhvnOwKBgHa6JHYw5aoj+iuteXp7yXg5pQlL8VHI9uMc8th2VVMeBXaTAOem6Pk69GMjIbjK6hXHJUITBxNvo2YdD1fvIXslUIk6dxVQRobUZdEUqyeOdQiqA29k9erxaccsROTDNwCsW4FN66Kj8ZS9JNszMTa08Vti0uK5DEl4adTrmKPZAoGBAIu7DRxSv8dUFljN7ynJKkDDy2h7UdiwOSRcGF/vQmdN17+WR8Eiqiyfc7cNyMNMIOlrmYi6ISYF1UhjJ1SPGoCr6p+84vzl8pQgpZU5mjaLZABzC0mtwEyqDidqDqjkiSdkggrTZJsHR2gn1c8GSxIa5lkVA0K4BZr8cBOA2Xks"
        public_key1 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtNUaxFyNguNGUQ8fSwfnL4UPAlsPMvG8Fv3iZ41hQgBFsgF+ScVXPLBb5+E0PB22UvSev0DYG+wVhbbkDScGkNDvW2nGpgKO4X3TK7XuhbkExB892zI05fTG/zURvEiLbQ/u6d9yvuF13ouayZwsNTqTY2CTn0o2YXw2MsdEW91FP4SUn6XFacqCfxPvBvjmOg3Mj9k7TzU7Q0O/gMvFqY02LEjxwwBa/rbWMaPwJRz9XWBWnkL4x4lo5iWF/PFaTm9Ifr2XsxjXycZCd9nNQ1MEi4PqW2YBqmALhR883C7eVAQAjBBLqCdZ6tjLYfa+4qcjtJMs9w3VtLzIdVAbHQIDAQAB"
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key1, public_key1, sys_id1, product_id, huifu_id1)
        print("setup")

    def tearDown(self):
        print("tearDown")

    # 企业商户进件
    def test_create_enterprise(self):
        merchant_info = dg_sdk.MerchantInfo(short_name="yong",
                                            prov_id="310000",
                                            area_id="310100",
                                            district_id="310151",
                                            detail_addr="上海-上海市-崇明区长江农场长江大街161号上海长江经济园",
                                            contact_name="yingyongwang",
                                            contact_mobile_no="17602151526",
                                            contact_email="yingyong.wang@huifu.com",
                                            busi_type="1",
                                            receipt_name="will超市",
                                            mcc="5311",
                                            service_phone="17602151526",
                                            sms_send_flag="Y",
                                            login_name="willwang1")

        card_info = dg_sdk.MerCardInfo(card_type="2",
                                       card_name="王英永",
                                       card_no="6214852106586327",
                                       prov_id="310000",
                                       area_id="310100",
                                       bank_code="03080000",
                                       branch_name="",
                                       cert_type="00",
                                       cert_no="370481198704223510",
                                       cert_validity_type="0",
                                       cert_begin_date="20181201",
                                       cert_end_date="20281201",
                                       mp="")
        lic_info = dg_sdk.BussinessLicInfo(reg_name="上海汇涵信息科技服务有限公司",
                                           ent_type="3",
                                           license_code="91310230MA1JTWAK98",
                                           reg_prov_id="310000",
                                           reg_area_id="310100",
                                           reg_district_id="310151",
                                           reg_detail="上海-上海市-崇明区长江农场长江大街161号上海长江经济园",
                                           license_validity_type="1",
                                           license_begin_date="20190705",
                                           license_end_date="")

        legal_info = dg_sdk.LegalInfo(legal_name="张戈",
                                      legal_cert_type="00",
                                      legal_cert_no="510102196609237493",
                                      legal_cert_validity_type="0",
                                      legal_cert_begin_date="20050813",
                                      legal_cert_end_date="20250813")
        settle_info = dg_sdk.SettleConfigInfo(settle_cycle="D1",
                                              min_amt="1.00",
                                              remained_amt="2.00",
                                              settle_abstract="abstract",
                                              out_settle_flag="2",
                                              out_settle_huifuid="",
                                              fixed_ratio="5.00")
        cash_config = dg_sdk.CashConfigInfo(cash_type="D0",
                                            fix_amt="1.00",
                                            fee_rate="0.11")
        cash_list = [cash_config]

        result = dg_sdk.Merchant.create_enterprise(upper_huifu_id=upper_huifu_id,
                                                   merch_info=merchant_info,
                                                   card_info=card_info,
                                                   lic_info=lic_info,
                                                   legal_person=legal_info,
                                                   )

        assert result["resp_code"] == "00000001"

    def test_query_ent(self):
        result = dg_sdk.Merchant.query_merch_info(huifu_id="6666000120254152")
        assert result["resp_code"] == "00000000"

    def test_query_apply_no(self):
        result = dg_sdk.Merchant.query_apply_status(apply_no="2022072200769029")
        assert result["resp_code"] == "00000000"

    def test_open(self):
        sys_id1 = "6666000108840829"
        alipay = {
            "mcc": "2015050700000000",
            "pay_scene": "1",
            "fee_rate": "0.81",
        }
        ali_conf_list = [alipay]
        result = dg_sdk.Merchant.reg_busi_info(upper_huifu_id=sys_id1, ali_conf_list=json.dumps(ali_conf_list))
        assert result["resp_code"] == "00000000"

    def test_payment_create(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE", trans_amt="0.01", goods_desc="test",
                                           notify_url="https://checkoutbfftest.cloudpnr.com/v1/callback")
        assert result["resp_code"] == "00000000"

    def test_payment_query(self):
        # "req_date": "20220726", "req_seq_id": "202207261659088430969""https://qr.alipay.com/bax07930dlbbhmobf2ei0013"
        result = dg_sdk.ScanPayment.query(org_req_date="20220726", org_req_seq_id="202207261659088430969")
        assert result["resp_code"] == "00000000"

    def test_refund(self):
        # "req_date":"20220726","req_seq_id":"202207261703353473238"
        result = dg_sdk.ScanPayment.refund(ord_amt="0.01", org_req_date="20220726",
                                           org_req_seq_id="202207261710496301903")
        assert result["resp_code"] == "00000000"

    def test_refund_query(self):
        result = dg_sdk.ScanPayment.refund_query(org_req_date="20220726", org_req_seq_id="202207261703353473238")
        assert result["resp_code"] == "00000000"

    def test_upload(self):
        result = dg_sdk.Merchant.upload(file_type="F17", picture_path="../test_pic.png")
        assert result["data"]["resp_code"] == "00000000"


def helipay_sign(params: dict):
    # E1807227095
    orginal_str = ""
    for key in params.keys():
        orginal_str += "&" + params[key]
    orginal_str += "&u9TuVGfn3hOFTuhBwRgomvugKmM9hyM5"
    print(orginal_str)
    h = MD5.new()
    h.update(str(orginal_str).encode('utf-8'))
    sign = h.hexdigest().lower()
    print(sign)
    return sign


def helipay_request(params):
    url = "http://pay.trx.helipay.com/trx/app/interface.action"
    sign = helipay_sign(params)
    params["sign"] = sign
    response = requests.post(url, params=params, verify=False)  # 发送请求
    if response.status_code != 200:
        try:
            reason = json.loads(response.text)['message']
        except Exception as e:
            str(e)
            reason = 'System Error'
        raise ConnectionError(response.status_code, reason)
    return ujson.loads(response.text)


class TestHELIPayApi(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    # 交易接口
    def test_payment_create(self):
        params = {
            "P1_bizType": "AppPay",
            "P2_orderId": "2022072715021",
            "P3_customerNumber": "E1807227095",
            "P4_payType": "SWIPE",
            "P5_orderAmount": "0.11",
            "P6_currency": "CNY",
            "P7_authcode": "284677387843274569",
            "P8_appType": 'ALIPAY',
            "P9_notifyUrl": "https://checkoutbfftest.cloudpnr.com/v1/callback",
            "P10_successToUrl":"",
            "P11_orderIp": "192.168.10.1",
            "P12_goodsName": 'Iphone7',
            "P13_goodsDetail":"111",
            "P14_desc": "22222",
        }
        result = helipay_request(params)
        print(result)
        assert result["rt2_retCode"] == "0000"

    def test_payment_query(self):
        params = {
            "P1_bizType": "AppPayQuery",
            "P2_orderId": "2022072715021",
            "P3_customerNumber": "E1807227095",
        }
        result = helipay_request(params)
        print(result)
        assert result["rt2_retCode"] == "0000"

    def test_payment_refund(self):
        params = {
            "P1_bizType": "AppPayRefund",
            "P2_orderId": "2022072715021",
            "P3_customerNumber": "E1807227095",
            "P4_refundOrderId":"2022072715011",
            "P5_amount":"0.11",
            "P6_callbackUrl":"https://checkoutbfftest.cloudpnr.com/v1/callback"
        }
        result = helipay_request(params)
        print(result)
        assert result["rt2_retCode"] == "0000"

    def test_payment_refund_query(self):
        params = {
            "P1_bizType": "AppPayRefundQuery",
            "P2_refundOrderId": "2022072715011",
            "P3_customerNumber": "E1807227095",
        }
        result = helipay_request(params)
        print(result)
        assert result["rt2_retCode"] == "0000"