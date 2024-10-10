#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError

from openai import OpenAI

# response = OpenAI().images.generate(
#     model="stable-diffusion-3",
#     # model="kling",
#
#     prompt="a white siamese cat",
#     size="1024x1024",
#     quality="standard",
#     style="vividx",
#     n=1,
#     extra_body={
#         "guidance_scale": 4.5,
#         "num_inference_steps": 25,
#         "negative_prompt": ""
#     }
# )
#

# from openai import OpenAI
#
# response = OpenAI().images.generate(
#     # model="stable-diffusion-3",
#     model="kling",
#
#     prompt="漫天的星河，浪漫，神秘。超高清，最好的质量，超高细节的画质，8K分辨率",
#     size="1024x1024",
#     n=1
# )


data = {
    'prompt': '一只可爱的边牧在坐公交车，卡通贴纸。动漫3D风格，超写实油画，超高分辨率，最好的质量，8k',

    'model': 'step-1x-medium',
    # 'n': 2, 'quality': 'hd', 'response_format': 'url', 'size': '1024x1024', 'style': 'vivid',
    # 'extra_body': {'guidance_scale': 4.5, 'num_inference_steps': 25, 'seed': None, 'negative_prompt': None}
}

prompt = '一只可爱的边牧在坐公交车，卡通贴纸。动漫3D风格，超写实油画，超高分辨率，最好的质量，8k'

from openai import OpenAI

# model = "stable-diffusion-3"
# with timer(model):
#     response = OpenAI(
#         # base_url="http://0.0.0.0:8000/v1"
#         # base_url="https://openai-dev.chatfire.cn/images/v1",
#         # base_url="https://openai.chatfire.cn/images/v1"
#
#         # base_url="http://111.173.117.175:40001/images/v1"
#         # base_url="https://api.stepfun.com/v1",
#         # api_key="4ewbnANQogxIX8DUY3Cz2VAMlB3ij39cwDrgQfkDtuNAoexu3E7CEJbR8USXVa3pA"
#     ).images.generate(
#         model=model,
#         prompt=prompt,
#     )
#     print(response)

# with timer('image'):
#     model = 'flux-schnell'
#
#     response = OpenAI(
#     ).images.generate(
#         model=model,
#         prompt=prompt,
#     )
#     print(response)
#
# with timer('image'):
#     model = 'flux-pro'
#
#     response = OpenAI(
#     ).images.generate(
#         model=model,
#         prompt=prompt,
#     )
#     print(response)

# model = 'step-1x-medium'
# with timer(model):
#     response = OpenAI().images.generate(
#         model=model,
#         prompt=prompt,
#     )
#     print(response)
#
# model = 'kling'
# with timer(model):
#     response = OpenAI().images.generate(
#         model=model,
#         prompt=prompt,
#     )
#     print(response)
#


prompt = """
日本漫画，2.5D，漫画风格，8K，立绘，异世界，古朴服装，街道，沙地，石头路，高对比度游戏场景，帝国，王国，宏伟，城墙，巨型结构,落日,运河,树,城堡,光辉，光芒，异世界，夜晚，天空，草原，高耸的塔尖和金色的宫殿坐，护城河环绕，大场景，风景，高山，仰视图,,，中景, ，俯视, ，日光, 军营,旗帜飘扬, 列队,，面部特写，清晰的面部，细节特征，清晰的特征，
"""

with timer('image'):
    model = 'flux-pro'
    model = 'flux-dev'
    model = 'flux-schnell'
    model = "cogview-3"
    model = "cogview-3"

    model = "cogview-3-plus"
    # model = "cogview-3-plus"

    # model = "cogview-3-plus"

    model = 'step-1x-medium'
    # model = 'stable-diffusion-xl-base-1.0'

    client = OpenAI(
        api_key='7hNjSQTH2Rsud7Vhd2Fs6oJE93KAAJSAQEHj7BSD51ZhMN5mjo8vxMYpn6jS3xaLR',
        # api_key='13OafcA8KSNO4XLrBR4DpvgVV9d59KCvPAmEdrtsvOIcU4T50B0EGstjLEqPnBI2N',

        base_url='https://api.stepfun.com/v1',

    )

    # print(client.models.list())

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size="1024x1024",
    )

    print(response.data[0].url)

# openai.AuthenticationError: Error code: 401 - {'error': {'message': 'Incorrect API key provided', 'type': 'invalid_api_key'}}
# openai.APIStatusError: Error code: 402 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details', 'type': 'quota_exceeded'}}
