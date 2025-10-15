from .DB import DBConnection
from ..model import DetallePromocion
from .productoDAO import ProductoDAO

class DetallePromocionDAO:
    @staticmethod
    def detallesPromocion() -> list[DetallePromocion]:
        detallesPromocion: list[DetallePromocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detalle_promocion")
        resultado = cur.fetchall()
        detallesPromocion.extend(
            DetallePromocion(
                detallePromocion[0],
                detallePromocion[1],
                ProductoDAO.producto(detallePromocion[2])
                )
                for detallePromocion in resultado
            )
        cur.close()
        conn.close()
        return detallesPromocion
    
    @staticmethod
    def detallePromocion(id_detalle_promocion: int) -> DetallePromocion:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM detalle_promocion WHERE id_detalle_promocion = {id_detalle_promocion}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return DetallePromocion(
                resultado[0],
                resultado[1],
                ProductoDAO.producto(resultado[2])
            )