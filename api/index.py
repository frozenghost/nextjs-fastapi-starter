from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.dtos.dog_breed import DogBreedRequest
from api.common import CommonResponse, StaticString
from pydantic import conint

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
async def get_dog_breed(input:conint(ge=1, le=8)):
    if 1 <= input <= 8:
        # Generate random dog images
        dog_images = []
        task_list = []
        async with aiohttp.ClientSession() as session:
            for _ in range(input):
                task = asyncio.create_task(get_dog_breed_image(session))
                task_list.append(task)
            
            done, pending = await asyncio.wait(task_list, timeout=None)
            for done_task in done:
                dog_images.append(done_task.result())
            # Save chat history
            # await save_chat_history(input_text, True, dog_images)

            return CommonResponse(data=dog_images)
    else:
        # Invalid input
        # await save_chat_history(input_text, False, "Please introduce any number between 1 and 8")
        raise HTTPException(status_code=400, detail="Please introduce any number between 1 and 8")


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