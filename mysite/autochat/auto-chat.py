import requests
import os
import time
import random

spam_list = []
f = open('Chinese.txt','r',encoding='utf-8')
for each in f.readlines():
    spam_list.append(each.split())
random.shuffle(spam_list)
for i in spam_list:
    payload = {
        'content': i[0]
    }

    header = {
        'authorization': 'mfa.0lioH4hnSVpVKr_lXzNTqAy3sSDlhgSxj1oEPD_QKH8n3GDOuMOHhSda4StLgwdnIVjqhcZ5vPwHEwxXS6l3'
    }
    r = requests.post('https://discord.com/api/v8/channels/899490796405915688/messages', data=payload, headers=header)
    print(i[0] + " sent")
    time.sleep(64)