import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def show_console_output(df, results):
    print("\n------------ Summary Statistics and Key Metrics -------------")
    print(df.describe())

    avg_price_by_year = df.groupby('year')['price'].mean().reset_index()
    print("\n---------- Average Price by Year -------------")
    print(avg_price_by_year)

    print("\n----------Transmission Type Distribution----------")
    print(df['transmission'].value_counts())

    print("\n---------- Fuel Type Distribution --------------")
    print(df['fuel_type'].value_counts())

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=avg_price_by_year, x='year', y='price')
    plt.title('Average Price of Used Cars by Year')
    plt.xlabel('Year')
    plt.ylabel('Average Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    top_10 = df.groupby(['make', 'model']).size().reset_index(name='count')
    top_10 = top_10.sort_values('count', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10, x='count', y=top_10['make'] + ' ' + top_10['model'], hue=top_10['make'] + ' ' + top_10['model'], palette='viridis', legend=False)
    plt.title('Top 10 Most Listed Car Models')
    plt.xlabel('Count')
    plt.ylabel('Car')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, y='transmission',order=df['transmission'].value_counts().index, hue='transmission', palette='magma', legend=False)
    plt.title('Distribution of Transmission Types')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, y='fuel_type', order=df['fuel_type'].value_counts().index, hue='fuel_type', palette='coolwarm', legend=False)
    plt.title('Distribution of Fuel Types')
    plt.tight_layout()
    plt.show()