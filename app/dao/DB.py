from psycopg2 import connect
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
import os

class DBConnection():
    load_dotenv()
    database=os.getenv("DB_NAME") or "pasteleria_alquimia"
    user=os.getenv("DB_USER") or "postgres"
    password=os.getenv("DB_PASS") or "passwd"
    host="localhost"
    port="5432"
    
    # Connection pool for better performance
    _pool = None
    
    @classmethod
    def _get_pool(cls):
        """Initialize connection pool if not already created"""
        if cls._pool is None:
            try:
                cls._pool = SimpleConnectionPool(
                    1,  # min connections
                    10,  # max connections
                    database=cls.database,
                    user=cls.user,
                    password=cls.password,
                    host=cls.host,
                    port=cls.port
                )
            except Exception as e:
                print(f"Error creating connection pool: {e}")
        return cls._pool
    
    @staticmethod
    def connection() -> connect:
        """Get a connection from the pool"""
        conn = None
        try:
            pool = DBConnection._get_pool()
            if pool:
                conn = pool.getconn()
        except Exception as e:
            print(f"Error getting connection from pool: {e}")
        return conn
    
    @staticmethod
    def return_connection(conn):
        """Return a connection to the pool"""
        try:
            pool = DBConnection._get_pool()
            if pool and conn:
                pool.putconn(conn)
        except Exception as e:
            print(f"Error returning connection to pool: {e}")
