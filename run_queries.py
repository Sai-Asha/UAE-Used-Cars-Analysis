import pandas as pd

def perform_queries(connection):
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
            SELECT transmission, COUNT(*) AS count FROM used_cars GROUP BY transmission;
        """,
        'fuel_type_distribution': """
            SELECT fuel_type, COUNT(*) AS count FROM used_cars GROUP BY fuel_type;
        """,
        'best_value_cars': """
            SELECT make, model, price, mileage, ROUND(price / mileage, 2) AS price_per_km
            FROM used_cars WHERE mileage > 0 ORDER BY price_per_km ASC LIMIT 10;
        """
    }
    result_dfs = {}

    for key, query in queries.items():
        result_dfs[key] = pd.read_sql(query, connection)

    return result_dfs