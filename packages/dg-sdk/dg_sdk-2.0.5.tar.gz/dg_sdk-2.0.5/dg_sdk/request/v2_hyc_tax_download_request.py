from dg_sdk.core.request_tools import request_post
from dg_sdk.request.request_api_urls import V2_HYC_TAX_DOWNLOAD



class V2HycTaxDownloadRequest(object):
    """
    完税凭证下载
    """

    # 系统号
    sys_id = ""
    # 产品号
    product_id = ""
    # 加签结果
    sign = ""
    # 数据
    data = ""

    def post(self, extend_infos):
        """
        完税凭证下载

        :param extend_infos: 扩展字段字典
        :return:
        """

        required_params = {
            "sys_id":self.sys_id,
            "product_id":self.product_id,
            "sign":self.sign,
            "data":self.data
        }
        required_params.update(extend_infos)
        return request_post(V2_HYC_TAX_DOWNLOAD, required_params)
