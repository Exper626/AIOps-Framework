import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb 
import numpy as np
import ollama
import glob
import multiprocessing
from chromadb.utils import embedding_functions
import torch



def device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"



def filePaths(source : str) -> list:

    if source == "company":
        folder_path = "Data/Company/*" 
        return [f for f in glob.glob(folder_path) if not f.endswith('/')]

    elif source == "network":
        folder_path = "Data/network/*"  
        return [f for f in glob.glob(folder_path) if not f.endswith('/')]



def imageToWords():
    raise NotImplemented;



def tokenizer(fileList : list) -> str:

    text = ""

    for filePath in fileList:
        reader = PdfReader(filePath)
        text += "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    with open("Tokens.txt" , "w", encoding="utf-8") as file:
        file.write(text)

    return text 



def embedding_text(topic : str , text : str, sentence_transformer = "all-MiniLM-L6-v2", chunk_size = 500) -> tuple[np.ndarray, list]:

    embedding_model = SentenceTransformer(sentence_transformer).to(device())

    def chunk_text(text, chunk_size):
        return [text[ i : i + chunk_size] for i in range(0,len(text), chunk_size)]

    chunks = chunk_text(text, chunk_size)
    embeddings = embedding_model.encode(chunks, convert_to_numpy = True)
    np.save(f"{topic}_embedding.npy", embeddings)

    return embeddings, chunks



def vector_database_create_chunks(topic: str , embeddings : np.array, chunks: list, distance_metric="cosine", steps=100, 
                                  maximum_no_neighbours = 16, size_of_candidate = 100, no_of_threads = None, candidate_list=100):


    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")


    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    collection = chroma_client.get_or_create_collection(
                        name = topic, embedding_function = embedding_function, 
                        metadata = {"hnsw:space": distance_metric, "hnsw:search_ef": candidate_list,
                        "hnsw:construction_ef": size_of_candidate, "hnsw:M": maximum_no_neighbours,
                        "hnsw:num_threads": no_of_threads if no_of_threads else multiprocessing.cpu_count(), 
                        "faiss:device": device()})

    for i, chunk in enumerate(chunks):
        collection.add(ids=[str(i)], documents = [chunk], embeddings = [embeddings[i].tolist()])

    return collection



def vector_database_get_chunks(topic : str):
    
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        collection = chroma_client.get_collection(topic)
    
    except Exception as e:
        return e

    return collection

