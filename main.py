from data_loading_cleaning import load_data
from db_connection import create_connection, insert_data
from run_queries import perform_queries
from analytics_output import show_console_output

file_path = 'C:/Users/saias/OneDrive/Desktop/Revature Projects/uae_used_cars_10k.csv'
df = load_data(file_path)

if df is not None:
    connection = create_connection()
    insert_data(df, connection)
    results = perform_queries(connection)
    show_console_output(df, results)
    connection.close()
    print("MySQL connection closed.")