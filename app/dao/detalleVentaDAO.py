from .DB import DBConnection
from ..model import DetalleVenta, Venta
from ..utils import cerrarConn, cerrarCommit
from ..dao import VentaDAO, ProductoDAO

class DetalleVentaDAO:
    def detalleVentas(self) -> list[DetalleVenta]:
        detalleVentas: list[DetalleVenta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detalle_venta")
        resultado = cur.fetchall()
        detalleVentas.extend(
            DetalleVenta(
                detalleVenta[0],
                VentaDAO().venta(detalleVenta[1]),
                ProductoDAO().producto(detalleVenta[2]),
                detalleVenta[3],
                detalleVenta[4]
                )
                for detalleVenta in resultado
            )
        cerrarConn(cur, conn)
        if detalleVentas is not None:
            return detalleVentas
        else:
            raise TypeError("No existen detalles")
    
    def detalleVenta(self, id_detalle: int) -> DetalleVenta:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM detalle_venta WHERE id_detalle = {id_detalle}")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return DetalleVenta(
                resultado[0],
                VentaDAO().venta(resultado[1]),
                ProductoDAO().producto(resultado[2]),
                resultado[3],
                resultado[4]
            )
        else:
            raise TypeError("No existe el detalle")

    def detalleVentaExistente(self, detalleVenta: DetalleVenta) -> DetalleVenta | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM detalle_venta "
            +"WHERE "
                + f"id_detalle = {detalleVenta.id_detalle}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return DetalleVenta(
                resultado[0],
                VentaDAO().venta(resultado[1]),
                ProductoDAO().producto(resultado[2]),
                resultado[3],
                resultado[4]
            )
        else:
            return False

    def addDetalleVenta(self, detalleVenta: DetalleVenta):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO detalle_venta ("
                + "id_venta,"
                + "id_producto,"
                + "cantidad,"
                + "subtotal"
            +") VALUES ("
                + f" '{detalleVenta.venta.id_venta}', "
                + f"'{detalleVenta.producto.id_producto}',"
                + f" '{detalleVenta.cantidad}',"
                + f"'{detalleVenta.subtotal}')"
            )
        cerrarCommit(cur, conn)

    def updateDetalleVenta(self, detalleVenta: DetalleVenta):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE detalle_venta "
            + "SET "
                + f"id_venta='{detalleVenta.venta.id_venta}', "
                + f"id_producto='{detalleVenta.producto.id_producto}', "
                + f"cantidad='{detalleVenta.cantidad}', "
                + f"subtotal={detalleVenta.subtotal} "
            +"WHERE "
                + f"id_detalle_venta={detalleVenta.id_detalle}"
            )
        cerrarCommit(cur, conn)

    def deleteDetalleVenta(self, id_detalleVenta: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            + "FROM "
                + "detalle_venta "
            +"WHERE "
                + f"id_detalle_venta={id_detalleVenta}"
            )
        cerrarCommit(cur, conn)

    def buscarDetalleVentas(self, columna: str, aBuscar: str) -> list[DetalleVenta]:
        if not aBuscar:
            raise TypeError("falta texto")
        detalleVentaes: list[DetalleVenta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * "
            + "FROM detalle_venta "
            +"JOIN venta "
            +"ON detalle_venta.id_venta = venta.id_venta "
            +"JOIN producto "
            +"ON detalle_venta.id_producto = producto.id_producto "
            + f"WHERE CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
        resultado = cur.fetchall()
        detalleVentaes.extend(
            DetalleVenta(
                detalleVenta[0],
                VentaDAO().venta(detalleVenta[1]),
                ProductoDAO().producto(detalleVenta[2]),
                detalleVenta[3],
                detalleVenta[4]
            )
            for detalleVenta in resultado
        )
        cerrarConn(cur, conn)
        if detalleVentaes is not None:
            return detalleVentaes
        else:
            raise TypeError("No existen detalleVentaes")

    def buscarPorVenta(self, venta: Venta) -> DetalleVenta:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM detalle_venta "
            + f"WHERE id_venta = {venta.id_venta}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return DetalleVenta(
                resultado[0],
                venta,
                ProductoDAO().producto(resultado[2]),
                resultado[3],
                resultado[4]
            )
        else:
            raise TypeError("No existe el empleado")