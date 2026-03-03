# Backend - Data Ingestion Service

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+

### 2. Installation

1. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. **Configure PostgreSQL**:
   Edit `.env` and set your database credentials:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=news_sentiment_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

3. **Create Database** (in PostgreSQL):
   ```sql
   CREATE DATABASE news_sentiment_db;
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Running the Service

**Option A: Continuous Scheduler (Recommended)**
```bash
python main.py
```
This starts the scheduler that fetches news every 5 minutes (configurable via `FETCH_INTERVAL_MINUTES` in `.env`)

**Option B: Run Once**
```bash
python -m src.scheduler
# Then press Ctrl+C and modify to call run_once()
```

### 4. Development Commands

Test database connection:
```bash
python -m src.utils test-db
```

Reset database (development only):
```bash
python -m src.utils reset-db
```

Show latest stored items:
```bash
python -m src.utils show-items
```

Count total items:
```bash
python -m src.utils count-items
```

## Architecture

```
main.py (Entry Point)
  ├─ database.py (PostgreSQL ORM)
  ├─ logger.py (Logging setup)
  ├─ scheduler.py (Scheduled execution)
  │   └─ data_pipeline.py (Orchestration)
  │       ├─ rss_fetcher.py (RSS parsing)
  │       └─ database.py (Storage)
  └─ utils.py (Development utilities)
```

## Data Flow

1. **Scheduler** triggers every N minutes (default: 5)
2. **DataPipeline** orchestrates the ingestion
3. **RSSFetcher** fetches from all configured feeds
4. **Database** stores unique items (duplicate check by URL)
5. **Logger** records all operations

## RSS Feed Sources

Currently configured feeds:
- BBC World News
- BBC Technology
- Reuters World News
- Hacker News
- TechCrunch
- The Verge

(See `src/rss_fetcher.py` to add more feeds)

## Logs

All logs are stored in the `logs/` directory with daily rotation:
- `logs/app_YYYYMMDD.log`

Console output also shows real-time status.

## Next Steps

After Milestone 1 is working:
- Implement sentiment analysis in `src/sentiment_analyzer.py`
- Add anomaly detection in `src/anomaly_detector.py`
- Create API endpoints in `src/api.py`
- Build frontend dashboard (Next.js)
