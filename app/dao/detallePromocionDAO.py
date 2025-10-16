from .DB import DBConnection
from ..model import DetallePromocion
from .productoDAO import ProductoDAO

class DetallePromocionDAO:
    def detallesPromocion(self) -> list[DetallePromocion]:
        detallesPromocion: list[DetallePromocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detalle_promocion")
        resultado = cur.fetchall()
        detallesPromocion.extend(
            DetallePromocion(
                detallePromocion[0],
                detallePromocion[1],
                ProductoDAO().producto(detallePromocion[2])
                )
                for detallePromocion in resultado
            )
        cur.close()
        conn.close()
        if detallesPromocion is not None:
            return detallesPromocion
        else:
            raise TypeError("No existen detalles")
    
    def detallePromocion(self,id_detalle_promocion: int) -> DetallePromocion:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM detalle_promocion WHERE id_detalle_promocion = {id_detalle_promocion}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return DetallePromocion(
                resultado[0],
                resultado[1],
                ProductoDAO().producto(resultado[2])
            )
        else:
            raise TypeError("No existe el detalle")