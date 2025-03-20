import sqlite3
import os
from config import DB_PATH

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Victor_locations.db")

# Function to retrieve POIs for multiple cities
def get_pois(cities):
    """ Retrieve POIs for multiple cities based on user preferences. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    pois = []
    for city_data in cities:
        city_name = city_data["name"]
        types = city_data["poi_types"]
        query = "SELECT name, city, type, price, time, latitude, longitude FROM attractions WHERE city = ?"
        params = [city_name]

        if types:
            query += " AND type IN ({})".format(", ".join(["?"] * len(types)))
            params += types

        cursor.execute(query, params)
        pois.extend(cursor.fetchall())

    conn.close()
    return pois
