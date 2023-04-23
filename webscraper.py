import aiohttp
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, query, search_engine):
        self.query = query
        self.search_engine = search_engine.lower()
        self.url, self.headers = self.build_url_and_headers()

    def build_url_and_headers(self):
        if self.search_engine == "google":
            url = f"https://www.google.com/search?q={self.query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
            }
        elif self.search_engine == "bing":
            url = f"https://www.bing.com/search?q={self.query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
            }
        elif self.search_engine == "yahoo":
            url = f"https://search.yahoo.com/search?p={self.query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
            }
        elif self.search_engine == "yandex":
            url = f"https://yandex.com/search/?text={self.query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
            }
        else:
            raise ValueError(f"Unsupported search engine: {self.search_engine}")

        return url, headers

    async def get_results(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    response.raise_for_status()
                    text = await response.text()

        except aiohttp.ClientError as e:
            return {"error": f"Error in making the request: {e}"}

        try:
            soup = BeautifulSoup(text, "html.parser")
            elements = self.extract_search_results(soup)

            results = []
            for i in range(min(10, len(elements))):
                link = self.extract_link(elements[i])
                results.append(link)

            return results
        except Exception as e:
            return {"error": f"Error processing the page: {e}"}

    def extract_search_results(self, soup):
        if self.search_engine == "google":
            return soup.find_all("div", class_="tF2Cxc")
        elif self.search_engine == "bing":
            return soup.find_all("li", class_="b_algo")
        elif self.search_engine == "yahoo":
            return soup.find_all("div", class_="Sr")
        elif self.search_engine == "yandex":
            return soup.find_all("div", class_="organic typo typo_text_m typo_line_s")

    def extract_link(self, element):
        if self.search_engine == "google":
            return element.find("a")["href"]
        elif self.search_engine == "bing":
            return element.find("a")["href"]
        elif self.search_engine == "yahoo":
            return element.find("a")["href"]
        elif self.search_engine == "yandex":
            return element.find("a", class_="link link_theme_normal")["href"]
