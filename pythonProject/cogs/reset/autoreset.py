import requests
import json


def cookie_trans(cookie_info):
    cookie_list = [info.strip().split('=') for info in cookie_info.split(';')]
    cookies = {data[0]: data[1].replace('"', '') for data in cookie_list}
    return cookies


def reset_mekaio():
    url = 'https://dashboard.mekrobotics.com/api/reset'
    payload = {}
    headers = {
        'authorization': 'Bearer EyllEDF8P6XqP6jlvbEcikD4IFWVde',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    }

    html = requests.post(url, data=payload, headers=headers)
    try:
        return json.loads(html.text)
    except:
        error = 'Please re-try login on our website!'
        return error


def reset_stellar():
    cookie_info = 'dashboard_session=s%3A-H6L0hdLojNJ4XpPYWJ24zoaZfmIgr6t.zpHVvXK1pJ0V3WGiqgY6dacwvUVtS9EolTO4WidxE8o'
    cookies = cookie_trans(cookie_info)

    url = 'https://account.stellara.io/api/reset'
    payload = {
        'license_key': "6FBZH-7C47DWF9-L9QQL-FQ3UV"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    }

    html = requests.post(url, data=payload, headers=headers, cookies=cookies)
    try:
        return json.loads(html.text)
    except:
        error = 'Please re-try login on our website!'
        return error

def reset_kodai():
    cookie_info = 'kodai_dashboard=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IllJTSM5Nzg0IiwiZW1haWwiOiJoZXJvbnNvbmcxMDI0QGdtYWlsLmNvbSIsImlkIjoiNTU5NDk1Njk4NzAyMTM5NDEyIiwiYXZhdGFyIjoiYmZhMGU1YWIwMzM2YTJjMjczOWY2ZGJmZDc5ODBiYTEiLCJkaXNjcmltaW5hdG9yIjoiOTc4NCIsInN0b3JhZ2UiOiIxZmZhOTFhYjhkZjQyNDEwYzg1YmJmZWY3YjMzMWNjODQ4YjY4NDllYzYwYjI0NzZmNTI2ZGZiZDM3Y2FmZTdkNWVhZGJmOWJlMzUxODg0ZmNhNTNjNmEyOTQzYTJlMWJhODViMTJhM2YzYmVkMDJmZTY3N2FmMTNjM2UyZjI2Zjk4ZTk5NzFmZDU0NjBmZDRkNzM1YWRkNzQxMzRjY2VmNmZhNWVhNTFkYTIzOTM0YjIzNjFmMTIzNDFmNDVjZjI2Yzg3YWY3YjE3N2ZlODBhYjFlNzNlMjc4ODgyODg1MDZjZDdlYzdlYzIxMmUwYWMwNTJmZGEyNDcwZmM1ZGZlNDliYTUzYWZkMjM2MDE3MjM1ZTI2OWMxOTA4NDViMDExNmQzZjIxYjY2YzkyZWVkMTcwYjEyNGFhZmM4MzFkOTgzMTA2ZTY1ZWQ5YzNhNTYzNjgxOGRlNjQxZGI5Y2FlYmRjNjc5YTk5MmIzYzQzMTllN2RjOTFjODQwYTc5ZWRhNzFiMjZiMzc4MmE1Y2FiMTU0ZGQzNjcxOGJiYzZhZCIsImlwIjoiMjE2LjEyNi4yMjQuMTAyIiwiaWF0IjoxNjI5MDAxODA3fQ.REGfy2rkxDnlfm4yxqq-icn4Db6t0_9iHN80XQCVqzw'
    cookies = cookie_trans(cookie_info)

    url = 'https://hub.kodai.io/api/user/unbind'
    payload = {
        'unbind_type': "machine"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    }

    html = requests.post(url, json=payload, headers=headers, cookies=cookies)
    try:
        return json.loads(html.text)
    except:
        error = 'Please re-try login on our website!'
        return error

def reset_koi():
    url = 'https://dash.koi.solutions/api/user/reset/machine'
    payload = {
        'licenseKey': "FYANWP-HXATLA-NDNHVE-TKCQDL",
    }
    headers = {
        'authorization': 'Bearer iJO2eZbd0xFII4kyDEvqM7YJ4EOpVi',
        'content-type': 'application/json',
        'tl_client': 'koisolutions',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }

    html = requests.delete(url, data=json.dumps(payload), headers=headers).content.decode()
    try:
        return html
    except:
        error = 'Please re-try login on our website!'
        return error