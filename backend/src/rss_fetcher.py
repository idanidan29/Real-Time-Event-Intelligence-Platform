"""RSS Feed Fetcher Module"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse
from src.logger import setup_logger

logger = setup_logger(__name__)


class RSSFetcher:
    """Fetches and parses RSS feeds"""
    
    # List of free RSS feeds
    RSS_FEEDS = {
        'BBC World': 'http://feeds.bbci.co.uk/news/world/rss.xml',
        'BBC Technology': 'http://feeds.bbci.co.uk/news/technology/rss.xml',
        'Reuters World': 'http://feeds.reuters.com/Reuters/worldNews',
        'Hacker News': 'https://hnrss.org/frontpage',
        'TechCrunch': 'http://feeds.feedburner.com/TechCrunch/',
        'The Verge': 'https://www.theverge.com/rss/index.xml',
    }
    
    def __init__(self):
        self.timeout = 10
    
    def fetch_feed(self, feed_url: str, source_name: str) -> List[Dict]:
        """
        Fetch and parse a single RSS feed
        
        Args:
            feed_url: URL of the RSS feed
            source_name: Name/identifier of the source
            
        Returns:
            List of parsed news items
        """
        items = []
        try:
            logger.info(f"Fetching feed from {source_name}: {feed_url}")
            
            # Fetch the feed with timeout
            response = requests.get(feed_url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse the feed
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                logger.warning(f"Feed parsing warning for {source_name}: {feed.bozo_exception}")
            
            # Extract entries
            for entry in feed.entries[:10]:  # Limit to latest 10 items
                try:
                    item = self._parse_entry(entry, source_name)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Error parsing entry from {source_name}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(items)} items from {source_name}")
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch feed from {source_name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error fetching {source_name}: {e}")
        
        return items
    
    def _parse_entry(self, entry, source_name: str) -> Optional[Dict]:
        """
        Parse a single RSS entry
        
        Args:
            entry: feedparser entry object
            source_name: Name of the source
            
        Returns:
            Dictionary with news item data or None if invalid
        """
        try:
            title = entry.get('title', '').strip()
            summary = entry.get('summary', entry.get('description', '')).strip()
            url = entry.get('link', '').strip()
            
            # Validate required fields
            if not title or not url:
                return None
            
            # Parse published date
            published_at = self._parse_date(entry)
            if not published_at:
                published_at = datetime.utcnow()
            
            return {
                'title': title,
                'summary': summary,
                'source': source_name,
                'url': url,
                'published_at': published_at,
                'fetched_at': datetime.utcnow()
            }
            
        except Exception as e:
            logger.warning(f"Error parsing entry: {e}")
            return None
    
    @staticmethod
    def _parse_date(entry) -> Optional[datetime]:
        """Parse published date from RSS entry"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                from time import struct_time
                if isinstance(entry.published_parsed, struct_time):
                    return datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                from time import struct_time
                if isinstance(entry.updated_parsed, struct_time):
                    return datetime(*entry.updated_parsed[:6])
        except Exception:
            pass
        return None
    
    def fetch_all(self) -> List[Dict]:
        """
        Fetch all configured RSS feeds
        
        Returns:
            List of all parsed news items
        """
        all_items = []
        
        for source_name, feed_url in self.RSS_FEEDS.items():
            items = self.fetch_feed(feed_url, source_name)
            all_items.extend(items)
        
        logger.info(f"Total items fetched: {len(all_items)}")
        return all_items
