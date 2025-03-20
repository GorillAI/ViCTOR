import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Victor_locations.db")

def get_pois(city, categories=[]):
    """ Retrieve POIs for a given city. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT name, city, type, price, time FROM attractions WHERE city = ?"
    params = [city]

    if categories:
        query += " AND type IN ({})".format(", ".join(["?"] * len(categories)))
        params += categories

    cursor.execute(query, params)
    pois = cursor.fetchall()
    conn.close()
    
    return pois
