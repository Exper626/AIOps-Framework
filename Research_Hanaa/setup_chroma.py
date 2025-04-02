import os
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pypdf import PdfReader

# Path to store database
CHROMA_DB_DIR = "embeddings"
PDF_DIR = "E:\\LLM675930\dataset"

# Initialize SentenceTransformer for local embeddings
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
    return text


# Initialize ChromaDB and store embeddings
def initialize_chroma():
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    collection = client.get_or_create_collection(
        name="telecom_finance",
        embedding_function=embedding_function
    )

    if not os.path.exists(PDF_DIR):
        print(f"📂 No PDFs found in {PDF_DIR}. Please add your files!")
        return

    for pdf_file in os.listdir(PDF_DIR):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, pdf_file)
            print(f"📄 Processing {pdf_file}...")

            text = extract_text_from_pdf(pdf_path)
            if text.strip():
                collection.add(
                    ids=[pdf_file],
                    documents=[text],
                    metadatas=[{"source": pdf_file}]
                )
                print(f"✅ {pdf_file} added to ChromaDB")
            else:
                print(f"⚠️ No extractable text in {pdf_file}")

if __name__ == "__main__":
    initialize_chroma()