# GPT Web Applications Repository

This repository contains a collection of GPT-based web applications designed for various purposes, ranging from document analysis to generating quizzes and processing video content. Each application leverages the power of GPT models to provide unique functionalities.

## Applications Overview

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

