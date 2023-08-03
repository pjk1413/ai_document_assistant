from flask import Flask, request
from flask_cors import CORS
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate
from langchain.retrievers import SelfQueryRetriever
from langchain.schema import SystemMessage, Document
from langchain.vectorstores import Chroma

from db.chroma import get_db, peek

# from db.chroma import query_collection, get_chroma_client, get_collection, get_vectorstore, get_db

server = Flask(__name__)

CORS(server)

# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a chatbot that queries documents."),  # The persistent system prompt
#     MessagesPlaceholder(variable_name="chat_history"),  # Where the memory will be stored.
#     HumanMessagePromptTemplate.from_template("{human_input}"),  # Where the human input will injectd
# ])

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatOpenAI(model='gpt-3.5-turbo')

# chat_llm_chain = LLMChain(
#     llm=llm,
#     prompt=prompt,
#     verbose=True,
#     memory=memory,
# )


@server.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@server.route("/chat", methods=["GET", "POST"])
def chat():
    db = get_db()
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type="stuff",
                                           retriever=db.as_retriever(search_kwargs={"k": 1}),
                                           return_source_documents=True,
                                           verbose=True)
    llm_response = qa_chain(request.json['input'])
    print(llm_response)
    # print(llm_response['metadata'])
    return _parse_response(llm_response)


def _parse_response(res):
    # print(res.metadata)

    documents = res['source_documents']
    docs = []

    for doc in documents:

        docs.append({
            # "page_content": doc['page_content'],
            "source": doc.metadata['source'],
            "title": doc.metadata['title'],
        })
        # docs.append(doc.json())

    return {
        "response": res['result'],
        "sources": docs
        # "source_title": res['metadata']['title'],
        # "source": res['metadata']['source'],
    }