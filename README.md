# Gymshark Products ETL Pipeline

## 📌 Project Overview

An end-to-end ETL (Extract, Transform, Load) pipeline built to process and load Gymshark product data from Kaggle into PostgreSQL. This project demonstrates core data engineering principles including data extraction, transformation, validation, and database loading.

**Dataset**: Gymshark Products Dataset (Kaggle)  
**Records Processed**: 44,831 entries  
**Data Size**: 70.879 MB  
**Tech Stack**: Python, PostgreSQL, Pandas, Psycopg2

---

## 🎯 Project Objectives

- Build a scalable ETL pipeline from scratch
- Extract product data from CSV format
- Clean and transform raw data for analysis
- Load processed data into PostgreSQL database
- Implement error handling and data validation

---

## 🏗️ Architecture

```
CSV Source (Kaggle) 
    ↓
Extract.py → Raw Data Extraction
    ↓
Transform.py → Data Cleaning & Validation
    ↓
Load.py → PostgreSQL Database Loading
    ↓
main.py → Pipeline Orchestration
```

---

## 📂 Project Structure

```
gymshark-etl/
│
├── extract.py          # Handles data extraction from CSV
├── transform.py        # Data cleaning and transformation logic
├── load.py            # PostgreSQL connection and data loading
├── main.py            # ETL pipeline orchestrator
├── data/              # Dataset folder
│   └── gymshark_products.csv
└── README.md          # Project documentation
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.x | Core programming language |
| Pandas | Data manipulation and analysis |
| PostgreSQL | Relational database |
| Psycopg2 | PostgreSQL adapter for Python |
| PyCharm | IDE for development |

---

## ⚙️ Pipeline Components

### 1. Extract.py
- Reads CSV file from local storage
- Validates file existence and format
- Implements exception handling for file errors
- Returns raw DataFrame for processing

**Key Functions:**
- `extract_gymshark_data(file_path)` - Extracts data from CSV source

### 2. Transform.py
- Removes duplicate entries
- Handles missing values appropriately
- Validates data types and constraints
- Drops unnecessary columns
- Standardizes data format

**Key Functions:**
- `transform_gymshark_data(df)` - Cleans and transforms raw data

**Transformations Applied:**
- Dropped `inventory_quantity` column (100% null values)
- Filled missing `product_type` with "Unknown"
- Filled missing `image_src` with "No-Image"
- Validated price values (removed non-positive prices)
- Removed duplicate records

### 3. Load.py
- Establishes PostgreSQL connection
- Creates database table schema
- Performs bulk insert operations (batch size: 1000 rows)
- Implements transaction management
- Auto-handles missing columns

**Key Functions:**
- `create_connection()` - Establishes database connection
- `create_table(conn)` - Creates table schema
- `load_data(conn, df)` - Bulk inserts data into PostgreSQL

### 4. main.py
- Orchestrates the complete ETL workflow
- Manages execution sequence
- Provides pipeline status updates
- Handles end-to-end error management

---

## 📊 Database Schema

**Table**: `gymshark_products`

| Column | Data Type | Description |
|--------|-----------|-------------|
| id | SERIAL | Primary key (auto-increment) |
| title | TEXT | Product title |
| product_type | TEXT | Category of product |
| vendor | TEXT | Product vendor |
| tags | TEXT | Product tags |
| handle | TEXT | URL handle |
| variant_title | TEXT | Product variant |
| sku | TEXT | Stock keeping unit |
| price | NUMERIC | Product price |
| image_src | TEXT | Product image URL |

---

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/gymshark-etl.git
cd gymshark-etl
```

2. **Install required packages**
```bash
pip install pandas psycopg2
```

3. **Set up PostgreSQL database**
```sql
CREATE DATABASE gymshark_etl;
```

4. **Update database credentials in `load.py`**
```python
DB_CONFIG = {
    "host": "localhost",
    "dbname": "gymshark_etl",
    "user": "your_username",
    "password": "your_password",
    "port": 5432
}
```

5. **Download dataset from Kaggle and place in project directory**

---

## 💻 Usage

### Run Complete ETL Pipeline
```bash
python main.py
```

### Run Individual Components
```bash
# Extract only
python extract.py

# Transform only
python transform.py

# Load only
python load.py
```

---

## 📈 Results

- ✅ Successfully extracted **44,831 records**
- ✅ Cleaned and validated all data entries
- ✅ Loaded data into PostgreSQL with **zero errors**
- ✅ Pipeline execution time: ~2-3 minutes

**Data Quality Metrics:**
- Duplicates removed: 0
- Missing values handled: 135 records
- Invalid prices filtered: 0
- Final records loaded: 44,831

---

## 🔍 Sample SQL Queries

```sql
-- Total products count
SELECT COUNT(*) FROM gymshark_products;

-- Average product price
SELECT AVG(price) as avg_price FROM gymshark_products;

-- Products by type
SELECT product_type, COUNT(*) as count 
FROM gymshark_products 
GROUP BY product_type 
ORDER BY count DESC;

-- Top 10 expensive products
SELECT title, price 
FROM gymshark_products 
ORDER BY price DESC 
LIMIT 10;
```

---

## 🎓 Key Learnings

- Designed and implemented modular ETL architecture
- Handled large-scale data processing efficiently
- Implemented robust error handling mechanisms
- Optimized database insertion using bulk operations
- Applied data validation and cleaning techniques

---

## 🚧 Future Enhancements

- [ ] Add data quality validation dashboard
- [ ] Implement incremental data loading
- [ ] Add automated testing (unit tests)
- [ ] Create data lineage tracking
- [ ] Add logging framework
- [ ] Schedule automated pipeline runs using Apache Airflow
- [ ] Implement data versioning

---

## 👨‍💻 About Me

**Hrishikesh Sachin Khairnar**

Transitioning from Food Technology to Data Engineering. This project represents my first step into building production-ready data pipelines. Passionate about solving real-world problems through data engineering and analytics.

**Skills**: Python | SQL | PostgreSQL | ETL | Data Modeling | Pandas

---

## 📧 Contact


- **GitHub**: https://github.com/HSK01-string
- **Email**: hrishikeshkhairnar29@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Dataset source: [Kaggle - Gymshark Products Dataset]
- Inspired by real-world data engineering challenges
- Special thanks to the data engineering community

---

**⭐ If you found this project helpful, please consider giving it a star!**