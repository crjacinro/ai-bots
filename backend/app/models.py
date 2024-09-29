from pydantic import BaseModel
from beanie import Document
from typing import List
from enum import Enum


class QueryRoleType(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    function = "function"


class QueryPrompt(BaseModel):
    role: QueryRoleType
    content: str


class QueryResponse(BaseModel):
    id: str
    response: str


class LlmParams(BaseModel):
    model_name: str
    temperature: float


class ConversationModel(Document):
    name: str
    llm_params: LlmParams
    messages: List[QueryPrompt] = []


class ConversationListingModel(BaseModel):
    id: str
    name: str
