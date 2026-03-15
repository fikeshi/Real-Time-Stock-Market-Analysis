## Project Name: Real Time Stock Market Analysis

The project implements a real time data pipeline that extracts data from vantage API, streams it thrugh kafka, process it with Apache Spark and loads it into a postgres database

All components are containerized with docker for easy deployment 


### Data Pipeline Architecture
![Data pipeline Architecture](./img/real_time_pipeline%20architecture.png)

Project Tech Stack and Flow
- `Kafka UI - inspect topics/messages`
- `API - produces JSON events into Kafka`
- `Spark - consumes from kafka, writes to postgres`
- `Postgres - stores result for analytics`
- `Pgadmin - manage Postgres visually.`
- `Power BI - external(connects to postgres database)`
