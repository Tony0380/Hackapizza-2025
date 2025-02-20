import os
from langchain.document_loaders import PyMuPDFLoader

def load_pdfs_recursively(folder_path):
    """
    Carica ricorsivamente tutti i file PDF da una cartella e dalle sue sottocartelle.

    :param folder_path: Percorso della cartella principale.
    :return: Lista di documenti caricati.
    """
    documents = []

    # Scansiona la cartella e sottocartelle
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".pdf"):
                file_path = os.path.join(root, filename)
                print(f"📄 Caricando: {file_path}")

                try:
                # Carica il PDF
                    loader = PyMuPDFLoader(file_path)
                    documents.extend(loader.load())  # Aggiunge i documenti alla lista
                except Exception as e:
                    print(f"⚠️ Errore con {file_path}: {e}")

    return documents
