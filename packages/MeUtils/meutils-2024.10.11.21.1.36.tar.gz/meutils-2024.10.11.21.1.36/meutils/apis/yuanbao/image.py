#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image
# @Time         : 2024/10/11 15:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json_repair

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.schemas.yuanbao_types import YUANBAO_BASE_URL, ImageProcessRequest
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.io.files_utils import to_url

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=onX3Rg"


@retrying(min=3, predicate=lambda x: any(x["code"] == code for code in {"429"}))
async def image_process(request: ImageProcessRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL)

    payload = {
        "imageUrl": request.image if request.image.startswith('http') else await to_url(request.image),
    }
    if request.task == 'style':
        payload.update({
            "style": request.style,
            "prompt": f"转换为{request.style}",
        })

    headers = {
        'cookie': token
    }
    async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post(f"/api/image/{request.task}", json=payload)
        response.raise_for_status()
        logger.debug(response.text)

        data = json_repair.repair_json(response.text, return_objects=True)[-2]
        return data


if __name__ == '__main__':
    request = ImageProcessRequest(image="https://oss.ffire.cc/files/kling_watermark.png", task='removewatermark')

    arun(image_process(request))
