from services.alternative_news_api_service import AlternativeNewsAPIService
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()  

def main():
    service = AlternativeNewsAPIService()
    try:
        articles = service.fetch_top_headlines(category="technology", page_size=3)
        for idx, article in enumerate(articles, 1):
            print(f"\nArticle {idx}:")
            print(f"Title: {article.title}")
            print(f"Source: {article.source}")
            print(f"URL: {article.url}")
            print(f"Author: {article.author}")
            print(f"Published At: {article.published_at}")
            print(f"Category: {article.category}")
    except Exception as e:
        logger.error(f"Error testing fallback API: {str(e)}")

if __name__ == "__main__":
    main()
