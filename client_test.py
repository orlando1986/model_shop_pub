
import requests
import json
'''
url = "http://127.0.0.1:9999/v1/chat/completions"

headers = {'Content-Type': 'application/json'}

data = {
    "model": "poe",
    "messages": [{"role": "user", "content": "who are you?"}],
}
data_json = json.dumps(data)

response = requests.post(url, headers=headers, data=data_json)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
'''

from openai import OpenAI

client = OpenAI(api_key="1234", base_url="http://127.0.0.1:9999/v1")

resp = client.chat.completions.create(
    model="wanx",
    messages=[{"role": "user", "content": "Mouse rides elephant"}],
)

print(resp)
