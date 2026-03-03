# Real-Time Social Sentiment & Event Intelligence Platform

## Overview

This project is a production-oriented full-stack intelligence system designed to ingest, process, and store social media posts in real time. The goal of Phase One is to establish a solid foundation: a backend API, database schema, and a synthetic post generator to simulate real-time social media streams.

This foundation sets the stage for future phases including NLP-based sentiment analysis, anomaly detection, LLM-powered event intelligence, and a real-time dashboard.

---

## Architecture

The system is designed as a modular, vertically integrated pipeline:

```
Synthetic Stream Generator
        ↓
FastAPI Backend (Ingestion API)
        ↓
PostgreSQL Database (Raw Storage)
        ↓
Processing Workers (Future: NLP Pipeline)
        ↓
Sentiment Scores Table (Future)
        ↓
Anomaly Detection Engine (Future)
        ↓
WebSocket Broadcaster → Real-Time Dashboard (Future)
```

**Key Notes:**

* **Synthetic Generator:** Produces posts with random users, platforms, text, and timestamps. Supports controlled spikes for anomaly testing.
* **FastAPI Backend:** Provides a REST API to receive posts and store them in the database.
* **Database:** PostgreSQL stores all raw posts with a schema designed to scale for future NLP and anomaly detection layers.
* **Modular Design:** Each layer can be replaced or extended without impacting others. For example, NLP workers will later consume the raw posts table.

---

## Database Schema

**1. posts** – Stores all raw social media posts

| Column     | Type      | Description                             |
| ---------- | --------- | --------------------------------------- |
| id         | UUID      | Primary key                             |
| platform   | TEXT      | Source platform (e.g., Twitter, Reddit) |
| user_id    | TEXT      | Unique user identifier                  |
| text       | TEXT      | Post content                            |
| created_at | TIMESTAMP | Post timestamp                          |
| language   | TEXT      | Language code                           |

**2. sentiment_scores** – Placeholder for future NLP outputs

| Column          | Type      | Description                     |
| --------------- | --------- | ------------------------------- |
| id              | UUID      | Primary key                     |
| post_id         | UUID      | References posts(id)            |
| sentiment_score | FLOAT     | Sentiment value (-1 to 1)       |
| confidence      | FLOAT     | Confidence score from NLP model |
| processed_at    | TIMESTAMP | Processing timestamp            |

**3. anomalies** – Placeholder for future event detection

| Column      | Type      | Description                       |
| ----------- | --------- | --------------------------------- |
| id          | UUID      | Primary key                       |
| type        | TEXT      | Anomaly type                      |
| topic       | TEXT      | Related topic                     |
| severity    | FLOAT     | Severity score                    |
| confidence  | FLOAT     | Confidence of detection           |
| detected_at | TIMESTAMP | Detection timestamp               |
| metadata    | JSONB     | Extra info (related posts, users) |

---

## Part One – Functionality

Currently implemented:

1. **Synthetic Post Generator:** Generates a configurable stream of posts to simulate live social media activity.
2. **Backend API:** FastAPI endpoint `/posts` receives JSON posts and stores them in PostgreSQL.
3. **Database Storage:** Raw posts are persisted with indexes on timestamp and platform for efficient future queries.
4. **Logging & Monitoring:** Basic logs track ingestion status and throughput.

---

## Future Phases

* **Phase 2 – NLP Pipeline:** Process posts to generate sentiment scores and topic modeling.
* **Phase 3 – Anomaly Detection Engine:** Detect spikes, sentiment changes, topic drift, and coordinated behavior.
* **Phase 4 – Event Intelligence & LLM Layer:** Aggregate anomalies and generate human-readable explanations.
* **Phase 5 – Real-Time Dashboard:** Display live metrics, incidents, and insights using WebSockets.

---

## How to Run

### 1. Set up environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r backend/requirements.txt
```

### 2. Start PostgreSQL

```bash
docker-compose up -d
```

### 3. Run Backend

```bash
uvicorn app.main:app --reload
```

### 4. Run Synthetic Generator

```bash
python generator/synthetic_generator.py
```

### 5. Verify Data

* Check database for posts

```sql
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10;
```

* Monitor logs for throughput and errors

---

## Notes

* `user_id` is included to enable future detection of coordinated behavior, bot detection, and user-level anomaly analysis.
* This Phase One foundation allows future integration of NLP, anomaly detection, LLM explanations, and real-time dashboards without major architectural changes.
