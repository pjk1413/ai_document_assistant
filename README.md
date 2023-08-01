# Document Assistant
The purpose of this project is to be a POC for scraping a large collection of docs/files/websites and then chatting with those documents to determine relevant information

## Get Started
Begin by setting up your python virtual environment. [PyDocs](https://docs.python.org/3/library/venv.html)

*Ensure your virtual environment is activated prior to installing the requirements.*

- if ```files``` directory does not exist, add it in the base directory
- cd into the root directory of this project ('document_assistant')
- run ```pip install -r requirements.txt``` to install requirements to run
- in ```settings.py``` review the necessary variables and adjust as needed
  - *as of 08/01/2023* - the ```CONFLUENCE, TRANSFORMER, DATABASE, FILE_INGRESTION``` are the only settings needed
    - **CONFLUENCE** - the ```URL``` and ```SPACES``` are the only needed fields unless the docs are password protected
      - [Confluence Ingregration Docs](https://python.langchain.com/docs/integrations/document_loaders/confluence)
- in the root directory, run ```python app.py -l confluence``` to load data in from the designated Confluence source
  - this will load the data into the *files* directory
  - Does not currently support attachments, *issue with tesseract on mac*
- after verifying files have been loaded in, run ```python app.py -chroma load``` to load files into **chromaDB**
  - This will prompt you and verify that you want to do this, simply enter ```y```
  - This will download default embedding model (around 70mb) on the first run
  - Database will be persisted at file location noted in ```settings.py```
- To verify everything has loaded correctly, run ```python app.py -chroma query``` to run a test query
  - This will prompt for text
  - Verify data has been returned

    
## Docs

### Crawler
- The purpose of the crawler is to take any set of starting urls as well as allowed domains and scrape those websites to be placed into the database
  - Currently under development
  - Uses ```scrapy``` to handle link requests and general navigation
  - Will utilize ```langchain``` to scrape data and store in database

### Loader
- Confluence loader is used for loading confluence docs
- HTML loader will be paired with crawler to load pages
  - Need to enable attachments in both areas

### Network Analysis
- Noted as a possible future avenue
- library to look into: ```networkx```

### Document Ingestion
- Noted as a future need, very simple to accomplish through langchain
