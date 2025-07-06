from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import requests
from typing import Tuple, List
from config.settings import settings
from scrapers.base_scraper import BaseScraper 

class SeleniumScraper(BaseScraper):
    @property
    def name(self) -> str:
        return "SeleniumScraper"

    def extract(self, url: str) -> Tuple[str, str, List[str]]:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument(f"user-agent={settings.USER_AGENT}")

        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()
        except WebDriverException as e:
            raise RuntimeError(f"Selenium WebDriver error: {e}")

        title = soup.title.string.strip() if soup.title else "No title"
        paragraphs = soup.find_all("p")
        content = "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        return title, content, []