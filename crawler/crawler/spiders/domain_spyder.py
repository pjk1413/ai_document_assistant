import os.path
from pathlib import Path

import scrapy
from scrapy.linkextractors import LinkExtractor

from settings import STARTING_URLS, ALLOWED_DOMAINS, USE_PARSED_FILES

# TODO pair with a loader
# https://python.langchain.com/docs/modules/data_connection/document_loaders/html
class DomainSpyder(scrapy.Spider):
    BASE_DIR = Path(__file__).resolve().parent.parent
    name = "domain_spyder"

    def start_requests(self):
        # check if html directory exists, create if not exists
        if not os.path.isdir(os.path.join(self.BASE_DIR, 'html')):
            os.mkdir(os.path.join(self.BASE_DIR, 'html'))

        # loop through the urls
        for url in STARTING_URLS:
            yield scrapy.Request(url=url, callback=self.parse, meta={'playwright': True})
    def _url_to_filename(self, url):
        return url.replace("http://", "").replace("https://", "").replace("/", "_")

    def parse(self, response):
        filename = self._url_to_filename(response.url) + '.html'
        path = os.path.join(self.BASE_DIR.parent.parent, "files", filename)

        if USE_PARSED_FILES:
            # store html files seperate from file ingestion directory
            path = os.path.join(self.BASE_DIR, 'html', filename)

        if 'display' in response.url or 'pages' in response.url:
            # loader = UnstructuredHTMLLoader("example_data/fake-content.html")
            with open(path, 'wb') as f:
            # ParseHTML(response.body)
                f.write(response.body)

                # soup = BeautifulSoup(response.body, "html.parser")
                # for link in soup.find_all("a"):
                #     if


        for a in LinkExtractor(allow_domains=ALLOWED_DOMAINS).extract_links(response):
            yield response.follow(a, callback=self.parse)


