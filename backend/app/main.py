from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from beanie import init_beanie

from models import ConversationModel, ConversationListingModel, QueryPrompt, QueryRoleType, QueryResponse
from errors import ApiBotException, handle_error, raise_not_found_error
from llm import get_completion
import os

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        filtered = [{"name": c.name, "id": str(c.id)} for c in conversations]
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


@app.post("/queries/{id}", status_code=status.HTTP_201_CREATED, response_model=QueryResponse)
async def queries(id: str, query_prompt: QueryPrompt):
    try:
        conversation_result: ConversationModel = await ConversationModel.get(id)
        if conversation_result is None:
            raise_not_found_error()

        llm_params = conversation_result.llm_params

        response = get_completion(query_prompt=query_prompt, context=conversation_result.messages,
                                  model=llm_params.model_name,
                                  temperature=llm_params.temperature)

        conversation_result.messages.append(query_prompt)
        conversation_result.messages.append(QueryPrompt(role=QueryRoleType.assistant, content=response))

        await conversation_result.replace()

        return QueryResponse(id=id, response=response.strip())

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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Chatbots API",
        version="1.0.0",
        summary="This project is a FastAPI Python application that simulates chat interfaces to ChatGPT",
        description="It uses Beanie as the Object-Document Mapper (ODM) to interact with MongoDB. "
                    "It is containerized using Docker for easy setup and deployment.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
