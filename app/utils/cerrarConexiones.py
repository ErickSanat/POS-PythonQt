from ..dao.DB import DBConnection

def cerrarCommit(cur, conn):
    """Commit transaction and return connection to pool"""
    conn.commit()
    cur.close()
    DBConnection.return_connection(conn)
    
def cerrarConn(cur, conn):
    """Close cursor and return connection to pool"""
    cur.close()
    DBConnection.return_connection(conn)