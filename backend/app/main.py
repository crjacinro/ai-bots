from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from openai import OpenAI
from pydantic import BaseModel, Field, validator
from typing import List
from beanie import Document, Indexed, init_beanie
import os

app = FastAPI()


# MongoDB model
class Item(Document):
    name: str
    description: str


# Initialize MongoDB
@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    await init_beanie(database=client.mydatabase, document_models=[Item])


# Set OpenAI API key
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items/")
async def create_item(item: Item):
    await item.insert()
    return {"message": "Item created successfully"}


@app.get("/items/", response_model=List[Item])
async def get_items():
    print("sdf")
    items = await Item.find_all().to_list()
    return items


MODEL_TEMPERATURE = 0.25
MODEL_LLM = "gpt-3.5-turbo"
ENABLE_LLM_API_MOCK = True


class QueryPrompt(BaseModel):
    role: str
    content: str

    @validator("role")
    def validate_role(cls, value):
        if value is None:
            raise ValueError("Price must be greater than zero")
        return value


class ApiBotException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": "Invalid parameters provided"},
    )

@app.exception_handler(ApiBotException)
async def unicorn_exception_handler(request: Request, exc: ApiBotException):
    return JSONResponse(
        status_code=exc.code,
        content={"code":exc.code, "message": exc.message},
    )

@app.post("/queries/{id}", status_code=status.HTTP_201_CREATED)
async def queries(id: str, query_prompt: QueryPrompt):
    try:

        # raise ApiBotException(code=422, message="Unable to create resource")

        response = get_completion(query_prompt)

        return {"response": response.strip()}

    except Exception as exc:
        if exc.code is None:
            raise ApiBotException(code=500, message="Internal server error")
        else:
            raise ApiBotException(code=exc.code, message=exc.message)


def get_completion(query_prompt: QueryPrompt, model=MODEL_LLM):
    messages = [{"role": query_prompt.role, "content": query_prompt.content}]

    if ENABLE_LLM_API_MOCK:
        return "This is a mock chat GPT!"

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=MODEL_TEMPERATURE
    )
    return response.choices[0].message.content
