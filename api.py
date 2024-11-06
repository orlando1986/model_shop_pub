from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],   # 允许所有HTTP方法
    allow_headers=["*"]    # 允许所有请求头
)
                       
class ChatCompletionRequest(BaseModel):
    model: str
    messages: list

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    if request.model == "poe":
        from models.poe import model_call
    elif request.model == "kimi":
        from models.kimi import model_call
    elif request.model == "haiku":
        from models.haiku import model_call
    elif request.model == "sonnet":
        from models.sonnet import model_call
    elif request.model == "sonnet-cheap":
        from models.sonnet import model_call_cheap as model_call
    elif request.model == "kimi-api":
        from models.kimi_api import model_call
    elif request.model == "spark":
        from models.spark import model_call
    elif request.model == "chatgpt":
        from models.chatgpt import model_call
    elif request.model == "yi":
        from models.yi import model_call
    elif request.model == "wanx-v1":
        from models.wanx import model_call
    else:
        from models.zhipu import model_call

    response = model_call(request.messages)
    if response is None:
        return {'error':429, 'message':"Too Many Requests"}

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response
                }
            }
        ],
        "model": request.model
    }

if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=9999)
    uvicorn.run(app, host="127.0.0.1", port=9999)
