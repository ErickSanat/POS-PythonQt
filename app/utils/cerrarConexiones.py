def cerrarCommit(cur, conn):
    conn.commit()
    cur.close()
    conn.close()
    
def cerrarConn(cur, conn):
    cur.close()
    conn.close()