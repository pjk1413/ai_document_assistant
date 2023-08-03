import chromadb
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from settings import CHROMA_DB_PATH, CHROMA_COLLECTION, SPLIT_BY
from transformer.split import split_by_character


def reset():
    get_db().delete_collection()

def get_db():
    emb_model = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=emb_model)

    documents = split_by_character()
    # collection.add(ids=[d.metadata['id'] for d in documents],
    #                documents=[d.page_content for d in documents],
    #                metadatas=[d.metadata for d in documents])
    vectordb = Chroma.from_documents(
        persist_directory=CHROMA_DB_PATH,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION,
        # metadatas=[d.metadata for d in documents],
        # collection_metadata=[d.metadata for d in documents],
        ids=[d.metadata['id'] for d in documents],
        documents=documents)

    # vectordb = Chroma(persist_directory=CHROMA_DB_PATH,
    #                   embedding_function=embeddings)
    vectordb.persist()
    # print(vectordb.search('BitCurator', 'similarity'))
    return vectordb


def get_chroma_client():
    client = chromadb.PersistentClient(CHROMA_DB_PATH)

    return client

def get_collection():
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    client = get_chroma_client()
    collection = client.get_or_create_collection(CHROMA_COLLECTION, embedding_function=embed_func)
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

