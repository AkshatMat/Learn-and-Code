'''This is a test runner file, just didn't want to run schedular again and again,
   So, for developement purpose, using this. 
   Schedular also has a run_once() function.'''

import sys
import os
from pathlib import Path
from services.aggregator_service import AggregatorService
from utils.logger import logger
from utils.exception import NewsAggregatorException

src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

def main():
    try:
        logger.info("Starting News Aggregator Application")
        
        aggregator = AggregatorService()
        results = aggregator.aggregate_news()
        
        summary = aggregator.get_aggregation_summary(results)
        logger.info(f"\n{summary}")
        
        logger.info("News Aggregator completed successfully")
        
    except NewsAggregatorException as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        try:
            if 'aggregator' in locals():
                aggregator.cleanup_resources()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    main()