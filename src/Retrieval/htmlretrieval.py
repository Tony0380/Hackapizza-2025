import os
from langchain.document_loaders import BSHTMLLoader

def load_htmls_recursively(folder_path):
    """
    Carica ricorsivamente tutti i file HTML da una cartella e dalle sue sottocartelle.

    :param folder_path: Percorso della cartella principale.
    :return: Lista di documenti caricati.
    """
    documents = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith((".html", ".htm")):
                file_path = os.path.join(root, filename)
                print(f"🌍 Caricando: {file_path}")

                try:
                    # Forza l'uso di html.parser se lxml non funziona
                    loader = BSHTMLLoader(file_path, bs_kwargs={"features": "html.parser"})
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"⚠️ Errore con {file_path}: {e}")
    return documents