import argparse

from db.chroma import load_chroma_db, query_collection, reset
from loader.confluence import load_confluence
from server.server import server

parser = argparse.ArgumentParser(description="Command line arguments for the doc assist")

# TODO build out crawler to utilize langchain
# parser.add_argument("-c", "--Crawl", help="Run crawler", action='store_true')
parser.add_argument("-l", "--Load", help="Loads data from a designated source, requires argument")
parser.add_argument("-chroma", "--Chroma", help="Performs a given action with chroma ['load', 'query']")
parser.add_argument("-serve", "--Serve", action='store_true')

args = parser.parse_args()

if args.Load:
    load_from = args.Load

    # TODO add additional sources

    if load_from == 'confluence':
        load_confluence()

if args.Chroma:
    if args.Chroma == 'load':
        answer = input("Preparing to load all current files into ChromaDB, confirm (y/n): ")

        if answer.lower() == 'y':
            load_chroma_db()

    if args.Chroma == 'query':
        answer = input("Query text: ")
        result = query_collection(answer.lower())
        print(result.values())

    if args.Chroma == 'reset':
        reset()

if args.Serve:
    server.run(host="0.0.0.0", port=1904)