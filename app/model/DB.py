from psycopg2 import connect

class DBConnection():
    database="pasteleria_alquimia"
    user="postgres"
    password="passwd"
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
