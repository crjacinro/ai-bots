from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, validator
from typing import List
from beanie import Document, Indexed, init_beanie

from errors import ApiBotException
from llm import QueryPrompt
from llm import get_completion
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




@app.post("/queries/{id}", status_code=status.HTTP_201_CREATED)
async def queries(id: str, query_prompt: QueryPrompt):
    try:
        # raise ApiBotException(code=422, message="Unable to create resource")
        response = get_completion(query_prompt)

        return {"response": response.strip()}

    except Exception as exc:
        handle_error(exc)


# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": "Invalid parameters provided"},
    )
@app.exception_handler(ApiBotException)
async def general_exception_handler(request: Request, exc: ApiBotException):
    return JSONResponse(
        status_code=exc.code,
        content={"code":exc.code, "message": exc.message},
    )
def handle_error(exc):
    if exc.code is None:
        raise ApiBotException(code=500, message="Internal server error")
    else:
        raise ApiBotException(code=exc.code, message=exc.message)
