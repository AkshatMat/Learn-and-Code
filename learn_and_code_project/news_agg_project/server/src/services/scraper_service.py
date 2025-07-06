import time
from typing import List, Tuple, Optional
from scrapers.base_scraper import BaseScraper
from scrapers.bs4_scraper import BS4Scraper
from scrapers.newspaper_scraper import NewspaperScraper
from scrapers.selenium_scraper import SeleniumScraper
from utils.exception import ScrapingError
from utils.logger import logger

class ScraperService:    
    def __init__(self, scrapers: Optional[List[BaseScraper]] = None):
        if scrapers is None:
            self.scrapers = [
                BS4Scraper(),
                NewspaperScraper(),
                SeleniumScraper()
            ]
        else:
            self.scrapers = scrapers
    
    def extract_article(self, url: str) -> Tuple[str, str, List[str]]:
        for scraper in self.scrapers:
            try:
                logger.info(f"Attempting to scrape {url} with {scraper.name}")
                result = scraper.extract(url)
                
                if result and result[0] and result[1]: 
                    logger.info(f"Successfully scraped {url} with {scraper.name}")
                    return result
                    
            except Exception as e:
                logger.warning(f"{scraper.name} failed for {url}: {str(e)}")
                continue
        
        raise ScrapingError(f"All scraping strategies failed for URL: {url}")
    
    def add_scraper(self, scraper: BaseScraper) -> None:
        self.scrapers.append(scraper)
    
    def remove_scraper(self, scraper_name: str) -> None:
        self.scrapers = [s for s in self.scrapers if s.name != scraper_name]