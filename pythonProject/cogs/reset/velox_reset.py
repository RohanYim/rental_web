import time
from selenium import webdriver
import requests
import configparser
import sys

seller = sys.argv[1]

CONFIG_FILE = "C:\\Users\\Administrator\\PycharmProjects\\pythonProject\\cogs\\reset\\reset_config.cfg"

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
token = config.get(seller, 'token')
velox_channel = config.get(seller, "velox_channel")

payload = {
    'content': '!deactivate'
}

header = {
    'authorization': token
}

r = requests.post('https://discord.com/api/v8/channels/' + velox_channel + '/messages', data=payload, headers=header)



