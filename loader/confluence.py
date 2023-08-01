import json
import os.path
from pathlib import Path

from langchain.document_loaders import ConfluenceLoader

from settings import CONFLUENCE_URL, CONFLUENCE_SPACES

BASE_DIR = Path(__file__).resolve().parent.parent

# TODO add support for attachments, error with tesseract

def load_confluence():
    loader = ConfluenceLoader(
        url=CONFLUENCE_URL
    )

    for space in CONFLUENCE_SPACES:
        documents = loader.load(space_key=space, limit=100)

        with open(os.path.join(BASE_DIR, "files", f"confluence_{space}.json"), "w") as w:
            w.write(json.dumps([d.dict() for d in documents]))