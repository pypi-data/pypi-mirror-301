#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : check_utils
# @Time         : 2024/9/30 13:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators.retry import retrying

from openai import OpenAI, AsyncOpenAI


@retrying()
async def check_token_for_siliconflow(api_key):
    url = "https://api.siliconflow.cn/v1/user/info"

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


@retrying()
async def check_token_for_openai(api_key, base_url="https://api.stepfun.com/v1"):
    try:
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        models = await client.models.list()
        logger.debug(models)
        return True

    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    from meutils.config_utils.lark_utils import get_next_token_for_polling

    pass
    # arun(check_token_for_siliconflow(os.getenv("SILICONFLOW_API_KEY")))

    FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=KVClcs"

    b = arun(check_token_for_openai(os.getenv("STEP_API_KEY")))

    # arun(get_next_token_for_polling(check_token=check_token_for_openai, feishu_url=FEISHU_URL))
