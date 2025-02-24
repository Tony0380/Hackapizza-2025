from src.Retrieval import search
import os
import getpass
from langchain.llms import LlamaCpp
from langchain.llms import OpenAI
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI


def gemini_llm():
    """
    Inizializza e restituisce un'istanza del modello Gemini per LangChain
    """
    # Importa la chiave API da variabile d'ambiente o file .env
    from dotenv import load_dotenv
    import os
    import getpass

    load_dotenv()

    if "GOOGLE_API_KEY" not in os.environ:
        api_key = getpass.getpass("Inserisci la tua Google API key: ")
        os.environ["GOOGLE_API_KEY"] = api_key

    # Inizializza l'API Gemini
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Crea l'istanza LangChain compatibile con Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    return llm

def local_llm():
    # Percorso del modello GGUF
    model_path = "../../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

    # Inizializza il modello
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.7,  # Controlla la creatività delle risposte
        max_tokens=512,  # Limita la lunghezza della risposta
        top_p=0.9,
        n_ctx=4096*2,  # Numero di token massimo nel contesto
        verbose=True  # Mostra dettagli nel log
    )
    return llm


def OpenAI_llm():
    # Carica variabili d'ambiente da .env file
    load_dotenv()

    # Verifica se la chiave API è disponibile
    if "OPENAI_API_KEY" not in os.environ:
        # Chiedi la chiave in modo sicuro senza mostrarla
        api_key = getpass.getpass("Inserisci la tua OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key

    # Crea l'istanza OpenAI
    llm = OpenAI()
    return llm

def rag_pipeline(folder_path, query, k=20):
    """
    Sistema RAG: Recupera i documenti rilevanti e genera una risposta con il LLM.

    Args:
    - folder_path (str): Percorso della cartella principale.
    - query (str): Query di ricerca.
    - k (int): Numero di documenti da recuperare.
    Returns:
    - str: La risposta generata dal LLM.
    """

    # Recupera i documenti più simili alla query
    docs = search(folder_path, query, k)

    # Unisci il testo dei documenti in un unico prompt
    context = "\n\n".join([doc.page_content for doc in docs])

    # Costruisci il prompt per il modello
    prompt = f"""
    Usa le seguenti informazioni per rispondere alla domanda in modo accurato:
    {context}

    Domanda: {query}
    Risposta:
    """

    llm = gemini_llm()

    # Genera la risposta con il modello
    print("🔹 Generazione della risposta in corso...")
    response = llm.invoke(prompt)
    return response
