from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, validator
from typing import List
from beanie import Document, Indexed, init_beanie

from errors import ApiBotException, handle_error
from llm import QueryPrompt
from llm import get_completion
import os

app = FastAPI()

class Interaction(BaseModel):
    user_message: str
    llm_message: str

class ConversationModel(Document):
    name: str
    params: Interaction


# Initialize MongoDB
@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    await init_beanie(database=client.mydatabase, document_models=[ConversationModel])

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/conversations/", status_code=status.HTTP_201_CREATED)
async def create_conversations(conversation: ConversationModel):
    result = await conversation.insert()
    return {"id": str(result.id)}

@app.get("/conversations/", response_model=List[ConversationModel])
async def get_conversations():
    items = await ConversationModel.find_all().project(ConversationModel.id).to_list()
    return items



@app.post("/queries/{id}", status_code=status.HTTP_201_CREATED)
async def queries(id: str, query_prompt: QueryPrompt):
    try:
        response = get_completion(query_prompt)
        return {
            "id": id,
            "response": response.strip()
        }
    except Exception as exc:
        handle_error(exc)


# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    bad_request_code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(
        status_code=bad_request_code,
        content={"code": bad_request_code, "message": "Invalid parameters provided"},
    )
@app.exception_handler(ApiBotException)
async def general_exception_handler(request: Request, exc: ApiBotException):
    return JSONResponse(
        status_code=exc.code,
        content={"code":exc.code, "message": exc.message},
    )

