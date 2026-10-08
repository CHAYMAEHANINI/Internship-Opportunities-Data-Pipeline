# 🚀 Internship Opportunities Data Pipeline

An end-to-end **Data Engineering project** that automatically collects internship opportunities from web sources, processes and validates the data, stores it in PostgreSQL, exposes it through a FastAPI backend, and provides an interactive dashboard for searching and filtering opportunities.

The project is designed as a **Dockerized data application**, combining web scraping, data processing, database management, REST APIs, and a frontend dashboard into one reproducible workflow.

---

## 📌 Project Overview

Internship opportunities are often distributed across multiple websites and presented in inconsistent formats.

This project aims to build a centralized pipeline that:

* Extracts internship opportunities from web sources
* Collects structured information such as title, company, location, internship type, skills, and dates
* Cleans and validates the extracted data
* Normalizes dates and text fields
* Generates a unique identifier for each opportunity
* Detects previously processed opportunities
* Stores structured data in PostgreSQL
* Exposes the data through a REST API
* Provides an interactive dashboard for exploration
* Runs the main application components using Docker

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │  Internship Websites │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Scrapy         │
                    │   Web Extraction     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Raw JSON        │
                    │    data/raw/         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Transformation     │
                    │  Clean / Validate    │
                    │  Normalize / Filter  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Processed JSON     │
                    │ data/processed/      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │   Persistent Storage │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │      REST API        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Dashboard       │
                    │ Search & Filtering   │
                    └──────────────────────┘
```

---

## 🔄 Data Pipeline

The pipeline follows an **Extract → Transform → Load (ETL)** workflow.

### 1. Extract

**Technology:** Scrapy

The scraper collects internship opportunities from supported websites and extracts structured fields such as:

* Internship title
* Company
* Location
* Work mode
* Internship type
* Stipend
* Description
* Skills
* Publication date
* Application deadline
* Source URL
* Source website

The scraper is configured to respect website `robots.txt` rules.

---

### 2. Transform

The transformation layer prepares the extracted data for storage.

Processing includes:

* Text cleaning
* Required-field validation
* Date normalization
* Invalid-record filtering
* Unique ID generation
* Data standardization

The transformation stage produces a structured processed dataset ready for database loading.

---

### 3. Load

**Technology:** PostgreSQL

Validated internship records are loaded into a relational database.

The database provides persistent storage and enables efficient querying from the backend.

The internship table uses a unique identifier to prevent duplicate database records.

---

## 🆕 Offer Identification

Each internship opportunity receives a deterministic identifier generated from its source URL.

```text
Offer URL
    ↓
Hash
    ↓
Unique Offer ID
```

This identifier allows the pipeline to distinguish previously processed opportunities from newly discovered ones.

The project maintains processing state to support incremental offer detection.

---

## 🗄️ Database

### PostgreSQL Schema

The main `internships` table contains:

| Column                 | Description                   |
| ---------------------- | ----------------------------- |
| `id`                   | Unique internship identifier  |
| `title`                | Internship title              |
| `company`              | Company name                  |
| `location`             | Internship location           |
| `work_mode`            | Remote / On-site / Hybrid     |
| `stipend`              | Compensation information      |
| `internship_type`      | Internship / PFE / other type |
| `description`          | Opportunity description       |
| `skills`               | Required skills               |
| `published_at`         | Publication timestamp         |
| `application_deadline` | Application deadline          |
| `url`                  | Original opportunity URL      |
| `source`               | Source website                |
| `scraped_at`           | Extraction timestamp          |

---

## ⚙️ Backend API

**Technology:** FastAPI

The backend provides REST endpoints for accessing and querying internship data.

### Available endpoints

```text
GET /
GET /internships
GET /locations
GET /stats
```

### `/internships`

Supports data exploration through:

* Search
* Location filtering
* Work-mode filtering
* Internship-type filtering
* Pagination

The API acts as the bridge between PostgreSQL and the frontend dashboard.

---

## 📊 Dashboard

The frontend provides an interactive interface for exploring internship opportunities.

### Main features

* Internship opportunity cards
* Search
* Dynamic filters
* Location filtering
* Work-mode filtering
* Internship-type filtering
* Pagination
* Statistics
* Loading states
* Empty-result handling
* API error handling

The dashboard consumes data directly from the FastAPI backend.

---

## 🐳 Docker Architecture

The application is containerized using **Docker Compose**.

### Services

```text
┌────────────────────┐
│     PostgreSQL     │
└────────────────────┘

