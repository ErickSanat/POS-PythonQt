from .DB import DBConnection
from ..utils import cerrarCommit, cerrarConn
from ..model import Proveedor

class ProveedorDAO:
    def proveedores(self) -> list[Proveedor]:
        """Fetch all suppliers"""
        proveedores: list[Proveedor] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM proveedor")
        resultado = cur.fetchall()
        proveedores.extend(
            Proveedor(
                proveedor[0],
                proveedor[1],
                proveedor[2],
                proveedor[3],
                proveedor[4],
                proveedor[5],
            )
            for proveedor in resultado
        )
        cerrarConn(cur, conn)
        if proveedores:
            return proveedores
        else:
            raise TypeError("No existen proveedores")

    def proveedor(self, id_proveedor: int) -> Proveedor:
        """Fetch a single supplier by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Proveedor(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                resultado[4],
                resultado[5],
            )
        else:
            raise TypeError("No existe el proveedor")

    def proveedorExistente(self, proveedor: Proveedor) -> Proveedor | bool:
        """Check if supplier exists by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM proveedor WHERE id_proveedor = %s", (proveedor.id_proveedor,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Proveedor(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                resultado[4],
                resultado[5],
            )
        else:
            return False

    def addProveedor(self, proveedor: Proveedor):
        """Add a new supplier using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO proveedor (nombre, nombre_contacto, telefono, direccion, activo) "
            "VALUES (%s, %s, %s, %s, %s)",
            (proveedor.nombre, proveedor.nombre_contacto, proveedor.telefono,
             proveedor.direccion, proveedor.activo)
        )
        cerrarCommit(cur, conn)

    def updateProveedor(self, proveedor: Proveedor):
        """Update a supplier using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE proveedor SET nombre=%s, nombre_contacto=%s, telefono=%s, "
            "direccion=%s, activo=%s WHERE id_proveedor=%s",
            (proveedor.nombre, proveedor.nombre_contacto, proveedor.telefono,
             proveedor.direccion, proveedor.activo, proveedor.id_proveedor)
        )
        cerrarCommit(cur, conn)

    def deleteProveedor(self, id_proveedor: int):
        """Delete a supplier using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM proveedor WHERE id_proveedor=%s", (id_proveedor,))
        cerrarCommit(cur, conn)

    def buscarProveedores(self, columna: str, aBuscar: str) -> list[Proveedor]:
        """Search suppliers using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        proveedores: list[Proveedor] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['nombre', 'nombre_contacto', 'telefono', 'direccion', 'id_proveedor']
        if columna not in allowed_columns:
            columna = 'nombre'  # default to safe column
        
        cur.execute(
            f"SELECT * FROM proveedor WHERE CAST({columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        proveedores.extend(
            Proveedor(
                proveedor[0],
                proveedor[1],
                proveedor[2],
                proveedor[3],
                proveedor[4],
                proveedor[5]
            )
            for proveedor in resultado
        )
        cerrarConn(cur, conn)
        if proveedores:
            return proveedores
        else:
            raise TypeError("No existe el proveedor")
