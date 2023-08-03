import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# FILE INGESTION
SOURCE_FILE_DIR = os.path.join(BASE_DIR, 'files')

# WEB SCRAPER
STARTING_URLS = ["https://confluence.educopia.org/display/BC/BitCurator+Environment"]
ALLOWED_DOMAINS = ["confluence.educopia.org"]
IGNORE_ROBOTSTXT = False
CRAWL_DEPTH_LIMIT = 5
# still under development
DOWNLOAD_FILES = True
# whitelist file extensions to download
DOWNLOAD_FILE_EXTENSIONS = ["pdf", "txt", "doc", "docx", "csv"]
# if true, will not store the html files in the files directory
#   the html files will be converted to json after scraping is finished
USE_PARSED_FILES = True

# TRANSFORMER SETTINGS
INCLUDE_METADATA = True
SPLIT_BY = "character"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOKEN_SIZE = 500

# CONFLUENCE LOADER SETTINGS
CONFLUENCE_URL = "https://confluence.educopia.org/"
CONFLUENCE_SPACES = ["BC", "MET"]
CONFLUENCE_TOKEN = "" # not yet implemented
CONFLUENCE_USERNAME = "" # not yet implemented
CONFLUENCE_PASSWORD = "" # not yet implemented

# DATABASE SETTINGS
#chroma
CHROMA_DB_PATH = os.path.join(BASE_DIR, "db", "chroma.db")
CHROMA_COLLECTION = "confluence"

#pinecone
USE_PINECONE = False


# EMBEDDINGS