import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'C:/Users/saias/OneDrive/Desktop/Revature Projects/uae_used_cars_10k.csv'

# File Handling
try:
    df = pd.read_csv(file_path)
    print("File loaded successfully")
except FileNotFoundError:
    print("Error: File Not Found")
except Exception as e:
    print("Error: An error occurred: ",e)

df_backup = df.copy()
print(df.info())
print(df.head())

# Remove duplicates and handle missing values
df.drop_duplicates(inplace=True)
df.dropna(thresh=5, inplace=True)

# Cleaning column names(Normalize column names)
new_columns = []
for col in df.columns:
    cleaned_col = col.strip().lower().replace(" ", "_")
    new_columns.append(cleaned_col)
df.columns = new_columns

df['price'] = df['price'].astype(float)

# Fill missing values in 'cylinders' column
df['cylinders'] = df['cylinders'].fillna('Unknown')

# Filter unrealistic data
if 'year' in df.columns:
    df = df[df['year'] <= 2025]
if 'mileage' in df.columns:
    df = df[df['mileage'] > 0]

print("\n Data is cleaned successfully \n")
print(df.head())

cleaned_data_path = 'C:/Users/saias/OneDrive/Desktop/Revature Projects/uae_used_cars_cleaned_data.csv'
df.to_csv(cleaned_data_path, index=False)
print("\n Cleaned data saved to", cleaned_data_path)


connection = mysql.connector.connect(host='localhost', password = 'Asha#1039', user = 'root', database= 'uae_used_cars_db')
try:
    if connection.is_connected():
        print("connection established ")
except mysql.connector.Error as e:
    print("MySql conncetion Error: ", e)

cursor = connection.cursor()

insert_query = "INSERT INTO used_cars (make, model, year, price, mileage, body_type,cylinders, transmission, fuel_type, color, location, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

for index, row in df.iterrows():
    data_tuple = (
    row['make'], row['model'], row['year'], row['price'],
    row['mileage'], row['body_type'], row['cylinders'],
    row['transmission'], row['fuel_type'], row['color'],
    row['location'], row['description'])
    
    try:
        cursor.execute(insert_query, data_tuple)
    except mysql.connector.Error as err:
        print("Error inserting at row", index,":",err)

connection.commit()
print("Rows inserted into MySQL successfully")
cursor.close()

# Queries for all computations
queries = {
    'avg_price_by_brand_model_year': """
        SELECT make, model, year, ROUND(AVG(price), 2) AS avg_price
        FROM used_cars
        GROUP BY make, model, year
        ORDER BY avg_price DESC;
    """,
    'most_common_makes_models': """
        SELECT make, model, COUNT(*) AS total_listings
        FROM used_cars
        GROUP BY make, model
        ORDER BY total_listings DESC
        LIMIT 10;
    """,
    'price_trends_by_year': """
        SELECT year, ROUND(AVG(price), 2) AS avg_price, ROUND(AVG(mileage), 2) AS avg_mileage
        FROM used_cars
        GROUP BY year
        ORDER BY year;
    """,
    'transmission_distribution': """
        SELECT transmission, COUNT(*) AS count
        FROM used_cars
        GROUP BY transmission;
    """,
    'fuel_type_distribution': """
        SELECT fuel_type, COUNT(*) AS count
        FROM used_cars
        GROUP BY fuel_type;
    """,
    'best_value_cars': """
        SELECT make, model, price, mileage, ROUND(price / mileage, 2) AS price_per_km
        FROM used_cars
        WHERE mileage > 0
        ORDER BY price_per_km ASC
        LIMIT 10;
    """
}
# Run all queries
results = {}
for key, query in queries.items():
    results[key] = pd.read_sql(query, connection)

# Print results for each
for key, result_df in results.items():
    print(f"\n {key}:")
    print(result_df.head())

print("\n🔍 Summary Statistics and Key Metrics:")
summary_stats = df.describe()
print(summary_stats)

# Assuming avg_price_by_year is already defined as a DataFrame
plt.figure(figsize=(10, 6))
# avg_price_by_year = results['price_trends_by_year']
sns.lineplot(data=results['price_trends_by_year'], x='year', y='avg_price')
plt.title('Average Price of Used Cars by Year')
plt.xlabel('Year')
plt.ylabel('Average Price')
plt.grid(True)
plt.tight_layout()
plt.show()

# Top 10 Most Listed Car Models
top_models = df.groupby(['make', 'model']).size().reset_index(name='count')
top_10 = top_models.sort_values('count', ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(data=top_10, x='count', y=top_10['make'] + ' ' + top_10['model'], palette='viridis')
plt.title('Top 10 Most Listed Car Models')
plt.xlabel('Count')
plt.ylabel('Car')
plt.tight_layout()
plt.show()

# Transmission Type Distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=df, y='transmission', order=df['transmission'].value_counts().index, palette='magma')
plt.title('Distribution of Transmission Types')
plt.xlabel('Count')
plt.ylabel('Transmission Type')
plt.tight_layout()
plt.show()

#   Fuel Type Distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=df, y='fuel_type', order=df['fuel_type'].value_counts().index, palette='coolwarm')
plt.title('Distribution of Fuel Types')
plt.xlabel('Count')
plt.ylabel('Fuel Type')
plt.tight_layout()
plt.show()

# Close connection
connection.close()
print("MySQL connection closed.")

