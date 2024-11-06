# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import time

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
browser = webdriver.Chrome(options=options)
for handle in browser.window_handles:
    browser.switch_to.window(handle)
    if ('chatgpt' in browser.current_url):
        break
else:
    print('no ChatGPT found')

#https://chatgpt.com/
print(f"ChatGPT title is: {browser.title}")

def chatgpt_new_conversation():
    new_chat = browser.find_element(By.CLASS_NAME, "bg-token-sidebar-surface-primary.pt-0")
    new_chat.click()
    time.sleep(1)

def model_call(messages: list):
    chatgpt_new_conversation()

    prompt = messages[-1]["content"]
    input_text = browser.find_element(By.ID, 'prompt-textarea')

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
        recommend = browser.find_elements(By.CLASS_NAME, 'items-center.justify-start.rounded-xl.p-1.flex')
        while (len(recommend) == 0):
            recommend = browser.find_elements(By.CLASS_NAME, 'items-center.justify-start.rounded-xl.p-1.flex')
            time.sleep(2)
    except NoSuchElementException:
        print("stop button not showing up")
        pass

    time.sleep(2)
    try:
        message = browser.find_elements(By.CLASS_NAME, 'markdown')[-1]
        message = message.find_elements(By.TAG_NAME, 'p')
        response = [m.get_attribute("innerText") for m in message]
        response = '\n'.join(response)
    except NoSuchElementException as e:
        print(f"markdown.prose.w-full.break-words.dark:prose-invert.light dismissed: {e}")

    return response

if __name__ == "__main__":
    messages = [{"role": "user", "content": "How are you?"}]
    response = model_call(messages)
    print(response)