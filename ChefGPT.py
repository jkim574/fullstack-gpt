# FastAPI is a framework for building server, like Flask.
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import pinecone
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone



# If you have shut down server and then rebooting, then you have to update the url
# Quick tunnel, which is meant for experimentation and does not require a Cloudflare account, 
# Tt's important to note that these tunnels have no uptime guarantee and are intended for temporary use. 
# If you restart the tunnel, it's likely to generate a new URL each time.
# cloudflared tunnel --url (your url address) 
app = FastAPI(
    title="ChefGPT. The best provider of Korean Recipes in the world",
    description="Give CheftGPT a couple of ingredients and it will give recipes in return.",
    servers=[
        {"url":"https://algeria-connector-for-ef.trycloudflare.com"}
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

    
