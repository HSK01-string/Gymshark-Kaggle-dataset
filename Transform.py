import pandas as pd

# Load the data
df = pd.read_csv(r"C:\Users\Smita Khairnar\Downloads\gymshark_products.csv")

# Check Basic info
print("Dataset shape:", df.shape)
print("\nColumn Names and types:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst few rows:")
print(df.head())

print("\nDuplicate rows:")
print(df.duplicated().sum())

import pandas as pd

def transform_gymshark_data(df):
    """Clean and Transform Gymshark Data"""
    df = df.copy()

    # Drop inventory_quantity column if empty
    if 'inventory_quantity' in df.columns and df['inventory_quantity'].isna().all():
        df = df.drop(columns=['inventory_quantity'])

    # Fill missing values
    if 'product_type' in df.columns:
        df['product_type'] = df['product_type'].fillna("Unknown")

    if 'image_src' in df.columns:
        df['image_src'] = df['image_src'].fillna("No-Image")

    # Validate price
    if 'price' in df.columns:
        df = df[df['price'] > 0]

    # Remove duplicates
    df = df.drop_duplicates()

    print(f"Rows after cleaning: {len(df)}")
    return df

if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\Smita Khairnar\Downloads\gymshark_products.csv")
    cleaned_df = transform_gymshark_data(df)
    cleaned_df.to_csv(r"C:\Users\Smita Khairnar\Downloads\gymshark_products_cleaned.csv", index=False)
    print("Cleaned data saved!")
    
