import argparse
import os
import subprocess

import scrapy.utils.reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# from crawler.confluence.to_json import run
from crawler.crawler.spiders.domain_spyder import DomainSpyder
from db.chroma import load_chroma_db, query_collection
from loader.confluence import load_confluence

parser = argparse.ArgumentParser(description="Command line arguments for the doc assist")

# TODO build out crawler to utilize langchain
# parser.add_argument("-c", "--Crawl", help="Run crawler", action='store_true')
parser.add_argument("-l", "--Load", help="Loads data from a designated source, requires argument")
parser.add_argument("-chroma", "--Chroma", help="Performs a given action with chroma ['load', 'query']")

args = parser.parse_args()

# if args.Crawl:
#     settings = get_project_settings()
#     process = CrawlerProcess(settings)
#     process.crawl(DomainSpyder)
#     process.start()
#     process.join()

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
