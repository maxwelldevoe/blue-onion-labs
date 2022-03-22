from unittest import result
import pymysql
import os
import json
from datetime import datetime, timezone


starlink_data = os.path.expanduser("/data.json")

db = pymysql.connect(
    user="root",
    password="testpass",
    host="db",
    database="default"
)

def load_data():
    with open(starlink_data, "r") as file:
        data = json.load(file)
        with db.cursor() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS data(
                    id varchar(225),
                    longitude int,
                    latitude float,
                    read_time time,
                    read_date date
                )
                """
            )
            values = []
            for row in data:
                if None not in row.values():
                    values.append(f"{(row['id'], row['longitude'], row['latitude'], datetime.fromisoformat(row['spaceTrack']['CREATION_DATE']).astimezone(timezone.utc).strftime('%H:%M:%S'), datetime.fromisoformat(row['spaceTrack']['CREATION_DATE']).astimezone(timezone.utc).strftime('%Y-%m-%d'))}")
            c.execute(f"""
                INSERT INTO data (id, longitude, latitude, read_time, read_date)
                VALUES {', '.join(values)}
                """
            )
    print("Data Successfully Loaded Into Table")

def query(filters=None):
    with db.cursor(pymysql.cursors.DictCursor) as c:
        if filters:                
            if "id" in filters.keys():
                c.execute(f"SELECT * FROM data WHERE id = '{filters['id']}'")
            elif "time" in filters.keys():
                c.execute(f"SELECT * FROM data WHERE read_time = '{filters['time']}'")
        else:
            c.execute("SELECT * FROM data LIMIT 50")
        result = c.fetchall()
    return json.dumps(result, default=str)

def home_query():
    with db.cursor(pymysql.cursors.DictCursor) as c:
        c.execute("SELECT id from data LIMIT 50")
        result = c.fetchall()
    return result