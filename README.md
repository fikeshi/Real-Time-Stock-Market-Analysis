## Real Time Stock Market Analysis

### Background 
Financial data is only valuable when its timely. Traditional batch pipelines that process stock data hours after the fact are insufficient for analytics teams who need to track price movements, volumes spikes and market trends as they happen. This project builds a fully containerised, real-time data pipeline that ingests live stock market data from the Alpha Vantage API, streams it through Apache Kafka, processes it with PySpark Structured Streaming and persists it to a PostgreSQL database all visualised through Power BI dashboards.

### Overview
This project implements an end-to-end real-time data pipeline for stock market analysis. A Python producer continuously polls the Alpha Vantage API and publishes JSON events to a Kafka topic. A PySpark Structured Streaming consumer reads from that topic, applies transformations and writes the cleaned data to PostgreSQL. pgAdmin provides a visual interface for database management, Kafka UI allows inspection of topics and message flow, and Power BI connects directly to PostgreSQL for live dashboard reporting

Every component runs inside Docker containers, making the entire stack reproducible with a single docker compose up command. 

### Data Pipeline Architecture
![Data pipeline Architecture](./img/real_time_pipeline%20architecture.png)

### Project Setup Guide
This guide will walk you through setting up the project environment including repository setup.
#### Prerequisites
- Docker Desktop
- Python 3.10+ 
- Alpha Vantage API Key — free tier available at https://www.alphavantage.co
- Power BI Desktop (for dashboard access —)


### Step 1: Clone the Repository

```bash
git clone https://github.com/fikeshi/Real-Time-Stock-Market-Analysis.git
cd Real-Time-Stock-Market-Analysis
```

### Step 2: Configure Environment Variables

Create a `.env` file in the root of the project directory:

```
ALPHA_VANTAGE_API_KEY=your_api_key_here
POSTGRES_USER=admin 
POSTGRES_PASSWORD=admin
POSTGRES_DB=stock_data
```
Note: The PostgreSQL credentials shown here are default values used for local development and are already defined in the project configuration


### Step 3: Start All Services

```bash
docker compose up -d
```
This will pull and start the following containers:
- `spark-master` — Spark master node
- `spark-worker` — Spark worker node (2 cores, 2GB memory)
- `consumer` — PySpark Structured Streaming job
- `kafka` — Confluent Kafka broker
- `kafka-ui` — Kafka UI dashboard
- `postgres` — PostgreSQL database
- `pgadmin` — pgAdmin for web UI


### Step 4: Start the Producer

The producer runs outside Docker and publishes stock data to Kafka. In a separate terminal:

```bash
pip install -r requirements.txt
cd producer
python producer.py
```
The producer will begin polling the Alpha Vantage API and publishing JSON messages to the `stock_analysis` Kafka topic.

Project Tech Stack and Flow
- `Kafka UI - inspect topics/messages`
- `API - produces JSON events into Kafka`
- `Spark - consumes from kafka, writes to postgres`
- `Postgres - stores result for analytics`
- `Pgadmin - manage Postgres visually.`
- `Power BI - external(connects to postgres database)`
