import json
import random
import datetime
import requests
from rsa_util_tonglian import rsa_sign, rsa_design
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

rsa_private_key_pay = 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAO0HpPUP+eHk//Ba6ZOePvoZVDpOCRtt943oeVfCTllye43bqja1jVIaebX0MgX+yPYnWIQIOJ9ubSH0R4iyY9y1/HR00qkUpfW3/0usBPt9qn7r0xtFHerhVCd4dT2rKb2Oc5IhKOg05cw/BmMFohMkFsqt0jlrUXI8zJOlLIcxAgMBAAECgYA9lt/pAYa3iK5sQOMyhUrt54j4QXCiXPeXOxHUmNuM6G9sU+itoI0hCVoYymP5JNQJCf45CH3WB3Z5/SRdQ6Uoo1cjao6cCohPLxMSfJglsZCHckPH53o25RKEza4njIgKC+yN7HAhanKymhw/yYQ6i0aXq38zFIk8djMtE7R6xQJBAP6jvNy7UhPKO5rxGFKR+MvvbO3qnYH6x0jZCGY3FlxuGfbavueOiFtMeK67FuDv683dcUKi+M48yR4kH5CfIusCQQDuS9KF6mlm3kHAiZWgVhE8VVNYGpRLCRDgAKm4InGmvk5mUv+O1yAtAFVAEHWIgD4awC7Eqf1YFrSF/It9HV9TAkEAsXiU7JJxhfFw0XAvL30lFZ1tIfReinSp6A+7VuIV552k4vNaEjC4wEjv43fpXiRZCEXJ5lOHbNXYpfUvOrBuuQJAOpow8rf8Jc0g1G3Be0XPRUwii/c1YuKe4Meo9VybIIuKkkV1Dba/9fEwBepGTURkgYWjur+nSyOCT7UUxLcVewJAPLig8dVfKpsiNwYuveEYMcFaO5xoRuiB7v+CMmvxpuuK+rrFS+d7RdmwDbnBiDV4JkTgFObUiGvB7MtS+LGfhw=='
rsa_private_key_merchant = 'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBALRYgEbi7/r+l7z6W3AlKJYBWLSvzatWypn8cCjN0aHlLZTlFpKl1Vm4qz+m/TnjBEB46HEvOrOt+qKpTwjOL0fqSPdcT71ZsuTR9Vx/XH42w7dmlLq9VXRtWerm9VLjEloYChEUtnCSdx0A8VxgwG9qit/GZursjTFEc+Q3U+mbAgMBAAECgYALktxp8C7CIaw/kqTjQwyM5+Q3SvWnfR0+bu63ElJVkfLFae2eFqoPpSQe+cqpeDIHKIXo8ZonpXl+uTUwavmqB6YWtJizsJZrnlTsW0KZDnLk0kPCKXwQFBIYFs9AlccvbQyVdDezrqpb8DLyxrK72RA3ifUU40bXwQCf6JsgoQJBAOp74xr/v2dHsaDAY8YOODQNrNPOwVfy2w7ACRNZUYnu06gIoBMRb6boJ6eEYrUCKhguDcOUm2fLyMnDB9452yECQQDE5OMnaKBDjIM31C4k/m+pYWNcFsAS/KGo49OrqMil4G0cxKzCowgPVgfPHEQac3tQTzXNqpqRLcV0RDzCQkk7AkEAxwUZ0IuroHSYjlFdHfhpuby1qRz+u7A0P8O8sECKVaFw4llXzHdrJeY76hISWYIZymYkZpFWifXMWXuAzRycIQJBAI2HzjT0w0brCSOndKgI8TD7HVYD0HuVd4sUgYICKID8CtLEGT8ru85yU9ivg9DTtA9tcMpu2P6EvUuvBVHKHiMCQHBrMBbRg38NZ+H6eB9mAurxRUZEDjFoGImSGYheWiep13bg+6bNpXFSQjcoMEPUz/+Ws/JsgeD4nV5ZCRXb0iU='
rsa_public = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDYXfu4b7xgDSmEGQpQ8Sn3RzFgl5CE4gL4TbYrND4FtCYOrvbgLijkdFgIrVVWi2hUW4K0PwBsmlYhXcbR+JSmqv9zviVXZiym0lK3glJGVCN86r9EPvNTusZZPm40TOEKMVENSYaUjCxZ7JzeZDfQ4WCeQQr2xirqn6LdJjpZ5wIDAQAB'
CUSID = '55058100780004S'
app_id = '00000005'
merchant_url = 'https://syb-test.allinpay.com/vsppcusapi/merchantapi/add'
pay_url = 'https://vsp.allinpay.com/apiweb/unitorder/pay'


def sign_param(params, rsa_private):
    keys = sorted(params.keys())
    result = ''
    for key in keys:
        value = params.get(key)
        if result:
            result = result + '&' + key + '=' + value
        else:
            result = key + '=' + value
    print(result)
    flag, sign = rsa_sign(rsa_private, result)
    print(sign)
    return sign


def request_ser(params, rsa_private, url):
    sign = sign_param(params, rsa_private)
    params['sign'] = sign

    request_url = url
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    header = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}

    resp = session.post(request_url, json=params, headers=header)
    print(
        'request to {}\nheader={}\nrequest_params{} \nresp is {}'.format(request_url, header, params, resp.text))
    resp.close()
    return resp


def generate_random_str():
    timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    return "" + timestamp + str(random.randint(100000, 9999999))


def atest_create_merchant():
    params = {
        'orgid': '',
        'cusid': '',
        'appid': '',
        'version': '11',
        'randomstr': '',
        'merchantid': '',
        'merchantname': '',
        'shortname': '',
        'servicephone': '',
        'mccid': '',
        'comproperty': '',

    }


def atest_pay():
    params = {
        'cusid': '990440148166000',
        'appid': '00000051',
        'version': '11',
        'randomstr': generate_random_str(),
        'trxamt': '10',
        'reqsn': generate_random_str(),
        'paytype': 'W01',
        'body': 'test',
        'remark': 'remark',
        'notify_url':'https://test.allinpaygd.com/JWeb/NotifyServlet',
        'validtime': '10',
        'signtype': 'RSA'
    }
    resulut = request_ser(params, rsa_private_key_pay, pay_url)


atest_pay()
