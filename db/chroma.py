import chromadb

from settings import CHROMA_DB_PATH, CHROMA_COLLECTION, SPLIT_BY
from transformer.split import split_by_character


def get_chroma_client():
    client = chromadb.PersistentClient(CHROMA_DB_PATH)
    return client

def get_collection():
    client = get_chroma_client()
    collection = client.get_or_create_collection(CHROMA_COLLECTION)
    return collection

def add_to_collection(documents, metadatas=None, ids=None):
    if ids is None:
        ids = []
    if metadatas is None:
        metadatas = []

    collection = get_collection()
    collection.add(documents=documents, metadatas=metadatas, ids=ids)

def query_collection(text, num_results=3):
    collection = get_collection()
    return collection.query(query_texts=text, n_results=num_results)


def peek():
    collection = get_collection()
    return collection.peek()

def load_chroma_db():
    """
    Loads all current documents into chromadb
    :return:
    """
    collection = get_collection()
    if SPLIT_BY == 'character':
        documents = split_by_character()
        collection.add(ids=[d.metadata['id'] for d in documents],
                       documents=[d.page_content for d in documents],
                       metadatas=[d.metadata for d in documents])

