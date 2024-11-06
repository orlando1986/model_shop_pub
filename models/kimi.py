# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import platform
import asyncio
import time

if platform.system() == 'Windows':
   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
browser = webdriver.Chrome(options=options)
for handle in browser.window_handles:
    browser.switch_to.window(handle)
    if ('Kimi.ai' in browser.title):
        break
else:
    print('no kimi found')

#https://kimi.moonshot.cn/
print(f"Kimi title is: {browser.title}")

def kimi_new_conversation():
    new_chat = browser.find_element(By.CLASS_NAME, 'myAgentTool___Y1_mC')
    new_chat.click()
    time.sleep(1)

def model_call(messages: list):
    kimi_new_conversation()

    prompt = messages[-1]["content"]
    searchbox = browser.find_element(By.CLASS_NAME, 'editorContentEditable___FZJd9')
    prompt = prompt.replace('\r\n', '\n')
    if '\n' in prompt:
        textsplit = prompt.split("\n") # explode
        textsplit_len = len(textsplit) - 1 # get last element
        for text in textsplit:
            searchbox.send_keys(text)
            if textsplit.index(text) != textsplit_len: # do what you need each time, if not the last element
                searchbox.send_keys(Keys.SHIFT + Keys.ENTER)
    else:
        searchbox.send_keys(prompt)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(2)

    try:
        recommend = browser.find_elements(By.CLASS_NAME, 'MuiBox-root.css-2wedsf')
        while (len(recommend) == 0):
            recommend = browser.find_elements(By.CLASS_NAME, 'MuiBox-root.css-2wedsf')
            time.sleep(2)
    except NoSuchElementException:
        print("stop button not showing up")
        pass

    time.sleep(2)

    responses = browser.find_elements(By.CLASS_NAME, 'markdown___vuBDJ')
    response = responses[-1].text

    return response

if __name__ == "__main__":
    messages = [{"role": "user", "content": "How are you?"}]
    resp = model_call(messages)
    print(resp)