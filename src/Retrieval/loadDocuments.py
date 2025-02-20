from .htmlretrieval import load_htmls_recursively
from .pdfretrieval import load_pdfs_recursively

def loadDocuments(folder_path):
    """
    Carica tutti i documenti da una cartella e dalle sue sottocartelle.

    :param folder_path: Percorso della cartella principale.
    :return: Lista di documenti caricati.
    """
    documents = load_htmls_recursively(folder_path)
    documents.extend(load_pdfs_recursively(folder_path))

    return documents