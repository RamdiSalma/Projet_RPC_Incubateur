import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")


connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};DATABASE={db_name};UID={db_user};PWD={db_password}"

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

def insert_alerte(date_heure, temperature, type_alerte):
    cursor.execute('''
        INSERT INTO Incident (date_heure, temperature, type_alerte)
        VALUES (?, ?, ?)
    ''', date_heure, temperature, type_alerte)
    conn.commit()

def get_medecin(username):
    cursor.execute("SELECT password FROM Medecin WHERE nom = ?", username)
    return cursor.fetchone()

def get_medecin_info(username):
    cursor.execute("""
        SELECT nom, prenom, departement FROM Medecin WHERE nom = ?
    """, username)
    return cursor.fetchone()  

def get_all_incidents():
    cursor.execute("""
        SELECT date_heure, temperature, type_alerte FROM Incident ORDER BY date_heure DESC
    """)
    return cursor.fetchall()  

