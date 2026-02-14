# crypto-price-analytics-dashboard-airflow
Data Engineering project: Crypto price ingestion pipeline. Orchestrates Binance API extraction, PostgreSQL storage, and Excel reporting with Apache Airflow.

# Crypto ETL Pipeline

Automated ETL pipeline that extracts cryptocurrency prices from Binance API, transforms and validates the data, and loads it into PostgreSQL. Orchestrated with Apache Airflow and containerized with Docker.

## Features
- Real-time price extraction for 5 major cryptocurrencies
- Data validation and quality checks
- Automated execution every 6 hours using Airflow
- Dockerized infrastructure for portability

## Tech Stack
- **Python 3.8+** - ETL logic
- **Apache Airflow 2.7.1** - Workflow orchestration
- **PostgreSQL 13** - Data storage
- **Docker & Docker Compose** - Containerization
- **Binance API** - Data source

## Architecture
```
Binance API → Extract (Python) → Transform → Load → PostgreSQL
                    ↑
              Airflow Scheduler
```

## Setup

1. Clone repository
2. Start services:
```bash
docker-compose up -d
```
3. Access Airflow UI: `localhost:8080`
   - User: `airflow`
   - Password: `airflow`

## Database Schema
```sql
CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    price DECIMAL(18, 8),
    time TIMESTAMP
);
```

## Future Improvements
- Add price change alerts for volatility >5%
- Implement moving averages (7-day, 30-day)
- Add email/Slack notifications
- Create Grafana dashboard
```
