"""Utility scripts for development and testing"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text
from src.logger import setup_logger
from src.database import get_session, init_db, NewsItem

logger = setup_logger(__name__)
load_dotenv()


def test_database_connection():
    """Test database connection"""
    logger.info("Testing database connection...")
    try:
        session = get_session()
        session.execute(text("SELECT 1"))
        session.close()
        logger.info("[OK] Database connection successful")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Database connection failed: {e}")
        return False


def reset_database():
    """Reset database tables (for development only)"""
    logger.warning("Resetting database...")
    try:
        from src.database import Base, get_db_engine
        engine = get_db_engine()
        
        # Drop all tables
        Base.metadata.drop_all(engine)
        logger.info("Dropped all tables")
        
        # Recreate tables
        init_db()
        logger.info("[OK] Database reset complete")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Database reset failed: {e}")
        return False


def show_stored_items():
    """Display all stored news items"""
    logger.info("Fetching stored news items...")
    try:
        session = get_session()
        items = session.query(NewsItem).order_by(NewsItem.fetched_at.desc()).limit(10).all()
        session.close()
        
        if not items:
            logger.info("No items found in database")
            return
        
        logger.info(f"Latest {len(items)} items:")
        for i, item in enumerate(items, 1):
            logger.info(f"{i}. [{item.source}] {item.title[:60]}")
            logger.info(f"   URL: {item.url}")
            logger.info(f"   Published: {item.published_at}")
            logger.info("")
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch items: {e}")


def count_items():
    """Count total items in database"""
    try:
        session = get_session()
        count = session.query(NewsItem).count()
        session.close()
        logger.info(f"Total items in database: {count}")
        return count
    except Exception as e:
        logger.error(f"✗ Failed to count items: {e}")
        return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m src.utils <command>")
        print("Commands:")
        print("  test-db        - Test database connection")
        print("  reset-db       - Reset database (for development)")
        print("  show-items     - Show latest stored items")
        print("  count-items    - Count total items")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'test-db':
        test_database_connection()
    elif command == 'reset-db':
        reset_database()
    elif command == 'show-items':
        show_stored_items()
    elif command == 'count-items':
        count_items()
    else:
        logger.error(f"Unknown command: {command}")
        sys.exit(1)
