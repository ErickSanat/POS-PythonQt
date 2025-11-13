from .DB import DBConnection
from ..utils import cerrarCommit, cerrarConn
from ..model import Empleado, Usuario, Rol

class EmpleadoDAO:
    def empleados(self) -> list[Empleado]:
        """Fetch all employees with their users and roles in a single query using JOIN"""
        empleados: list[Empleado] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            "SELECT e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM empleado e "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol"
        )
        resultado = cur.fetchall()
        empleados.extend(
            Empleado(
                empleado[0],  # id_empleado
                empleado[1],  # nombre
                empleado[2],  # direccion
                empleado[3],  # telefono
                Usuario(empleado[4], empleado[5], empleado[6], Rol(empleado[7], empleado[8]))  # usuario
            )
            for empleado in resultado
        )
        cerrarConn(cur, conn)
        if empleados:
            return empleados
        else:
            raise TypeError("No existen empleados")
    
    def empleado(self, id_empleado: int) -> Empleado:
        """Fetch a single employee by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection and JOIN to avoid extra queries
        cur.execute(
            "SELECT e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM empleado e "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "WHERE e.id_empleado = %s",
            (id_empleado,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Empleado(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                Usuario(resultado[4], resultado[5], resultado[6], Rol(resultado[7], resultado[8]))
            )
        else:
            raise TypeError("No existe el empleado")

    def empleadoExistente(self, empleado: Empleado) -> Empleado | bool:
        """Check if employee exists by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM empleado e "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "WHERE e.id_empleado = %s",
            (empleado.id_empleado,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Empleado(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                Usuario(resultado[4], resultado[5], resultado[6], Rol(resultado[7], resultado[8]))
            )
        else:
            return False
    
    def addEmpleado(self, empleado: Empleado):
        """Add a new employee using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO empleado (nombre, direccion, telefono, id_usuario) VALUES (%s, %s, %s, %s)",
            (empleado.nombre, empleado.direccion, empleado.telefono, empleado.usuario.id_usuario)
        )
        cerrarCommit(cur, conn)
    
    def updateEmpleado(self, empleado: Empleado):
        """Update an employee using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE empleado SET nombre=%s, direccion=%s, telefono=%s, id_usuario=%s WHERE id_empleado=%s",
            (empleado.nombre, empleado.direccion, empleado.telefono, 
             empleado.usuario.id_usuario, empleado.id_empleado)
        )
        cerrarCommit(cur, conn)
    
    def deleteEmpleado(self, id_empleado: int):
        """Delete an employee using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM empleado WHERE id_empleado=%s", (id_empleado,))
        cerrarCommit(cur, conn)

    def buscarPorUsuario(self, usuario: Usuario) -> Empleado:
        """Search employee by user using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM empleado e "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "WHERE e.id_usuario = %s",
            (usuario.id_usuario,)
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

    def buscarEmpleados(self, columna: str, aBuscar: str) -> list[Empleado]:
        """Search employees using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        empleados: list[Empleado] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['nombre', 'direccion', 'telefono', 'id_empleado']
        if columna not in allowed_columns:
            columna = 'nombre'  # default to safe column

        # Use JOIN to avoid N+1 query problem
        cur.execute(
            f"SELECT e.id_empleado, e.nombre, e.direccion, e.telefono, "
            f"u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            f"FROM empleado e "
            f"JOIN usuario u ON e.id_usuario = u.id_usuario "
            f"JOIN rol r ON u.id_rol = r.id_rol "
            f"WHERE CAST(e.{columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        empleados.extend(
            Empleado(
                empleado[0],
                empleado[1],
                empleado[2],
                empleado[3],
                Usuario(empleado[4], empleado[5], empleado[6], Rol(empleado[7], empleado[8]))
            )
            for empleado in resultado
        )
        cerrarConn(cur, conn)

        if empleados:
            return empleados
        else:
            raise TypeError("No existen empleados")