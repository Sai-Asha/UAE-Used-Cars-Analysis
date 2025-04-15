import pandas as pd

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("\n File loaded successfully")
    except FileNotFoundError:
        print("Error: File Not Found")
        return None
    except Exception as e:
        print("Error:", e)
        return None

    # print(df.isnull().sum())
    print(df.info())
    print(df.head())
    # data cleaning
    df.drop_duplicates(inplace=True) 
    df.dropna(thresh=5, inplace=True)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df['price'] = df['price'].astype(float)
    df['cylinders'] = df['cylinders'].fillna('Unknown')
    print(df.info())

    if 'year' in df.columns:
        df = df[df['year'] <= 2025]
    if 'mileage' in df.columns:
        df = df[df['mileage'] > 0]

    cleaned_data_path = 'C:/Users/saias/OneDrive/Desktop/Revature Projects/uae_used_cars_cleaned_data.csv'
    df.to_csv(cleaned_data_path, index=False)
    print("\n Cleaned data saved to", cleaned_data_path)
    return df
