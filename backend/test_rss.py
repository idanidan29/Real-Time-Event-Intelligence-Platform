"""Quick test of RSS fetching without database"""
import os
from dotenv import load_dotenv
from src.rss_fetcher import RSSFetcher
from src.logger import setup_logger

logger = setup_logger(__name__)

if __name__ == '__main__':
    load_dotenv()
    logger.info("Testing RSS feed fetching (without database storage)...")
    
    try:
        fetcher = RSSFetcher()
        items = fetcher.fetch_all()
        
        logger.info(f"\nFetched {len(items)} total items\n")
        
        # Show first 5 items
        for i, item in enumerate(items[:5], 1):
            logger.info(f"{i}. [{item['source']}] {item['title']}")
            logger.info(f"   Summary: {item['summary'][:100]}...")
            logger.info(f"   URL: {item['url']}")
            logger.info("")
        
        logger.info("✓ RSS fetch test successful!")
        
    except Exception as e:
        logger.error(f"✗ Test failed: {e}", exc_info=True)
