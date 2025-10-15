from .DB import DBConnection
from ..model import DetalleVenta
from .ventaDAO import VentaDAO
from .productoDAO import ProductoDAO

class DetalleVentaDAO:
    @staticmethod
    def detallesVenta() -> list[DetalleVenta]:
        detalleVentas: list[DetalleVenta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detalle_venta")
        resultado = cur.fetchall()
        detalleVentas.extend(
            DetalleVenta(
                detalleVenta[0],
                VentaDAO.venta(detalleVenta[1]),
                ProductoDAO.producto(detalleVenta[2]),
                detalleVenta[3],
                detalleVenta[4]
                )
                for detalleVenta in resultado
            )
        cur.close()
        conn.close()
        return detalleVentas
    
    @staticmethod
    def detalleVenta(id_detalle: int) -> DetalleVenta:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM detalle_venta WHERE id_detalle = {id_detalle}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return DetalleVenta(
                resultado[0],
                VentaDAO.venta(resultado[1]),
                ProductoDAO.producto(resultado[2]),
                resultado[3],
                resultado[4]
            )