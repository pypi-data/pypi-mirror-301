#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : utils
# @Time         : 2024/9/26 15:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators.retry import retrying

url = "https://api.siliconflow.cn/v1/user/info"


# todo: 付费不付费模型优化
@retrying()
async def check_token(api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    try:
        async with httpx.AsyncClient(headers=headers, timeout=60) as client:
            response: httpx.Response = await client.get(url)
            response.raise_for_status()

            logger.debug(response.text)
            logger.debug(response.status_code)

            if response.is_success:
                balance = response.json()['data']['balance']
                return float(balance) > 0
    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    api_key = os.getenv("SILICONFLOW_API_KEY")
    api_key = "sk-fevcjmveugyeqwjszyqktmxtjggpjbohsebfofbpaqxyruwl"
    arun(check_token(api_key))
