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
balko_channel = config.get(seller, "balko_channel")

payload = {
    'content': '!help'
}

header = {
    'authorization': token
}

r = requests.post('https://discord.com/api/v8/channels/'+ balko_channel + '/messages', data=payload, headers=header)



