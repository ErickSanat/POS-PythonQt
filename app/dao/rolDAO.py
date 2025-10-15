from .DB import DBConnection
from ..model import Rol

class RolDAO:
    @staticmethod
    def roles() -> list[Rol]:
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
        cur.close()
        conn.close()
        return roles
    
    @staticmethod
    def rol(id_rol: int) -> Rol:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM rol WHERE id_rol = {id_rol}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Rol(resultado[0], resultado[1])