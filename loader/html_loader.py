from pathlib import Path

# TODO pair this with a crawler to make it better
# https://python.langchain.com/docs/modules/data_connection/document_loaders/html
from langchain.document_loaders import UnstructuredHTMLLoader

BASE_DIR = Path(__file__).resolve().parent.parent

def load_unstructured_html():
    pass


loader = UnstructuredHTMLLoader("example_data/fake-content.html")