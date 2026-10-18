
# Multi-PDF RAG Assistant

A local Retrieval-Augmented Generation (RAG) application that answers questions using information retrieved from multiple PDF documents.

## Features

- Load multiple PDFs from a single folder
- Extract text and split documents into chunks
- Generate embeddings locally using Ollama
- Store and retrieve document chunks using Chroma
- Generate answers using a local language model
- Display source PDF filenames and page numbers
- Filter low-scoring retrieval results using a relevance threshold

## RAG Pipeline

PDF Documents → Text Extraction → Chunking → Embeddings → Chroma Vector Store → Retrieval → Local LLM → Answer + Sources

## Technologies Used

- Python
- LangChain
- ChromaDB
- Ollama
- Qwen 2.5 0.5B Instruct
- Nomic Embed Text
- PyPDF

## How It Works

1. The application finds PDF files in the `documents/` folder.
2. It extracts each PDF's pages and records the source filename.
3. The extracted text is split into overlapping chunks.
4. An embedding model converts chunks into numerical vectors.
5. Chroma stores the chunks and their embeddings.
6. When a user asks a question, the application retrieves relevant chunks.
7. The local language model generates an answer from the retrieved context.
8. The application displays source filenames and page numbers.

## Requirements

- Python 3.10 or newer
- Ollama installed and running
- The following Ollama models:
  - `qwen2.5:0.5b-instruct`
  - `nomic-embed-text`

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd multi-pdf-rag
```

Replace `YOUR_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 4. Download the Ollama models

```powershell
ollama pull qwen2.5:0.5b-instruct
ollama pull nomic-embed-text
```

### 5. Add your PDFs

Place your own PDF files inside the `documents/` folder.

### 6. Run the application

```powershell
python main.py
```

Type `exit` to stop the application.

## Example Questions

- What is inheritance in Java?
- What are lists in Python?
- What is a class?

## Project Structure

```text
multi-pdf-rag/
├── documents/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Current Limitations

- Answer quality depends on the retrieved text and the local language model.
- The relevance threshold is a simple filtering rule, not a guarantee of correctness.
- The vector store is rebuilt when the application starts.
- The application currently uses a terminal-based interface.
- Retrieved sources indicate which passages were selected, not proof that every generated claim is correct.

## What I Learned

- Loading and processing multiple PDF documents
- Text chunking and overlapping chunks
- Embeddings and vector similarity search
- Using Chroma for vector storage
- Using a local LLM through Ollama
- Tracking document metadata and source pages
- Understanding retrieval relevance and hallucinations

## Privacy

Run the application locally with Ollama. Documents are processed by the local application and local models; this project does not require a paid LLM API.

## License

Add a license if you want to specify the terms under which others may use and distribute this project.
