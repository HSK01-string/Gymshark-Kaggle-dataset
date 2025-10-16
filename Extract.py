import pandas as pd

def extract_gymshark_data(file_path):
    """Extract data from Gymshark CSV"""
    try:
        df = pd.read_csv(file_path)
        print(f"Extracted {len(df)} rows")
        return df  # Make sure this returns df
    except Exception as e:
        print(f"Error: {e}")
        return None
if __name__ == "__main__":
    data = extract_gymshark_data(r"C:\Users\Smita Khairnar\Downloads\gymshark_products.csv")
    if data is not None:
        print(data.head())
