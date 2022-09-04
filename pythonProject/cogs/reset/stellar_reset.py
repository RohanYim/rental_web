import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
import os


login_url = 'https://discord.com/login'
url = 'https://account.stellara.io/'

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(10)

# browser.get(login_url)
# browser.find_element_by_name("email").send_keys("iwannabuyu@gmail.com")
# browser.find_element_by_name("password").send_keys("Zjw825shr10fen_")
# browser.find_element_by_class_name("sizeLarge-1vSeWK").click()
# time.sleep(30)

# browser.get(url)
# time.sleep(60)
# with open('cookies.txt','w') as cookief:
#     cookief.write(json.dumps(browser.get_cookies()))
#
# browser.close()


browser.get(url)
with open('cookies.txt','r') as cookief:
    #使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookieslist = json.load(cookief)
    for cookie in cookieslist:
        browser.add_cookie(cookie)
# browser.refresh()
# time.sleep(5)
# browser.close()
# command = '!deactivate'
# time.sleep(10)
# browser.find_element_by_class_name("accentButton").click()
# time.sleep(5)
# browser.find_element_by_link_text("Reset").click()
# time.sleep(10)
# browser.get(login_url)
# browser.find_element_by_class_name("button_danger__c1xhy").click()
# browser.find_element_by_class_name("button_danger__c1xhy").click()
# time.sleep(5)
# browser.find_element_by_class_name("input-2_SIlA").click()
# browser.find_element_by_class_name("input-2_SIlA").send_keys(command, Keys.ENTER)

# time.sleep(10)
#
# browser.close()

# os.system('taskkill /im chromedriver.exe /F')
