"""Main entry point for the backend application"""
import os
import sys
from dotenv import load_dotenv
from src.logger import setup_logger
from src.database import init_db
from src.scheduler import FetchScheduler

logger = setup_logger(__name__)


def main():
    """Initialize and start the application"""
    # Load environment variables
    load_dotenv()
    
    logger.info("=" * 60)
    logger.info("Real-Time News Sentiment Tracker - Backend")
    logger.info("=" * 60)
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully")
        
        # Start the scheduler
        logger.info("Starting data ingestion scheduler...")
        scheduler = FetchScheduler()
        scheduler.start()
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
