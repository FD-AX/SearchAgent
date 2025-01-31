from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from model import ai_agent
import json
import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    id: int

class QueryResponse(BaseModel):
    id: int
    answer: Optional[int]
    reasoning: str
    sources: List[str]


def get_sources() -> List[str]:
    return ["https://itmo.ru/ru/", "https://abit.itmo.ru/"]

@app.post("/api/request", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    answer = ai_agent(request.query)
    reasoning = "Главный кампус Университета ИТМО расположен в Санкт-Петербурге."
    sources = get_sources()
    
    return QueryResponse(
        id=request.id,
        answer=answer,
        reasoning=reasoning,
        sources=sources
    )