┌────────────────────┐
│      Backend       │
│      FastAPI       │
└────────────────────┘

┌────────────────────┐
│      Frontend      │
│      Dashboard     │
└────────────────────┘

┌────────────────────┐
│       Scraper      │
│       Scrapy       │
└────────────────────┘
```

Docker Compose allows the different components to run as an integrated application with reproducible configuration.

---

## 📁 Project Structure

```text
Internship-Opportunities-Data-Pipeline/
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── database/
│       │   ├── database.py
│       │   └── test_connection.py
│       │
│       ├── services/
│       │   └── internship_service.py
│       │
│       └── main.py
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── pipeline/
│   ├── jobs/
│   │   └── run_pipeline.py
│   │
│   ├── load/
│   │   ├── load_to_postgres.py
│   │   └── test_db_connection.py
│   │
│   ├── scraper/
│   │   ├── spiders/
│   │   │   └── publimaroc.py
│   │   ├── items.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── scrapy.cfg
│   │
│   └── transform/
│       └── transform.py
│
├── data/
│   ├── raw/
│   │   └── publimaroc.json
│   │
│   └── processed/
│       ├── internships.json
│       └── seen_offers.json
│
├── tests/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## ▶️ Running the Project

### Prerequisites

Make sure the following are installed:

* Python 3.12+
* Docker
* Docker Compose
* PostgreSQL
* Git

---

### 1. Clone the repository

```bash
git clone <your-repository-url>

cd Internship-Opportunities-Data-Pipeline
```

---

### 2. Start the Dockerized application

```bash
docker compose up --build
```

This starts the main application services.

---

### 3. Run the data pipeline

From the project root:

```bash
python pipeline/jobs/run_pipeline.py
```

The orchestration script executes:

```text
Scrapy
  ↓
Raw JSON
  ↓
Transformation
  ↓
Processed JSON
  ↓
PostgreSQL
```

---

## 🧪 Data Quality & Validation

The pipeline includes validation mechanisms to ensure that records contain the required information before being processed further.

Required fields include:

* `title`
* `published_at`
* `url`
* `source`

The transformation layer also normalizes text and date formats before database loading.

---

## 🔍 Current Data Source

The current implementation includes internship extraction from **Publimaroc**.

The scraper is designed with a modular structure so that additional internship sources can be integrated as independent Scrapy spiders.

---

## 🛠️ Tech Stack

### Data Engineering

* Python
* Scrapy
* Pandas
* ETL / Data Pipeline concepts
* Data Cleaning
* Data Validation
* Incremental Processing

### Database

* PostgreSQL
* SQL

### Backend

* FastAPI
* REST API
* Uvicorn
* Psycopg

### Frontend

* HTML
* CSS
* JavaScript

### DevOps

* Docker
* Docker Compose

### Development

* Git
* VS Code

---

## 🎯 Engineering Concepts Demonstrated

This project demonstrates practical understanding of:

* Web data extraction
* ETL pipeline design
* Data ingestion
* Data cleaning and normalization
* Data validation
* Unique identifier generation
* Incremental data processing
* Relational database storage
* REST API development
* Backend–database integration
* Frontend–API integration
* Containerization
* Multi-service application architecture

---

## 🚀 Future Improvements

The project architecture allows several future extensions:

* Additional internship websites
* Automated periodic scraping
* Advanced incremental processing
* User preference management
* Personalized internship matching
* Email notifications for newly discovered opportunities
* Advanced data quality monitoring
* Automated testing
* CI/CD
* Production deployment

---

## 👩‍💻 Author

**Chaymae Hanini**

Master's Student — Big Data & Smart Systems
Focus: **Data Engineering & AI**

---

## ⭐ Project Goal

This project was developed as a practical Data Engineering application to demonstrate the complete journey of data from **web extraction to a usable data product**:

```text
Extract → Transform → Store → Serve → Visualize
```

The goal is not only to collect internship data, but to build a reproducible and extensible data pipeline connected to a real web application.
