import sys
from Extract import extract_gymshark_data
from Transform import transform_gymshark_data
from Load import create_connection, create_table, load_data

# Configuration
CSV_PATH = r"C:\Users\Smita Khairnar\Downloads\gymshark_products.csv"

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Complete ETL Pipeline")
    print("=" * 50)

    # Step 1: Extract
    print("\n[1/3] EXTRACTING data...")
    raw_data = extract_gymshark_data(CSV_PATH)
    if raw_data is None:
        print("ERROR: Extraction failed!")
        sys.exit(1)

    # Step 2: Transform
    print("\n[2/3] TRANSFORMING data...")
    clean_data = transform_gymshark_data(raw_data)

    # Step 3: Load
    print("\n[3/3] LOADING data to PostgreSQL...")
    conn = create_connection()
    if conn is None:
        print("ERROR: Connection failed!")
        sys.exit(1)

    try:
        create_table(conn)
        load_data(conn, clean_data)
    except Exception as e:
        print(f"ERROR during load: {e}")
    finally:
        conn.close()

    print("\n" + "=" * 50)
    print("ETL Pipeline Completed Successfully!")
    print("=" * 50)
