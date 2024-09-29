from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, validator
from typing import List
from beanie import Document, Indexed, init_beanie

from models import ConversationModel, ConversationListingModel, QueryPrompt, QueryRoleType, Message
from errors import ApiBotException, handle_error, raise_not_found_error
from llm import get_completion
import os

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
        await init_beanie(database=client.mydatabase, document_models=[ConversationModel])
    except Exception as exc:
        handle_error(exc)

@app.post("/conversations/", status_code=status.HTTP_201_CREATED)
async def create_conversations(conversation: ConversationModel):
    try:
        result = await conversation.insert()
        return {"id": str(result.id)}
    except Exception as exc:
        handle_error(exc)

@app.get("/conversations/", response_model=List[ConversationListingModel])
async def get_conversations():
    try:
        conversations = await ConversationModel.find_all().to_list()
        filtered: List[ConversationShortModel] = [{"name": c.name, "id": str(c.id)} for c in conversations]
        return filtered
    except Exception as exc:
        handle_error(exc)

@app.get("/conversations/{id}", response_model=ConversationModel)
async def get_conversations(id: str):
    try:
        result = await ConversationModel.get(id)
        if result is None:
            raise_not_found_error()

        return result
    except Exception as exc:
        handle_error(exc)

@app.put("/conversations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_conversations(id: str, conversation: ConversationModel):
    try:
        result = await ConversationModel.get(id)
        if result is None:
            raise_not_found_error()

        result.name = conversation.name
        result.llm_params = conversation.llm_params

        await result.replace()
    except Exception as exc:
        handle_error(exc)

@app.delete("/conversations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_conversations(id: str):
    try:
        result = await ConversationModel.get(id)
        if result is None:
            raise_not_found_error()

        await result.delete()
    except Exception as exc:
        handle_error(exc)


@app.post("/queries/{id}", status_code=status.HTTP_201_CREATED)
async def queries(id: str, query_prompt: QueryPrompt):
    try:
        conversation_result: ConversationModel = await ConversationModel.get(id)
        if conversation_result is None:
            raise_not_found_error()

        llm_params = conversation_result.llm_params
        response = get_completion(query_prompt, model=llm_params.model_name, temperature=llm_params.temperature)

        message = Message(user_message = query_prompt,llm_message= response)
        conversation_result.messages.append(message)

        await conversation_result.replace()
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
        content={"code": exc.code, "message": exc.message},
    )
