from .DB import DBConnection
from ..utils import cerrarCommit, cerrarConn
from ..model import Rol

class RolDAO:
    def roles(self) -> list[Rol]:
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
        if roles is not None:
            return roles
        else:
            raise TypeError("No existen roles")
    
    def rol(self, id_rol: int) -> Rol:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM rol WHERE id_rol = {id_rol}")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Rol(resultado[0], resultado[1])
        else:
            raise TypeError("No existe el rol")
    
    def porNombre(self, nombre: str) -> Rol:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM rol WHERE nombre = '{nombre}'")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Rol(resultado[0], resultado[1])
        else:
            raise TypeError("No existe el rol")