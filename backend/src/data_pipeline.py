"""Data ingestion and storage pipeline"""
from sqlalchemy.exc import IntegrityError
from src.rss_fetcher import RSSFetcher
from src.database import get_session, NewsItem
from src.logger import setup_logger

logger = setup_logger(__name__)


class DataPipeline:
    """Handles fetching and storing news data"""
    
    def __init__(self):
        self.fetcher = RSSFetcher()
    
    def run(self):
        """
        Execute the data ingestion pipeline:
        1. Fetch data from all sources
        2. Store in database
        3. Log results
        """
        logger.info("=" * 60)
        logger.info("Starting data ingestion pipeline")
        logger.info("=" * 60)
        
        try:
            # Fetch data
            items = self.fetcher.fetch_all()
            logger.info(f"Fetched {len(items)} items from RSS feeds")
            
            if not items:
                logger.warning("No items fetched from any source")
                return 0
            
            # Store data
            stored_count = self.store_items(items)
            
            logger.info("=" * 60)
            logger.info(f"Pipeline completed: {stored_count}/{len(items)} items stored")
            logger.info("=" * 60)
            
            return stored_count
            
        except Exception as e:
            logger.error(f"Pipeline failed with error: {e}", exc_info=True)
            return 0
    
    def store_items(self, items: list) -> int:
        """
        Store fetched items in the database
        
        Args:
            items: List of news item dictionaries
            
        Returns:
            Number of items successfully stored
        """
        session = get_session()
        stored_count = 0
        
        try:
            for item_data in items:
                try:
                    # Check if item already exists (by URL)
                    existing = session.query(NewsItem).filter(
                        NewsItem.url == item_data['url']
                    ).first()
                    
                    if existing:
                        logger.debug(f"Item already exists: {item_data['url']}")
                        continue
                    
                    # Create new item
                    news_item = NewsItem(
                        title=item_data['title'],
                        summary=item_data['summary'],
                        source=item_data['source'],
                        url=item_data['url'],
                        published_at=item_data['published_at'],
                        fetched_at=item_data['fetched_at']
                    )
                    
                    session.add(news_item)
                    stored_count += 1
                    logger.debug(f"Added: {item_data['source']} - {item_data['title'][:50]}")
                    
                except IntegrityError as e:
                    session.rollback()
                    logger.debug(f"Duplicate or constraint violation: {e}")
                except Exception as e:
                    session.rollback()
                    logger.error(f"Error storing item: {e}")
            
            # Commit all changes
            session.commit()
            logger.info(f"Successfully stored {stored_count} new items to database")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error during batch storage: {e}")
        finally:
            session.close()
        
        return stored_count
