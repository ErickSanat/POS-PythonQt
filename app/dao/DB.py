from psycopg2 import connect
from dotenv import load_dotenv
import os

class DBConnection():
    load_dotenv()
    database=os.getenv("DB_NAME") or "pasteleria_alquimia"
    user=os.getenv("DB_USER") or "postgres"
    password=os.getenv("DB_PASS") or "passwd"
    host="localhost"
    port="5432"
    @staticmethod
    def connection() -> connect:
        conn = None
        try:
            conn = connect(
            database=DBConnection.database,
            user=DBConnection.user,
            password=DBConnection.password,
            host=DBConnection.host,
            port=DBConnection.port
            )
        except Exception as e:
            print(f"Error connecting to database: {e}")
        finally:
            if conn is not None:
                return conn
