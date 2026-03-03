"""Scheduled task runner for continuous data ingestion"""
import os
import schedule
import time
from src.data_pipeline import DataPipeline
from src.logger import setup_logger

logger = setup_logger(__name__)


class FetchScheduler:
    """Manages scheduled RSS feed fetching"""
    
    def __init__(self):
        self.pipeline = DataPipeline()
        self.interval_minutes = int(os.getenv('FETCH_INTERVAL_MINUTES', '5'))
    
    def job(self):
        """Job function to run periodically"""
        try:
            self.pipeline.run()
        except Exception as e:
            logger.error(f"Scheduled job failed: {e}", exc_info=True)
    
    def start(self):
        """Start the scheduler"""
        logger.info(f"Starting scheduler with {self.interval_minutes} minute interval")
        
        # Schedule the job
        schedule.every(self.interval_minutes).minutes.do(self.job)
        
        # Run initial job immediately
        self.job()
        
        # Keep scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(10)  # Check every 10 seconds
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {e}", exc_info=True)
    
    def run_once(self):
        """Run the pipeline once without scheduling"""
        logger.info("Running pipeline once")
        self.pipeline.run()


if __name__ == '__main__':
    scheduler = FetchScheduler()
    scheduler.start()
