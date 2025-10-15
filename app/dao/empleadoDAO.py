from .DB import DBConnection
from ..model import Empelado
from .usuarioDAO import UsuarioDAO

class EmpleadoDAO:
    @staticmethod
    def empleados() -> list[Empelado]:
        empleados: list[Empelado] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM empleado")
        resultado = cur.fetchall()
        empleados.extend(
            Empelado(
                empleado[0],
                empleado[1],
                empleado[2],
                empleado[3],
                UsuarioDAO.usuario(empleado[4])
                )
                for empleado in resultado
            )
        cur.close()
        conn.close()
        return empleados
    
    @staticmethod
    def empleado(id_empleado: int) -> Empelado:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM empleado WHERE id_empleado = {id_empleado}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Empelado(
            resultado[0],
            resultado[1],
            resultado[2],
            resultado[3],
            UsuarioDAO.usuario(resultado[4])
        )