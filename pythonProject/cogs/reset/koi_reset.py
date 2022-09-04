import requests
import json

## 需要网站的kodai_dashboard cookie：30 mins的rate limit

cookie_info = '_ga=GA1.2.666459657.1622681297; __stripe_mid=5f78dcfe-cb8f-4736-a5f5-424538465b6f2b7074; __zlcmid=14kk82KecwCLwKq; _gid=GA1.2.1065406704.1629296292; __stripe_sid=cbd62315-889c-4863-92ba-ecfa43f0e44f0ae7e1; __cf_bm=7a13d25fdda59f7898c95cc89dca4e3d07e29099-1629381021-1800-AYRP0WIJ6ocaNgjE1hEGWzak224Z5866wMDgQm83jGKbxYCg3+icmKJgkPjGFThMP6VxicLuPSnnpwTGxttimBPYXOePDHs3zFy1ZbeanqK7y6YRVsTT12TIglnnPlf/mQ==; _gat_gtag_UA_180828276_1=1'
cookie_list = [info.strip().split('=') for info in cookie_info.split(';')]
cookies = {data[0]: data[1].replace('"', '') for data in cookie_list}

url = 'https://dash.koi.solutions/api/user/reset/machine'
payload = {
    'licenseKey': "FYANWP-HXATLA-NDNHVE-TKCQDL",
}
headers = {
    'authorization': 'Bearer iJO2eZbd0xFII4kyDEvqM7YJ4EOpVi',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}

# html = requests.delete(url, data=json.dumps(payload), headers=headers, cookies=cookies).content.decode()
# print(html)

html = requests.get(url, headers=headers, cookies=cookies).content.decode()
print(html)

