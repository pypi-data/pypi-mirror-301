from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_MERCHANT_BUSI_EFPCONFIG



class V2MerchantBusiEfpconfigRequest(object):
    """
    全渠道资金管理配置
    """

    # 请求流水号
    req_seq_id = ""
    # 请求日期
    req_date = ""
    # 商户汇付id
    huifu_id = ""
    # 所属渠道商
    upper_huifu_id = ""
    # 开关
    switch_state = ""
    # 自动入账开关0:关闭 1:开通；switch_state为1时必填；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：1&lt;/font&gt;
    out_order_auto_acct_flag = ""
    # 支付手续费外扣汇付ID支付手续费外扣标记为1时必填；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：6666000109812123&lt;/font&gt;
    out_fee_huifuid = ""
    # 全域资金开户使用的银行卡信息首次开通时必填 jsonObject格式
    out_order_acct_card = ""
    # 全域资金开户手续费首次开通时必填 jsonObject格式
    out_order_acct_open_fees = ""
    # 全渠道资金管理补充材料id涉及文件类型：[F504-全渠道资金管理补充材料](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e530&lt;/font&gt;
    other_payment_institutions_pic = ""
    # 新网银行数字证书及电子签名授权委托书out_funds_gate_id为xw0时必填；涉及文件类型：[F534-银行数字证书及电子签名授权委托书](https://paas.huifu.com/open/doc/api/#/csfl/api_csfl_wjlx)；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：57cc7f00-600a-33ab-b614-6221bbf2e530&lt;/font&gt;
    xw_digital_certificate_pic = ""
    # 银行类型
    out_funds_gate_id = ""
    # 签约人信息switch_state为1时必填 jsonObject格式
    sign_user_info = ""
    # 入账来源
    acct_source = ""

    def post(self, extend_infos):
        """
        全渠道资金管理配置

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "huifu_id":self.huifu_id,
            "upper_huifu_id":self.upper_huifu_id,
            "switch_state":self.switch_state,
            "out_order_auto_acct_flag":self.out_order_auto_acct_flag,
            "out_fee_huifuid":self.out_fee_huifuid,
            "out_order_acct_card":self.out_order_acct_card,
            "out_order_acct_open_fees":self.out_order_acct_open_fees,
            "other_payment_institutions_pic":self.other_payment_institutions_pic,
            "xw_digital_certificate_pic":self.xw_digital_certificate_pic,
            "out_funds_gate_id":self.out_funds_gate_id,
            "sign_user_info":self.sign_user_info,
            "acct_source":self.acct_source
        }
        required_params.update(extend_infos)
        return request_post(V2_MERCHANT_BUSI_EFPCONFIG, required_params)
