"""Database connection and models"""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class NewsItem(Base):
    """News Item Model"""
    __tablename__ = 'news_items'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title = Column(Text, nullable=False)
    summary = Column(Text)
    source = Column(String(255), nullable=False)
    url = Column(Text, unique=True, nullable=False)
    published_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<NewsItem(id={self.id}, source={self.source})>"


class SentimentScore(Base):
    """Sentiment Analysis Results"""
    __tablename__ = 'sentiment_scores'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    news_id = Column(String(36), nullable=False)
    sentiment = Column(Float)  # -1 to 1
    confidence = Column(Float)
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SentimentScore(news_id={self.news_id}, sentiment={self.sentiment})>"


class Anomaly(Base):
    """Anomaly Detection Results"""
    __tablename__ = 'anomalies'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    topic = Column(String(255), nullable=False)
    sentiment = Column(String(50))  # Positive/Negative
    severity = Column(Float)
    detected_at = Column(DateTime, default=datetime.utcnow)
    meta_info = Column(Text)  # JSON as text
    
    def __repr__(self):
        return f"<Anomaly(topic={self.topic}, sentiment={self.sentiment})>"


def get_db_engine():
    """Create database engine from environment variables"""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'news_sentiment_db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    
    # Wrap IPv6 addresses in brackets
    if ':' in db_host and not db_host.startswith('['):
        db_host = f'[{db_host}]'
    
    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    try:
        engine = create_engine(connection_string, echo=False)
        logger.info(f"Database engine created for {db_name}")
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise


def init_db():
    """Initialize database tables"""
    try:
        engine = get_db_engine()
        Base.metadata.create_all(engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_session():
    """Get database session"""
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()
