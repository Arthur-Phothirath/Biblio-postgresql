import psycopg2
from db.config import config

def connect():
    """ Connect to the PostgreSQL database server """
    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    return psycopg2.connect(**params)

conn = connect()

class Crud:
    # fetch
    @staticmethod
    def fetchOne(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()
    @staticmethod
    def fetchAll(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    @staticmethod
    def mutation(query):
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    