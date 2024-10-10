#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : file
# @Time         : 2022/7/5 下午3:31
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import mimetypes
from meutils.pipe import *
# from fastapi import UploadFile 有点区别
from starlette.datastructures import UploadFile
from contextlib import asynccontextmanager


def file_append_firstline(line):
    with open('untitled.txt', "r+") as f:
        old = f.read()

        f.seek(0)
        f.write(line)
        f.write(old)


def base64_to_bytes(base64_image_string):
    """
    # 将字节数据写入图片文件
    image_data = base64_to_bytes(...)
    with open(filename, 'wb') as file:
        file.write(image_data)
    """
    return base64.b64decode(base64_image_string.split(",", 1)[-1])


async def to_bytes(file: Union[UploadFile, str, bytes]):  # plus
    """

    :param file: 文件对象、路径、base64、url
    :return: todo: bytes、filepath、io.BytesIO
    """
    # assert file

    logger.debug(type(file))

    if isinstance(file, bytes): return file

    file_bytes = None
    if isinstance(file, UploadFile):
        file_bytes = await file.read()

    elif isinstance(file, str) and file.startswith('http'):
        resp = await httpx.AsyncClient(timeout=30).get(file)
        file_bytes = resp.content

    elif isinstance(file, str) and len(file) > 256:
        file_bytes = base64_to_bytes(file)

    elif isinstance(file, str) and len(file) < 256 and Path(file).is_file():
        file_bytes = Path(file).read_bytes()

    return file_bytes


@asynccontextmanager
async def to_tempfile(file: Union[UploadFile, str]):
    """

    :param file: 文件对象、路径、base64、url
    :return: todo: bytes、filepath、io.BytesIO
    """
    file_bytes = await to_bytes(file)

    with tempfile.NamedTemporaryFile(mode='wb+') as temp:
        temp.write(file_bytes)
        temp.seek(0)

        logger.debug(temp.name)

        yield temp.name


async def to_url(file: Union[UploadFile, str, bytes]):
    from meutils.oss.minio_oss import Minio
    from meutils.apis.chatglm.glm_video import upload_task as upload

    file = await to_bytes(file)
    file_object = await upload(file)

    return file_object and file_object.url

    # file_object = await Minio().put_object_for_openai(file=file, content_type=content_type, bucket_name="caches")

    # return file_object.filename


def base64_to_file(base64_image_string, filename):
    image_data = base64_to_bytes(base64_image_string)
    with open(filename, 'wb') as file:
        file.write(image_data)


# NamedTemporaryFile

if __name__ == '__main__':
    # import tempfile
    #
    # # 使用上下文管理器自动处理文件的关闭和删除
    # with tempfile.NamedTemporaryFile(mode='wb+') as temp:
    #     temp.write(b"This is a temporary file.")
    #     temp.seek(0)
    #     print(f"文件内容: {temp.read()}")
    #     print(f"临时文件名: {temp.name}")
    # 文件在这里自动关闭和删除

    arun(to_bytes(''))