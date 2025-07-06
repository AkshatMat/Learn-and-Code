import schedule
import time
import os
import shutil
from datetime import datetime
from typing import Optional, Callable
from services.aggregator_service import AggregatorService
from repositories.file_repository import FileRepository
from utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)

class NewsScheduler:
    def __init__(self, interval_hours: int = 4):
        self.interval_hours = interval_hours
        self.aggregator_service = AggregatorService()
        self.file_repository = FileRepository()
        self.is_running = False
        self.last_run_time: Optional[datetime] = None
        self.success_count = 0
        self.error_count = 0
        
    def clear_output_directory(self) -> bool:
        try:
            if os.path.exists(settings.OUTPUT_DIR):
                for filename in os.listdir(settings.OUTPUT_DIR):
                    file_path = os.path.join(settings.OUTPUT_DIR, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        logger.error(f"\n Error deleting {file_path}: {str(e)}")
                        return False
                
                logger.info(f"\n Cleared output directory: {settings.OUTPUT_DIR}")
            else:
                logger.info(f"Output directory {settings.OUTPUT_DIR} doesn't exist, creating it...")
                os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing output directory: {str(e)}")
            return False
    
    def run_news_aggregation(self) -> bool:
        try:
            logger.info("\n Starting scheduled news aggregation...")
            start_time = datetime.now()
            
            if not self.clear_output_directory():
                logger.error("Failed to clear output directory, continuing anyway...")
            
            results = self.aggregator_service.aggregate_news()
            
            if results["success"]:
                summary = self.aggregator_service.get_aggregation_summary(results)
                logger.info(f"Aggregation completed successfully:\n{summary}")
                self.success_count += 1
            else:
                logger.warning("Aggregation completed with no articles processed")
                self.error_count += 1
            
            end_time = datetime.now()
            duration = end_time - start_time
            self.last_run_time = end_time
            
            logger.info(f"News aggregation completed in {duration}")
            
            return results["success"]
            
        except Exception as e:
            logger.error(f"Error during news aggregation: {str(e)}")
            self.error_count += 1
            return False
    
    def start_scheduler(self, run_immediately: bool = True) -> None:
        logger.info("Starting News Aggregation Scheduler")
        logger.info(f"News will be fetched every {self.interval_hours} hours")
        
        schedule.every(self.interval_hours).hours.do(self.run_news_aggregation)
        
        self.is_running = True
        
        if run_immediately:
            logger.info("Running initial news aggregation...")
            self.run_news_aggregation()
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60) 
                
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                self.stop_scheduler()
                break
                
            except Exception as e:
                logger.error(f"Unexpected error in scheduler loop: {str(e)}")
                time.sleep(60)
    
    def stop_scheduler(self) -> None:
        logger.info("Stopping News Aggregation Scheduler...")
        self.is_running = False
        
        schedule.clear()
        
        try:
            self.aggregator_service.cleanup_resources()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
        
        logger.info("Scheduler stopped successfully")
    
    def get_scheduler_status(self) -> dict:
        next_run = None
        if schedule.jobs:
            next_run = schedule.next_run()
        
        return {
            "is_running": self.is_running,
            "interval_hours": self.interval_hours,
            "last_run_time": self.last_run_time,
            "next_run_time": next_run,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "total_runs": self.success_count + self.error_count
        }
    
    def run_once(self) -> bool:
        logger.info("Running news aggregation once...")
        return self.run_news_aggregation()
    
    def schedule_custom_job(self, job_func: Callable, interval_hours: int) -> None:
        schedule.every(interval_hours).hours.do(job_func)
        logger.info(f"Custom job scheduled to run every {interval_hours} hours")
    
    def get_next_run_info(self) -> Optional[str]:
        if not schedule.jobs:
            return None
        
        next_run = schedule.next_run()
        now = datetime.now()
        time_until_next = next_run - now
        
        hours, remainder = divmod(time_until_next.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        
        return f"Next run in {int(hours)} hours and {int(minutes)} minutes ({next_run.strftime('%Y-%m-%d %H:%M:%S')})"


def main():
    scheduler = NewsScheduler()
    
    try:
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {str(e)}")
        raise
    finally:
        scheduler.stop_scheduler()


if __name__ == "__main__":
    main()