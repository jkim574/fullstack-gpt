# Full-Stack GPT

Full-Stack GPT is an innovative project that harnesses the capabilities of GPT (Generative Pre-trained Transformer) models in a full-stack environment. This project showcases a diverse range of applications, from document processing to interactive web applications, all powered by the advanced AI of GPT models. It demonstrates how GPT can be integrated into various aspects of a web-based platform, providing intelligent and automated solutions to complex tasks.


## Table of Contents
- 
-
-
-



## Features

- 🔍 Langchain Integration: Utilizes Langchain for seamless integration of GPT models, offering advanced functionalities like text summarization and question answering based on uploaded documents.

- 🌐 Streamlit Web Framework: Leverages Streamlit for creating intuitive and interactive web interfaces, enabling users to interact with GPT-powered applications effortlessly.

- 🧠 GPT-3.5 & GPT-4 Models: Employs GPT-3.5 and GPT-4 instances for robust text generation, offering high-quality responses and content creation.

- 🍳 ChefGPT for Korean Cuisine: A specialized feature providing Korean recipe suggestions based on input ingredients, blending culinary arts with AI technology.

- 📊 Efficient Data Retrieval: Incorporates vector search technology using Pinecone for efficient and relevant data retrieval.

- 👩‍🏫 Educational Quizzes: Generates interactive quizzes from documents or Wikipedia articles, enhancing learning experiences.

- 🔒 Privacy-Focused Features: Offers offline processing options for privacy-conscious users, ensuring data security.


## Requirements

- Python 3.11.6
- OpenAI API key
- Pinecone API key
- Check 'requirements.txt' for more details
- Pydantic for data validation
- Cloudflare for temporary URL generation and deployment


## Installations




## GPT Web Applications

### 1. DocumentGPT

DocumentGPT creates an interface for a GPT-based chatbot capable of answering questions about uploaded files such as .txt, .pdf, or .docx. I used the `langchain` library for processing and embedding files, and `streamlit` for the web interface. Key features include embedding file contents, managing chat history, and a chat interface for document-related queries.

---

### 2. PrivateGPT

PrivateGPT is designed with a focus on privacy, processing data offline. This script utilizes `ollama` embeddings, indicating a distinct language model approach for handling sensitive data. It ensures that all data processing is done locally, avoiding the transmission of data to external servers.

---

### 3. QuizGPT

QuizGPT is an application for creating quizzes from user-uploaded documents or Wikipedia articles. It combines the `langchain` library and `streamlit` for quiz generation. The GPT model formulates both questions and answers based on the content provided, allowing users to test their knowledge on various topics.

---

### 4. SiteGPT

SiteGPT is designed to answer questions about the content of specific websites. It processes website content using a sitemap loader and a GPT model for answering queries. The user interface includes functionality for entering a website URL and posing questions, with the script providing relevant answers.

---

### 5. MeetingGPT

MeetingGPT focuses on processing video files to generate transcripts, summaries, and Q&A about the video content. It involves steps such as audio extraction, transcription, and text summarization, utilizing GPT models for generating summaries and answering related questions. Users can upload videos for a comprehensive transcript, summary, and an interactive Q&A chatbot.

---




# ChefGPT

`ChefGPT.py` is a central component of my project, utilizing FastAPI and GPT technologies to revolutionize the discovery of Korean recipes. This application blends the speed of FastAPI with cutting-edge AI to offer a unique culinary experience.

## Features

### FastAPI for Efficient Web Service

- **Asynchronous Capabilities**: Built on FastAPI, ChefGPT efficiently handles multiple web requests concurrently, ensuring a smooth user experience.
- **Scalability**: Designed to be robust and scalable, catering to a growing number of users.

### Cutting-Edge AI Integration

- **GPT and Vector Search**: Utilizes OpenAIEmbeddings from the langchain library for converting recipe data into vectors, enabling efficient similarity searches.
- **Relevant Results**: Ensures the recipes suggested are closely aligned with the user's ingredient input.

### Simplified Recipe Discovery

- **HTTP GET Endpoint**: Features a `/recipes` endpoint that accepts ingredients as input and returns a list of matching Korean recipes.
- **User-Friendly Format**: Recipes are presented in a Document object format, detailing both the recipe and preparation instructions.

### Secure and Temporary URL Deployment

- **Cloudflare Integration**: Uses Cloudflare for creating temporary URLs, providing a secure and isolated testing environment.
- **Ease of Access**: Simplifies access to the application without complex deployment processes.

### Environment Management

- **dotenv for Configuration**: Utilizes dotenv for efficient and secure management of application settings and API keys.

## Getting Started

To get started with ChefGPT, clone the repository and follow the installation instructions provided in the `INSTALL.md` file.


