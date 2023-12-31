from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict

from operator import itemgetter
import streamlit as st
import os
import json

st.set_page_config(
    page_title="DocumentGPT",
    page_icon="🫧",
)

class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    # unlimited arguments and keyword arguments
    # on_llm_start(1, 2, 3, 4, a=1, b=2, c=4)
    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)
        
        
llm = ChatOpenAI(
    temperature=0.1,
    streaming=True,
    callbacks=[
        ChatCallbackHandler(), 
    ],
)

memory_llm = ChatOpenAI(
    temperature=0.1,
)


if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationSummaryBufferMemory(
        llm=memory_llm,
        max_token_limit=120,
        memory_key="chat_history",
        return_messages=True,
    )


@st.cache_data(show_spinner="Embedding file...")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    
    with open(file_path, "wb") as f:
        f.write(file_content)
        
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=300,
        chunk_overlap=100,
    )
    
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

# message is what either user or ai writes.
def save_message(message, role):
    st.session_state["messages"].append({"message": message, "role": role})


def save_memory(input, output):
    st.session_state["chat_history"].append({"input": input, "output": output})
    
    
def save_memory_on_file(memory_file_path):
    print("work save memory on file")
    history = st.session_state["memory"].chat_memory.messages
    history = messages_to_dict(history)
    
    with open(memory_file_path, "w") as f:
        json.dump(history, f)
        
def restore_memory():
    print("working restore memory")
    for history in st.session_state["chat_history"]:
        st.session_state["memory"].save_context(
            {"input": history["input"]}, {"output": history["output"]}
        )
    
    
def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


def paint_history():
    for message in st.session_state["messages"]:
        send_message(
            message["message"],
            message["role"],
            save=False,
        )

def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


def invoke_chain(message):
    # invoke the chain
    result = chain.invoke(message)
    # save the interaction in the memory
    save_memory(message, result.content)
    
    
def load_memory_from_file(memory_file_path):
    print("work load memory from file")
    loaded_message = load_json(memory_file_path)
    history = messages_from_dict(loaded_message)
    st.session_state["memory"].chat_memory.messages = history



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Answer the question using ONLY the following context. If you don't
            know the answer, just say you don't know. DON'T Make anything up.
            
            Context: {context}
            """,
        ),
        ("human","{question}"),
    ]
)



st.title("DocumentGPT")

st.markdown(
"""
Welcome!!!

Use this chatbot to ask questions to an AI about your files!

Upload your files on the sidebar.
""")
      
with st.sidebar:  
    file = st.file_uploader(
        "Upload a .txt .pdf or .docx file", 
        type=["pdf", "txt", "docx"],
    )
    memory_checkbox = None
    memory_file_path = "./.cache/chat_memory/memory.json"
    if os.path.exists(memory_file_path):
        memory_checkbox = st.checkbox(
            "Do you want to keep your previous chat?", value=True
        )
        if memory_checkbox:
            load_memory_from_file(memory_file_path)

if file:
    if memory_checkbox:
        # Load memory
        memory_dict = load_json(memory_file_path)
    
    retriever = embed_file(file)
    send_message("I'm ready! Ask away!", "ai", save=False)
    paint_history()
    message = st.chat_input("Ask anything about your file...")
    if message:
        send_message(message, "human")
        
        
        # Below code can be replaced by using chain.
        
        # docs = retriever.invoke(message)
        # # a list of document, and each document has document.page_content
        # # we want to put all the page contents inside of the string using a seperator that is two line breaks 
        # docs = "\n\n".join(document.page_content for document in docs)
        # prompts = prompt.format_messages(context=docs, question=message)
        # llm.predict_messages(prompts)
        
        chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        } 
        | RunnablePassthrough.assign(
            chat_history=RunnableLambda(
                st.session_state["memory"].load_memory_variables
            )
            | itemgetter("chat_history")
        )
        | prompt 
        | llm
        )
        with st.chat_message("ai"):
            invoke_chain(message)
            
        if len(st.session_state["memory"].chat_memory.messages) != 0:
            save_memory_on_file(memory_file_path=memory_file_path)
        
        # search for the documents on our own, format the documents, then format the prompt,
        # give the prompt formateted to the llm.
        
        
        # Langchain will automatically run retriever from the user input.
        # input from the user: chain.invoke(message)
        
else:
    st.session_state["messages"] = []
    st.session_state["chat_history"] = []

