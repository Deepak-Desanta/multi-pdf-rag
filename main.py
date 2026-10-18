
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma


# 1. Find and load all PDFs
pdf_folder = Path("documents")
pdf_files = sorted(pdf_folder.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError("No PDF files found in the documents folder.")

documents = []

for pdf_file in pdf_files:
    loader = PyPDFLoader(str(pdf_file))
    pdf_documents = loader.load()

    for document in pdf_documents:
        document.metadata["source"] = pdf_file.name

    documents.extend(pdf_documents)
    print(f"Loaded {pdf_file.name}: {len(pdf_documents)} pages")

print(f"\nTotal PDFs: {len(pdf_files)}")
print(f"Total pages: {len(documents)}")


# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")


# 3. Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")


# 4. Store chunks in Chroma
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="multi_pdf_notes"
)

print("Embeddings created and stored!")


# 5. Load the local LLM
llm = OllamaLLM(model="qwen2.5:0.5b-instruct")


# 6. Ask questions across all PDFs
while True:
    query = input("\nAsk your PDFs (type 'exit' to quit): ")

    if query.lower().strip() == "exit":
        break

    results = vector_store.similarity_search_with_relevance_scores(
        query,
        k=5
    )

    if not results or results[0][1] < 0.4:
        print("\n--- Answer ---")
        print("I couldn't find enough information in your notes.")
        continue

    retrieved_documents = [result[0] for result in results]

    context = "\n\n".join(
        document.page_content for document in retrieved_documents
    )

    prompt = f"""
Answer using only the supplied PDF context.

Rules:
- Do not use outside knowledge.
- If the context doesn't answer the question, say:
  "I couldn't find enough information in your notes."
- Keep the answer clear and concise.

Context:
{context}

Question:
{query}

Answer:
"""

    answer = llm.invoke(prompt)

    print("\n--- Answer ---")
    print(answer)

    print("\n--- Sources ---")
    seen_sources = set()

    for document in retrieved_documents:
        source = document.metadata.get("source", "Unknown PDF")
        page = document.metadata.get("page")

        if page is not None:
            source_info = (source, page + 1)

            if source_info not in seen_sources:
                seen_sources.add(source_info)
                print(f"{source} — Page {page + 1}")
