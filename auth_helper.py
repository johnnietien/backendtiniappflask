# auth_helper.py
import urllib.request
import json

import base64
import hmac
import hashlib

import time
import os

###########################
# Cách tính signature bằng Python tương tự trong bài viết:
# https://miniapp.tiki.vn/docs/backend-api/platform-api/calculate-signature
###########################


def base64URLEncode(data):
    message_bytes = data.encode()
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode()
    return base64_message.replace("=", "").replace("+", "-").replace("/", "_")


def sign(secret, payload):
    return hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

###########################
# Chuẩn bị định dạng và thực hiện POST request theo yêu cầu hướng dẫn trong bài viết:
# https://miniapp.tiki.vn/docs/backend-api/platform-api/exchange-auth-token
###########################


def new_request_auth_exchange(data_dict):
    # Chúng ta sẽ truyền thông tin cho các biến sau từ môi trường lúc khởi động container khi deploy Cloud Run
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    AUTH_ENDPOINT = os.environ.get("AUTH_ENDPOINT")

    if not CLIENT_ID:
        raise Exception("CLIENT_ID missing")

    if not CLIENT_SECRET:
        raise Exception("CLIENT_SECRET missing")

    if not AUTH_ENDPOINT:
        raise Exception("AUTH_ENDPOINT missing")

    headers = {
        "Content-Type": "application/json",
    }

    data = json.dumps(data_dict, separators=(',', ':'))

    my_timestamp = str(time.time_ns() // 1_000_000)
    payload = my_timestamp + '.' + CLIENT_ID + '.' + data
    encodedPayload = base64URLEncode(payload)
    my_signature = sign(CLIENT_SECRET, encodedPayload)

    req = urllib.request.Request(AUTH_ENDPOINT, data.encode(), headers)
    req.add_header('X-Tiniapp-Client-Id', CLIENT_ID)
    req.add_header('X-Tiniapp-Signature', my_signature)
    req.add_header('X-Tiniapp-Timestamp', my_timestamp)

    response = urllib.request.urlopen(req)
    res = response.read()

    return res
