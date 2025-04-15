import mysql.connector

# Establishing connection with MySQL
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Asha#1039',
        database='uae_used_cars_db'
    )
    if connection.is_connected():
        print("\n MySQL connection established")
    return connection

# Inserting values to mysql database table
def insert_data(df, connection):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO used_cars (make, model, year, price, mileage, body_type,cylinders, transmission, fuel_type, color, location, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    for index, row in df.iterrows():
        data_tuple = (
            row['make'], row['model'], row['year'], row['price'],
            row['mileage'], row['body_type'], row['cylinders'],
            row['transmission'], row['fuel_type'], row['color'],
            row['location'], row['description']
        )
        try:
            cursor.execute(insert_query, data_tuple)
        except mysql.connector.Error as e:
            print(f"Error inserting row {index}: {e}")

    connection.commit()
    cursor.close()
    print("\n Data inserted into MySQL successfully")