import requests

## 需要用户的cookie:dashboard_session,以及payload中的license_key
def test():
    cookie_info = 'dashboard_session=s%3AudJIwaIeCXzTq9gVGOUJT5oCwRL9nvu1.klCw2qljejCJFTNqneku81X9gFq3149RfP%2FSSL%2FP%2BLw'
    cookie_list = [info.strip().split('=') for info in cookie_info.split(';')]
    cookies = {data[0]:data[1].replace('"','') for data in cookie_list}

    url = 'https://account.stellara.io/api/reset'
    payload = {
        'license_key': "6FBZH-7C4ND-7DWF9-L9QQL-FQ3UV"
    }
    headers = {
                'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
            }

    html = requests.post(url, data=payload, headers=headers, cookies=cookies).content.decode()
    return html



