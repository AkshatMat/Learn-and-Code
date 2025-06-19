from bs4 import BeautifulSoup
import requests
from typing import Tuple, List
from config.settings import settings
from scrapers.base_scraper import BaseScraper 

class BS4Scraper(BaseScraper):
    @property
    def name(self) -> str:
        return "BS4Scraper"

    def extract(self, url: str) -> Tuple[str, str, List[str]]:
        headers = {"User-Agent": settings.USER_AGENT}
        response = requests.get(url, headers=headers, timeout=settings.REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        paragraphs = soup.find_all("p")
        content = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        return title, content, []