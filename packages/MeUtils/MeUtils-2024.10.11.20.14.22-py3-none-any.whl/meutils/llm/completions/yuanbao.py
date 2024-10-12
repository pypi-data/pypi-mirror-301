#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : yuanbao
# @Time         : 2024/6/11 18:56
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.schemas.openai_types import ChatCompletionRequest, ImageRequest
from meutils.schemas.yuanbao_types import SSEData, YUANBAO_BASE_URL, API_CHAT, API_GENERATE_ID, API_DELETE_CONV, \
    GET_AGENT_CHAT
from meutils.llm.openai_utils import create_chat_completion_chunk, create_chat_completion
from meutils.llm.utils import oneturn2multiturn

from meutils.config_utils.lark_utils import get_next_token_for_polling, aget_spreadsheet_values

# import rev_HunYuan
FEISHU__URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=onX3Rg"


class Completions(object):

    async def create(
            self,
            request: Optional[ChatCompletionRequest] = None,
            image_request: Optional[ImageRequest] = None,
            token: Optional[str] = None
    ):
        token = token or await get_next_token_for_polling(FEISHU__URL)

        logger.debug(token)

        prompt = request and oneturn2multiturn(request.messages) or image_request.prompt

        payload = {
            "model": "gpt_175B_0404",
            "version": "v2",

            "prompt": prompt,
            # "displayPrompt": "画条可爱的狗狗",
            # "displayPromptType": 1,
            "multimedia": [],
            # "agentId": "gtcnTp5C1G",
            "supportHint": 2,

            "plugin": "Adaptive",

            "options": {
                "imageIntention": {
                    "needIntentionModel": True,
                    "backendUpdateFlag": 2,
                    "intentionStatus": True,
                    "userIntention": {
                        "resolution": "1280x1280",
                        # "scale": "9:16" 1:1 3:4 4:3 9:16 16:9
                        # "n": 1,
                        # "resolution": "1280x1280",
                    }
                }
            }

        }
        if image_request:
            payload["options"]["imageIntention"]["userIntention"].update(
                {
                    "style": image_request.style,
                    "scale": (
                        image_request.size
                        if image_request.size in {"1:1", "3:4", "4:3", "9:16", "16:9"}
                        else "1:1"
                    ),
                    "N": image_request.n,
                    "num": image_request.n,
                    "Count": image_request.n,

                })

        headers = {
            'cookie': token
        }
        async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=300) as client:
            # chatid = (await client.post(API_GENERATE_ID)).text
            chatid = uuid.uuid4()

            async with client.stream(method="POST", url=f"{API_CHAT}/{chatid}", json=payload) as response:
                logger.debug(response.status_code)
                response.raise_for_status()

                async for chunk in response.aiter_lines():
                    content = SSEData(chunk=chunk, crop_image=False).content
                    # print(content)
                    yield content

    def generate_id(self, random: bool = True):
        if random:
            return f'{uuid.uuid4()}'
        return httpx.post(API_GENERATE_ID).text

    def delete_conv(self, chatid):
        response = httpx.post(f"{API_DELETE_CONV}/{chatid}")
        return response.status_code == 200


async def check_token(token):
    headers = {
        "cookie": token
    }
    try:
        async with httpx.AsyncClient(base_url=YUANBAO_BASE_URL, headers=headers, timeout=10) as client:
            response = await client.get("/api/info/general")
            response.raise_for_status()
            # logger.debug(response.json())
            return True
    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    # chatid = generate_id()
    # print(chatid)
    # print(delete_conv(chatid))
    # payload = {
    #     # "model": "gpt_175B_0404",
    #     # "prompt": "1+1",
    #     "prompt": "错了",
    #
    #     # "plugin": "Adaptive",
    #     # "displayPrompt": "1+1",
    #     # "displayPromptType": 1,
    #     # "options": {},
    #     # "multimedia": [],
    #     # "agentId": "naQivTmsDa",
    #     # "version": "v2"
    # }
    # chat(payload)

    # async2sync_generator(Completions(api_key).achat('画条狗')) | xprint

    token = """web_uid=ac283ec7-4bf6-40c9-a0ce-5a2e0cd7db06; _gcl_au=1.1.1953544475.1725261468; hy_source=web; _ga_RPMZTEBERQ=GS1.1.1725847489.1.0.1725847489.0.0.0; _ga=GA1.2.981511920.1725261466; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22100000458739%22%2C%22first_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24search_keyword_id%22%3A%2289fde657001b70490000000367076eae%22%2C%22%24search_keyword_id_type%22%3A%22baidu_seo_keyword_id%22%2C%22%24search_keyword_id_hash%22%3A7357687423495761%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxYjE5OGM3YjJkNTItMGZjY2E4ZDczMWNiOWI4LTE4NTI1NjM3LTIwNzM2MDAtMTkxYjE5OGM3YjMxZmQ5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTAwMDAwNDU4NzM5In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22100000458739%22%7D%2C%22%24device_id%22%3A%22191b198c7b2d52-0fcca8d731cb9b8-18525637-2073600-191b198c7b31fd9%22%7D; hy_user=bUZenNkB3YaXTbw9; hy_token=lTb5OHLVMWugG/U9/hzmYa5iD/AgErdhUhVYAnaHe89jwcc7yKOrNSjuWBtwEeK3"""

    arun(Completions().create(
        ChatCompletionRequest(messages=[{'role': 'user', 'content': '你是谁'}]),
        # ImageRequest(prompt='画条狗', size='16:9', style='粘土风格'),
        token=token
    ))

    # df = arun(aget_spreadsheet_values(feishu_url=FEISHU__URL, to_dataframe=True))
    #
    # for i in df[0]:
    #     if not arun(check_token(i)):
    #         print(i)
    #
