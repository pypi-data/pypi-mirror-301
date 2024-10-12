from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_INVOICE_QUERYAPPLY



class V2InvoiceQueryapplyRequest(object):
    """
    发票开具申请查询
    """

    # 请求流水号
    req_seq_id = ""
    # 请求时间
    req_date = ""
    # 渠道号汇付商户号为空时，必传；&lt;font color&#x3D;&quot;green&quot;&gt;示例值：6666000109812124&lt;/font&gt;
    channel_id = ""
    # 流水号
    seq_id = ""

    def post(self, extend_infos):
        """
        发票开具申请查询

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "req_seq_id":self.req_seq_id,
            "req_date":self.req_date,
            "channel_id":self.channel_id,
            "seq_id":self.seq_id
        }
        required_params.update(extend_infos)
        return request_post(V2_INVOICE_QUERYAPPLY, required_params)
