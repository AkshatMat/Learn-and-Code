from bs4 import BeautifulSoup
from newspaper import Article, Config as NewsConfig
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import requests
from typing import Tuple, List
from config.settings import settings
from scrapers.base_scraper import BaseScraper

class NewspaperScraper(BaseScraper):
    @property
    def name(self) -> str:
        return "NewspaperScraper"

    def extract(self, url: str) -> Tuple[str, str, List[str]]:
        config = NewsConfig()
        config.browser_user_agent = settings.USER_AGENT
        config.request_timeout = settings.REQUEST_TIMEOUT

        article = Article(url, config=config)
        article.download()
        article.parse()
        article.nlp()
        return article.title, article.text, article.keywords