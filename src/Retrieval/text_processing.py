from .loadDocuments import loadDocuments
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def chunking(folder_path):
    """
    Esegue il chunking di documenti.
    :param folder_path: Percorso della cartella principale.
    :return: Lista di chunk.
    """
    documents = loadDocuments(folder_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=16384*2, chunk_overlap=500*2)
    chunks = text_splitter.split_documents(documents)
    return chunks

def indexing(chunks, embedding_model):
    """
    Esegue l'indicizzamento di chunk in un vettore store.
    :param chunks: Lista di chunk.
    :param embedding_model: Modello di embedding.
    :return: Vettore store.
    """
    vectorstore = FAISS.from_texts(
        texts=[chunk.page_content for chunk in chunks],
        embedding=embedding_model
    )
    return vectorstore

def indexing_pipeline(folder_path):
    """
    Esegue il chunking, l'embedding e l'indicizzamento di documenti.
    :param folder_path: Percorso della cartella principale.
    :return: Vettore store.
    """
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    chunks = chunking(folder_path)
    vectorstore = indexing(chunks, embedding_model)
    return vectorstore

def search(folder_path, query, k=20):
    """
    Esegue una ricerca di similarità.

    :param folder_path: Percorso della cartella principale.
    :param query: Query di ricerca.
    :param k: Numero di risultati da restituire.
    """

    vectorstore = indexing_pipeline(folder_path)
    results = vectorstore.similarity_search(query, k=k)
    return results