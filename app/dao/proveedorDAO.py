from .DB import DBConnection
from ..utils import cerrarCommit, cerrarConn
from ..model import Proveedor, proveedor
from .empleadoDAO import EmpleadoDAO

class ProveedorDAO:
    def proveedores(self) -> list[Proveedor]:
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
        if proveedores is not None:
            return proveedores
        else:
            raise TypeError("No existen proveedores")

    def proveedor(self, id_proveedor: int) -> Proveedor:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM proveedor WHERE id_proveedor = {id_proveedor}")
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
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM proveedor "
            +"WHERE "
                + f"id_proveedor = {proveedor.id_proveedor}"
        )
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
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO proveedor ("
                + "nombre,"
                + "nombre_contacto,"
                + "telefono,"
                + "direccion,"
                + "activo"
            +") VALUES ("
                + f" '{proveedor.nombre}', "
                + f"'{proveedor.nombre_contacto}',"
                + f" '{proveedor.telefono}',"
                + f"'{proveedor.direccion}',"
                + f"'{proveedor.activo}')"
            )
        cerrarCommit(cur, conn)

    def updateProveedor(self, proveedor: Proveedor):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE proveedor "
            + "SET "
                + f"nombre='{proveedor.nombre}', "
                + f"nombre_contacto='{proveedor.nombre_contacto}', "
                + f"telefono='{proveedor.telefono}', "
                + f"direccion='{proveedor.direccion}', "
                + f"activo={proveedor.activo} "
            +"WHERE "
                + f"id_proveedor={proveedor.id_proveedor}"
            )
        cerrarCommit(cur, conn)

    def deleteProveedor(self, id_proveedor: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            + "FROM "
                + "proveedor "
            +"WHERE "
                + f"id_proveedor={id_proveedor}"
            )
        cerrarCommit(cur, conn)

    def buscarProveedores(self, columna: str, aBuscar: str) -> list[Proveedor]:
        if not aBuscar:
            raise TypeError("falta texto")
        proveedores: list[Proveedor] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * "
            + "FROM proveedor "
            +"WHERE "
                + f"{columna} LIKE '%{aBuscar}%'")
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
        if proveedores is not None:
            return proveedores
        else:
            raise TypeError("No existen proveedores")