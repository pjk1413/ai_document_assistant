import json
import os
from pathlib import Path

from settings import INCLUDE_METADATA, CHUNK_SIZE, CHUNK_OVERLAP, TOKEN_SIZE
from langchain.text_splitter import CharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent.parent

def split_by_character():
    """
    Splits data by character and returns a list of documents
    :return:
    """
    for file in os.listdir(os.path.join(BASE_DIR, "files")):
        with open(os.path.join(BASE_DIR, "files", file), "r") as r:
            data = json.loads(r.read())

            text_splitter = CharacterTextSplitter(
                separator="\n\n",
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                length_function=len,
            )

            if INCLUDE_METADATA:
                print(data[0])
                texts = text_splitter.create_documents(
                    [d['page_content'] for d in data], [d['metadata'] for d in data])
            else:
                texts = text_splitter.create_documents([d['page_content'] for d in data])

            return texts


def split_by_token():
    """
    Splits data by token, returns a list of documents
    :return:
    """
    for file in os.listdir(os.path.join(BASE_DIR, "files")):
        with open(os.path.join(BASE_DIR, "files", file), "r") as r:
            data = json.loads(r.read())

            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=TOKEN_SIZE, chunk_overlap=0
            )

            text = ""
            text += [d['page_content'] for d in data]

            texts = text_splitter.split_text(text)

            return texts