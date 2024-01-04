import json
import streamlit as st
from langchain.retrievers import WikipediaRetriever
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser


st.set_page_config(page_title="QuizGPT", page_icon="❓")


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)

# The reason for using double bracket, is to not letting langchain to get confused.
# It's helpful to add output format '''json
# This will not let LLM to reply as such: "Certainly! I would like to answer that!"
function = {
    "name": "create_quiz",
    "description": "function that takes a list of questions and answers and returns a quiz",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                        },
                        "answers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "answer": {
                                        "type": "string",
                                    },
                                    "correct": {
                                        "type": "boolean",
                                    },
                                },
                                "required": ["answer", "correct"],
                            },
                        },
                    },
                    "required": ["question", "answers"],
                },
            }
        },
        "required": ["questions"],
    },
}


llm = ChatOpenAI(
    temperature=0.1,
    model="gpt-3.5-turbo-1106",
    streaming=True,
    callbacks=[
        StreamingStdOutCallbackHandler(),
    ],
).bind(
    function_call={
        "name": "create_quiz",
    },
    functions=[
        function,
    ],
)


questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
    You are a helpful assistant that is role playing as a teacher.
            
    Based ONLY on the following context make 10 (TEN) questions minimum to test the user's knowledge about the text.

    Each question should have 4 answers, three of them must be incorrect and one should be correct.

    Context: {context}
    """,
        )
    ]
)


questions_chain = {"context": format_docs} | questions_prompt | llm


@st.cache_data(show_spinner="Loading file...")
def split_file(file):
    file_content = file.read()
    file_path = f"./.cache/quiz_files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs

# caching the document that already uploaded.
# The reason for caching is to save time when re-run the same documents.
# @st.cache_data(show_spinner="Making quiz...")
# The reason why it should be _docs is that if we just say docs, 
# docs parameter is not hashable 
@st.cache_data(show_spinner="Making quiz...")
def run_quiz_chain(_docs, topic):
    response = questions_chain.invoke(_docs)
    response = response.additional_kwargs["function_call"]["arguments"]
    return json.loads(response)

# caching the wikipedia search
# cache data hash the parameter "term".
# so if this function is called again, and signature of this function doesnt change.
# Then the streamlit knows that this function should not run again.
# So it gives the previous values.
@st.cache_data(show_spinner="Searching Wikipedia...")
def wiki_search(term):
    retriever = WikipediaRetriever(top_k_results=1)
    docs = retriever.get_relevant_documents(term)
    return docs


st.title("QuizGPT")

# decide if the user wants to upload a file or use wikipedia
with st.sidebar:
    docs = None
    topic = None
    choice = st.selectbox(
        "Choose what you want to use.",
        (
            "File",
            "Wikipedia Article",
        ),
    )

    if choice == "File":
        file = st.file_uploader(
            "Upload a .docx, .txt or .pdf file", type=["pdf", "txt", "docx"]
        )

        if file:
            docs = split_file(file)
    else:
        topic = st.text_input("Search Wikipedia...")
        if topic:
            docs = wiki_search(topic)

if not docs:
    st.markdown(
        """
    Welcome to QuizGPT.
                
    I will make a quiz from Wikipedia articles or files you upload to test your knowledge and help you study.
                
    Get started by uploading a file or searching on Wikipedia in the sidebar.
    """
    )
else:
    response = run_quiz_chain(docs, topic if topic else file.name)
    with st.form("questions_form"):
        for idx, question in enumerate(response["questions"]):
            st.write(question["question"])
            value = st.radio(f"Select an option {idx}", [answer["answer"] for answer in question["answers"]],
                index=None,
            )
            if {"answer": value, "correct": True} in question["answers"]:
                st.success("Correct!")
            elif value is not None:
                st.error("Wrong!")
        button = st.form_submit_button()
        
    