import kagglehub
import sqlite3
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Password1!",
    database="cs4501"
)

cursor = conn.cursor()

cursor.execute("SELECT Location FROM GreaterManchesterCrime LIMIT 5")

for row in cursor.fetchall():
    print(row)

# db = sqlite3.connect("countries.db")
# Download latest version
# path = kagglehub.dataset_download("marchman/geo-nuclear-data")

# print("Path to dataset files:", path)
