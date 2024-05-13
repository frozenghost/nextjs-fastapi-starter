from time import time
import api.settings
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.database.database import ChatHistory, async_session, engine
from api.common import CommonResponse, StaticString

import aiohttp
import asyncio

app = FastAPI()

# CORS middleware for allowing cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dog_breed/",response_model=CommonResponse)
async def get_dog_breed(input:str, background_tasks: BackgroundTasks):
    start_time = time()
    history = ChatHistory();
    history.input_value = input
    if input.isdigit() and 1 <= int(input) <= 8:
        history.valid_input = True
        # Generate random dog images
        dog_images = []
        task_list = []
        async with aiohttp.ClientSession() as session:
            for _ in range(int(input)):
                task = asyncio.create_task(get_dog_breed_image(session))
                task_list.append(task)
            
            done, pending = await asyncio.wait(task_list, timeout=None)
            for done_task in done:
                dog_images.append(done_task.result())

            history.images = dog_images
            end_time = time()
            history.execute_duration = (end_time - start_time) * 1000
            background_tasks.add_task(save_chat_history, history)
            return CommonResponse(data=dog_images)
    else:
        history.valid_input = False
        end_time = time()
        history.execute_duration = (end_time - start_time) * 1000
        await save_chat_history(history=history)
        # Invalid input
        # await save_chat_history(input_text, False, "Please introduce any number between 1 and 8")
        raise HTTPException(status_code=400, detail="Please introduce any number between 1 and 8")
    # finally:
    #     background_tasks.add_task(save_chat_history, history)
    
    
async def save_chat_history(history):
    async with async_session() as session:
        session.add(history)
        await session.commit()



async def get_dog_breed_image(session: aiohttp.ClientSession) -> str:
    async with session.get(StaticString.DOG_IMAGE_SOURCE) as response:
        print(await response.text())
        data = await response.json()
        return data["message"]
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content=CommonResponse(data=None, error=exc.detail, success=False).model_dump())

@app.exception_handler(RequestValidationError)
async def exception_handler(request, exc):
    return JSONResponse(status_code=422, content=CommonResponse(data=None, error=StaticString.INVALID_INPUT, success=False).model_dump())