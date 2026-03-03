"""Database setup script"""
import os
from dotenv import load_dotenv
from src.database import init_db
from src.logger import setup_logger

logger = setup_logger(__name__)

if __name__ == '__main__':
    load_dotenv()
    logger.info("Setting up database...")
    
    try:
        init_db()
        logger.info("✓ Database setup complete!")
        logger.info("You can now run: python main.py")
    except Exception as e:
        logger.error(f"✗ Database setup failed: {e}")
        exit(1)
