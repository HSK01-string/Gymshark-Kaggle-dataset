#!/usr/bin/env python3
"""
Load.py
- Connects to PostgreSQL
- Creates table gymshark_products
- Loads a cleaned CSV and inserts rows into the table (bulk insert)
"""

import sys
from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# ----------------CONFIG---------------
DB_CONFIG = {
    "host": "localhost",
    "dbname": "Gymshark_ETL",
    "user": "postgres",
    "password": "XYZcabcd@123",
    "port": 5432
}

TABLE_NAME = "gymshark_products"
CSV_PATH = r"C:\Users\Smita Khairnar\Downloads\gymshark_products.csv"
# --------------------------------------

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id SERIAL PRIMARY KEY,
    title TEXT,
    product_type TEXT,
    vendor TEXT,
    tags TEXT,
    handle TEXT,
    variant_title TEXT,
    sku TEXT,
    price NUMERIC,
    image_src TEXT
);
"""

INSERT_SQL = f"""
INSERT INTO {TABLE_NAME}
    (title, product_type, vendor, tags, handle, variant_title, sku, price, image_src)
VALUES %s
ON CONFLICT DO NOTHING;
"""


def create_connection(db_config=DB_CONFIG):
    """Create and return a psycopg2 connection."""
    try:
        conn = psycopg2.connect(
            host=db_config["host"],
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"],
            port=db_config["port"]
        )
        conn.autocommit = False
        print("✓ Connected to PostgreSQL")
        return conn
    except Exception as e:
        print(f"ERROR: Could not connect to PostgreSQL: {e}")
        return None


def create_table(conn):
    """Create table if it doesn't exist and ensure all columns are present"""
    try:
        with conn.cursor() as cur:
            # Create table if not exists
            cur.execute(CREATE_TABLE_SQL)
            conn.commit()

            # Check if tags column exists, add if missing
            check_col_sql = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s AND column_name = 'tags';
            """
            cur.execute(check_col_sql, (TABLE_NAME,))
            tags_exists = cur.fetchone()

            if not tags_exists:
                print("  Adding missing 'tags' column...")
                cur.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN tags TEXT;")
                conn.commit()

            print(f"✓ Table '{TABLE_NAME}' is ready")
    except Exception as e:
        conn.rollback()
        print(f"ERROR: Failed to create table: {e}")
        raise


def load_data(conn, df: pd.DataFrame, batch_size: int = 1000):
    """Bulk insert DataFrame rows into PostgreSQL using execute_values."""

    # Ensure columns exist in df; if missing add with None
    expected_cols = ["title", "product_type", "vendor", "tags",
                     "handle", "variant_title", "sku", "price", "image_src"]

    for c in expected_cols:
        if c not in df.columns:
            df[c] = None

    # Convert price to numeric; invalid->NaN->None
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Replace pandas NaN with None for psycopg2
    df = df[expected_cols].where(pd.notnull(df), None)

    # Build list of tuples
    records = [tuple(x) for x in df.to_numpy()]
    total = len(records)

    if total == 0:
        print("No rows to insert.")
        return

    print(f"Preparing to insert {total} rows into '{TABLE_NAME}'...")

    try:
        with conn.cursor() as cur:
            # Insert in batches to avoid huge single queries
            for i in range(0, total, batch_size):
                batch = records[i:i + batch_size]
                execute_values(cur, INSERT_SQL, batch, page_size=batch_size)
                print(f"  Inserted rows {i + 1} to {min(i + batch_size, total)}")

        conn.commit()
        print(f"✓ Successfully inserted {total} rows into '{TABLE_NAME}'")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: Failed during insert: {e}")
        raise


def read_csv_clean(path: Path) -> pd.DataFrame:
    """Read and clean CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    # Read the CSV file
    df = pd.read_csv(path)
    print(f"✓ CSV loaded: {len(df)} rows")

    # Clean column names: strip whitespace
    df.columns = [c.strip() for c in df.columns]

    # Normalize column names to match expected schema
    col_map = {
        "variant title": "variant_title",
        "product type": "product_type",
        "image src": "image_src"
    }

    # Rename columns if needed
    normalized = {}
    for c in df.columns:
        key = c.strip().lower()
        if key in col_map:
            normalized[c] = col_map[key]

    if normalized:
        df = df.rename(columns=normalized)

    # Keep only relevant columns
    desired = ["title", "product_type", "vendor", "tags", "handle",
               "variant_title", "sku", "price", "image_src"]

    for c in desired:
        if c not in df.columns:
            df[c] = None

    return df[desired]


def main():
    """Main ETL execution"""
    print("=" * 50)
    print("Starting ETL Load Process")
    print("=" * 50)

    # Step 1: Read CSV
    try:
        csv_path = Path(CSV_PATH)
        df = read_csv_clean(csv_path)
    except Exception as e:
        print(f"ERROR: Could not read CSV: {e}")
        sys.exit(1)

    # Step 2: Connect to PostgreSQL
    conn = create_connection()
    if conn is None:
        sys.exit(1)

    # Step 3: Create table and load data
    try:
        create_table(conn)
        load_data(conn, df)
        print("\n" + "=" * 50)
        print("ETL Load Process Completed Successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\nERROR: ETL failed: {e}")

    finally:
        if conn:
            conn.close()
            print("✓ Connection closed")


if __name__ == "__main__":
    main()