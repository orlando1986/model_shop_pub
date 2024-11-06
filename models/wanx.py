from http import HTTPStatus
from dashscope import ImageSynthesis

API_KEY = 'sk-9024331ddd154d3ab563cca198625af9'

def simple_call(prompt):
    try:
        rsp = ImageSynthesis.call(model=ImageSynthesis.Models.wanx_v1,
                                prompt=prompt,
                                api_key=API_KEY,
                                n=1,
                                size='1024*1024')
        if rsp.status_code == HTTPStatus.OK:
            return rsp.output.results[0].url
        else:
            print('Failed, status_code: %s, code: %s, message: %s' %
                (rsp.status_code, rsp.code, rsp.message))
    except Exception as e:
        print(e)
    return None

def model_call(messages):
    for msg in messages:
        if 'role' in msg and msg['role'] == 'user':
            prompt = msg['content']
            return simple_call(prompt)
    return None
