import psycopg2
from dbConn.config import config

import logging
import logging.handlers

# logger = logging.getLogger("log")
# logfile = logging.handlers.RotatingFileHandler("./dbFail_log.log")
# logger.addHandler(logfile)
# logger.setLevel(logging.INFO)


def get_select(query):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        cursor = conn.cursor()
        cursor.execute(query)
        record = cursor.fetchall()

        cursor.close()

        return record
    except (Exception, psycopg2.DatabaseError) as error:
        #         loger.info(error)
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()


def get_insert(query):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        print("=" * 70)
        print(query)
        print("Query push success..")
    except (Exception, psycopg2.DatabaseError) as error:
        #         loger.info(error)
        print(error)
    finally:
        if conn is not None:
            cursor.close()
            conn.close()