from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.chat_models import ChatOpenAI
import streamlit as st

st.set_page_config(
    page_title="DocumentGPT",
    page_icon="🫧",
)

llm = ChatOpenAI(
    temperature=0.1,
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

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        # message is what either user or ai writes.
        st.session_state["messages"].append({"message": message, "role": role})


def paint_history():
    for message in st.session_state["messages"]:
        send_message(
            message["message"],
            message["role"],
            save=False,
        )

def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
     Answer the question using ONLY the following context. If you don't
     know the answer, just say you don't know.
     DON'T Make anything up.
     
     Context: {context}
     """,
     ),
    ("human","{question}")
])



st.title("DocumentGPT")

st.markdown("""
Welcome!

Use this chatbot to ask questions to an AI about your files!

Upload your files on the sidebar.
""")
      
with st.sidebar:  
    file = st.file_uploader(
        "Upload a .txt .pdf or .docx file", 
        type=["pdf", "txt", "docx"],
        )

if file:
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
        
        chain = {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        } | prompt | llm
        response = chain.invoke(message)
        send_message(response.content, "ai")
        
        # search for the documents on our own, format the documents, then format the prompt,
        # give the prompt formateted to the llm.
        
        
        # Langchain will automatically run retriever from the user input.
        # input from the user: chain.invoke(message)
        
else:
    st.session_state["messages"] = []
