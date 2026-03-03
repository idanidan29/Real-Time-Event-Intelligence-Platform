# Real-Time News Sentiment Tracker

## Overview

The Real-Time News Sentiment Tracker is a full-stack project designed to ingest, process, and analyze news headlines and summaries from free RSS feeds and public news APIs in near real-time. It performs sentiment analysis on each news item and detects positive or negative spikes in sentiment per topic, displaying the results on a live dashboard.

This project demonstrates **real-time data ingestion, NLP-based sentiment analysis, anomaly detection, and dynamic visualization**, making it a portfolio-ready showcase.

---

## Architecture

The system is modular and consists of the following pipeline:

```
RSS/News APIs (BBC, Reuters, Hacker News, etc.)
             ↓
Fetch & Parsing Module (Python / feedparser)
             ↓
Raw Storage Database (PostgreSQL)
             ↓
Sentiment Analysis Pipeline (Python NLP / TextBlob / HuggingFace)
             ↓
Anomaly Detection Engine (Detect sentiment spikes per topic)
             ↓
Real-Time Dashboard (Next.js / React + Charts / WebSockets)
```

**Key Points:**

* **RSS/News APIs:** Provides continuously updating news headlines and summaries.
* **Fetch & Parsing Module:** Periodically polls feeds, extracts title, summary, timestamp, and source.
* **Raw Storage:** Stores original news items for reproducibility, auditing, and reprocessing.
* **Sentiment Analysis:** Calculates sentiment score for each news item.
* **Anomaly Detection:** Flags unusual spikes in positive or negative sentiment per topic.
* **Dashboard:** Displays live trends, sentiment scores, and detected anomalies.

---

## Data Sources

### RSS Feeds (Free)

* BBC World: [http://feeds.bbci.co.uk/news/world/rss.xml](http://feeds.bbci.co.uk/news/world/rss.xml)
* BBC Technology: [http://feeds.bbci.co.uk/news/technology/rss.xml](http://feeds.bbci.co.uk/news/technology/rss.xml)
* Reuters World News: [http://feeds.reuters.com/Reuters/worldNews](http://feeds.reuters.com/Reuters/worldNews)
* Hacker News Front Page: [https://hnrss.org/frontpage](https://hnrss.org/frontpage)
* TechCrunch: [http://feeds.feedburner.com/TechCrunch/](http://feeds.feedburner.com/TechCrunch/)
* The Verge: [https://www.theverge.com/rss/index.xml](https://www.theverge.com/rss/index.xml)

### Optional Free APIs

* NewsAPI.org (free tier, requires API key)
* Mediastack (free tier)
* GDELT Global Events Database (public news data)

---

## Database Schema

**1. news_items** – Stores raw news entries

| Column       | Type      | Description                 |
| ------------ | --------- | --------------------------- |
| id           | UUID      | Primary key                 |
| title        | TEXT      | Headline/title              |
| summary      | TEXT      | Summary or description      |
| source       | TEXT      | News source (BBC, HN, etc.) |
| url          | TEXT      | Link to original article    |
| published_at | TIMESTAMP | Timestamp of publication    |
| fetched_at   | TIMESTAMP | Timestamp when fetched      |

**2. sentiment_scores** – NLP sentiment results

| Column       | Type      | Description                     |
| ------------ | --------- | ------------------------------- |
| id           | UUID      | Primary key                     |
| news_id      | UUID      | References news_items(id)       |
| sentiment    | FLOAT     | Sentiment score (-1 to 1)       |
| confidence   | FLOAT     | NLP confidence score (optional) |
| processed_at | TIMESTAMP | Timestamp when analyzed         |

**3. anomalies** – Detected sentiment spikes

| Column      | Type      | Description                 |
| ----------- | --------- | --------------------------- |
| id          | UUID      | Primary key                 |
| topic       | TEXT      | Topic or feed name          |
| sentiment   | TEXT      | Positive / Negative spike   |
| severity    | FLOAT     | Magnitude of anomaly        |
| detected_at | TIMESTAMP | When anomaly was detected   |
| metadata    | JSONB     | Related items or extra info |

---

## Functionality

1. **Real-Time Fetching:** Continuously polls RSS feeds or APIs for the latest news.
2. **Raw Storage:** Persists all fetched news for reproducibility and auditability.
3. **Sentiment Analysis:** Scores each news headline/summary for sentiment.
4. **Anomaly Detection:** Detects sudden spikes in sentiment per topic.
5. **Live Dashboard:** Visualizes sentiment trends, volume, and anomalies in real time.

---

## How to Run

### 1. Set up Python environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2. Run PostgreSQL

```bash
docker-compose up -d
```

### 3. Start Fetch & Parsing Module

```bash
python fetch_news.py
```

### 4. Run Sentiment Analysis Pipeline

```bash
python sentiment_pipeline.py
```

### 5. Start Live Dashboard

```bash
cd frontend
npm install
npm run dev
```

---



This README gives a complete overview of the **Real-Time News Sentiment Tracker**, making it ready for a GitHub repo or portfolio. You can add diagrams or screenshots later to enhance clarity.
