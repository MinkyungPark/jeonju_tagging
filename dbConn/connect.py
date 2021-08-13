import psycopg2
from dbConn.config import config


def connect():
    conn = None
    try:
        params = config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        cursor = conn.cursor()
        cursor.execute("SELECT * from scraping.instagram LIMIT 1")
        record = cursor.fetchall()
        print("Result", record)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    connect()