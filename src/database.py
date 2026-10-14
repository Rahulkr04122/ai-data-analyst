import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "ai_analyst_db"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connection_timeout=5,
    )

if __name__=="__main__":
    connection = None

    try:
        
        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")
        database_name, mysql_version = cursor.fetchone()

        print("Connection successful!")
        print("Database:", database_name)
        print("MySQL version:", mysql_version)

        cursor.close()

    except mysql.connector.Error as error:
        print("MySQL connection failed:", error)

