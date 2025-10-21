from .DB import DBConnection
from ..utils import cerrarCommit, cerrarConn
from ..model import Empleado, Usuario
from .usuarioDAO import UsuarioDAO

class EmpleadoDAO:
    def empleados(self) -> list[Empleado]:
        empleados: list[Empleado] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM empleado")
        resultado = cur.fetchall()
        empleados.extend(
            Empleado(
                empleado[0],
                empleado[1],
                empleado[2],
                empleado[3],
                UsuarioDAO().usuario(empleado[4])
                )
                for empleado in resultado
            )
        cerrarConn(cur, conn)
        if empleados is not None:
            return empleados
        else:
            raise TypeError("No existen empleados")
    
    def empleado(self, id_empleado: int) -> Empleado:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM empleado WHERE id_empleado = {id_empleado}")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Empleado(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                UsuarioDAO().usuario(resultado[4])
            )
        else:
            raise TypeError("No existe el empleado")
    
    def addEmpleado(self, empleado: Empleado):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO empleado ("
                + "nombre,"
                + "direccion,"
                + "telefono,"
                + "id_usuario"
            +") VALUES ("
                + f"'{empleado.nombre}',"
                + f"'{empleado.direccion}',"
                + f"{empleado.telefono}),"
                + f"{empleado.usuario.id_usuario})"
        )
        cerrarCommit(cur, conn)
    
    def updateEmpleado(self, empleado: Empleado):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE empleado "
            + "SET "
                + f"nombre='{empleado.nombre}', "
                + f"direccion='{empleado.direccion}', "
                + f"telefono={empleado.telefono}, "
                + f"id_usuario={empleado.usuario.id_usuario} "
            +"WHERE "
                + f"id_empleado={empleado.id_empleado}"
            )
        cerrarCommit(cur, conn)
    
    def deleteEmpleado(self, id_empleado: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            + "FROM "
                + "empleado "
            +"WHERE "
                + f"id_empleado={id_empleado}"
            )
        cerrarCommit(cur, conn)
        
    def buscarPorUsuario(self, usuario: Usuario) -> Empleado:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM empleado "
            + f"WHERE id_usuario = {usuario.id_usuario}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Empleado(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                usuario
            )
        else:
            raise TypeError("No existe el empleado")