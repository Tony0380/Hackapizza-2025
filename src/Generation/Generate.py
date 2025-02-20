from src.Retrieval import search

from langchain.llms import LlamaCpp

def rag_pipeline(folder_path, query, k=20):
    """
    Sistema RAG: Recupera i documenti rilevanti e genera una risposta con il LLM.



    Returns:
    - str: La risposta generata dal LLM.
    """
    # Percorso del modello GGUF
    model_path = "../../models/mistral-7b-instruct-v0.2.Q3_K_M.gguf"

    # Inizializza il modello
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.7,  # Controlla la creatività delle risposte
        max_tokens=1024,  # Limita la lunghezza della risposta
        top_p=0.9,
        n_ctx=2048*2,  # Numero di token massimo nel contesto
        verbose=True  # Mostra dettagli nel log
    )
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

    # Genera la risposta con il modello
    print("🔹 Generazione della risposta in corso...")
    response = llm.invoke(prompt)
    return response

pquery = "Quali sono i piatti che includono le Chocobo Wings come ingrediente?"

response = rag_pipeline("../../HackapizzaDataset", pquery)

print("🔹 RISPOSTA:")
print(response)