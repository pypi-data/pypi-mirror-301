


import time
import jwt

ak = "76BEA788C18A40DEBCBF43A8E880E5E2" # 填写您的ak
sk = "5EC3CD719160461791A544F650F86C16" # 填写您的sk

def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 9999999999999, # 填写您期望的有效时间，此处示例代表当前时间+30分钟
        "nbf": int(time.time()) - 5 # 填写您期望的生效时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token

authorization = encode_jwt_token(ak, sk)
print(authorization) # 打印生成的API_TOKEN
