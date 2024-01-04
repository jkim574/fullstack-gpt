# FastAPI is a framework for building server, like Flask.
from typing import Any, Dict
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import pinecone
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone


app = FastAPI(
    title="ChefGPT. The best provider of Korean Recipes in the world",
    description="Give CheftGPT a couple of ingredients and it will give recipes in return.",
    servers=[
        {"url":"https://spec-hc-heater-door.trycloudflare.com"}
    ]
)


# FastAPI doesn't load .env file.

load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment="gcp-starter",
)

embeddings = OpenAIEmbeddings()

vector_store = Pinecone.from_existing_index(
    "recipes",
    embeddings,
)


# Pydantic model
class Document(BaseModel):
    page_content: str

@app.get(
    "/recipes",
    summary="Returns a list of recipes.",
    description="Upon receiving an ingredient, this endpoint will return a list of recipes that contain that ingredient.",
    response_description="A Document object that contains the recipe and preparation instructions",
    response_model=list[Document],
    openapi_extra={
        "x-openai-isConsequential": False,
    },
)

# hit command cloudflared tunnel --url http://127.0.0.1:8000
# Paste that url.
# https://spec-hc-heater-door.trycloudflare.com 
def get_recipe(ingredient: str):
    docs = vector_store.similarity_search(ingredient)
    return docs


def get_example():
    return {
        "quote": "Life is hsort so eat is all."
    }
    
def get_quote(request: Request):
    print(request.header)
    return {"quote": "Life is short so eat it all.",
            "year": 1958, }