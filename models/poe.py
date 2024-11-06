# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

import time

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
browser = webdriver.Chrome(options=options)
for handle in browser.window_handles:
    browser.switch_to.window(handle)
    if ('poe' in browser.current_url):
        break
else:
    print('no Poe found')

#https://poe.com/
print(f"Poe title is: {browser.title}")

def poe_new_conversation():
    new_chat = browser.find_element(By.CLASS_NAME, "Button_buttonBase__Bv9Vx.Button_flat__dcKQ1.ChatBreakButton_button__zyEye.ChatMessageInputFooter_chatBreakButton__sGik8")
    new_chat.click()
    time.sleep(1)

def model_call(messages: list):
    poe_new_conversation()

    prompt = messages[-1]["content"]
    input_text = browser.find_element(By.CLASS_NAME, 'GrowingTextArea_textArea__ZWQbP')

    prompt = prompt.replace('\r\n', '\n')
    if '\n' in prompt:
        textsplit = prompt.split("\n") # explode
        textsplit_len = len(textsplit) - 1 # get last element
        for text in textsplit:
            input_text.send_keys(text)
            if textsplit.index(text) != textsplit_len: # do what you need each time, if not the last element
                input_text.send_keys(Keys.SHIFT + Keys.ENTER)
                pass
    else:
        input_text.send_keys(prompt)
    input_text.send_keys(Keys.ENTER)
    time.sleep(2)

    try:
        recommend = browser.find_elements(By.CLASS_NAME, 'ChatMessageFollowupActions_container__0Mrhg')
        while (len(recommend) == 0):
            recommend = browser.find_elements(By.CLASS_NAME, 'ChatMessageFollowupActions_container__0Mrhg')
            time.sleep(2)
    except NoSuchElementException:
        print("stop button not showing up")
        pass

    time.sleep(2)
    try:
        message = browser.find_elements(By.CLASS_NAME, 'ChatMessage_chatMessage__xkgHx')[-1]
        message = message.find_element(By.CLASS_NAME, 'Markdown_markdownContainer__Tz3HQ')
        message = message.find_elements(By.TAG_NAME, 'p')
        response = [m.get_attribute("innerText") for m in message]
        response = '\n'.join(response)
    except NoSuchElementException as e:
        print(f"Markdown_markdownContainer__Tz3HQ dismissed: {e}")

    return response

if __name__ == "__main__":
    messages = [{"role": "user", "content": "How are you?"}]
    res = model_call(messages)
    print(res)