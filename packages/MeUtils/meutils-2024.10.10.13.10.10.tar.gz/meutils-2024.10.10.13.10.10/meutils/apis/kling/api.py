#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : api
# @Time         : 2024/10/10 10:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_next_token_for_polling

import jwt

FEISHU_URL_API = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=LGVKwN"


ak = ""  # 填写access key
sk = ""  # 填写secret key


async def encode_jwt_token(ak, sk):

    await get_next_token_for_polling(FEISHU_URL_API)
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token


if __name__ == '__main__':
    api_token = encode_jwt_token(ak, sk)
    print(api_token)  # 打印生成的API_TOKEN
