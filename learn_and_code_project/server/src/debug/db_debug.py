from repositories.database_repository import DatabaseRepository
from utils.logger import logger
from dotenv import load_dotenv

load_dotenv()  

def main():
    db = DatabaseRepository()
    try:
        dict = db.get_fallbackapi_entry()
        print(dict)
    except Exception as e:
        logger.error(f"Error testing db: {str(e)}")

if __name__ == "__main__":
    main()