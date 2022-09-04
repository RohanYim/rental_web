import requests
import configparser
import os
import sys

# order_number = input("order number: ")
# command = input("command name: ")
bot = sys.argv[1]
buyer = sys.argv[2]

content = '+role add <@' + buyer + '> ' + bot
payload = {
    'content': content
}

header = {
    'authorization': 'NzQwNDcxMzUxNTQ1OTU0NDQ2.YOqm0A.Awavde7lwPhZp57S6BpuWWMIE-8'
}

r = requests.post('https://discord.com/api/v8/channels/850597103783641131/messages', data=payload, headers=header)