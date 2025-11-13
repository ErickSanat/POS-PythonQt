from .DB import DBConnection
from ..utils import cerrarConn
from ..model import Rol

class RolDAO:
    def roles(self) -> list[Rol]:
        """Fetch all roles"""
        roles: list[Rol] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM rol")
        resultado = cur.fetchall()
        roles.extend(
            Rol(
                rol[0],
                rol[1]
            )
            for rol in resultado
        )
        cerrarConn(cur, conn)
        if roles:
            return roles
        else:
            raise TypeError("No existen roles")
    
    def rol(self, id_rol: int) -> Rol:
        """Fetch a single role by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM rol WHERE id_rol = %s", (id_rol,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Rol(resultado[0], resultado[1])
        else:
            raise TypeError("No existe el rol")
    
    def porNombre(self, nombre: str) -> Rol:
        """Get role by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM rol WHERE nombre = %s", (nombre,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Rol(resultado[0], resultado[1])
        else:
            raise TypeError("No existe el rol")