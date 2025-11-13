from .DB import DBConnection
from ..model import DetallePromocion, Producto, Categoria
from ..utils import cerrarConn

class DetallePromocionDAO:
    def detallesPromocion(self) -> list[DetallePromocion]:
        """Fetch all promotion details with products and categories in a single query using JOIN"""
        detallesPromocion: list[DetallePromocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            "SELECT dp.id_detalle_promocion, dp.id_promocion, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM detalle_promocion dp "
            "JOIN producto p ON dp.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria"
        )
        resultado = cur.fetchall()
        detallesPromocion.extend(
            DetallePromocion(
                detallePromocion[0],  # id_detalle_promocion
                detallePromocion[1],  # id_promocion
                Producto(
                    detallePromocion[2], detallePromocion[3], detallePromocion[4],
                    detallePromocion[5], detallePromocion[6], detallePromocion[7],
                    Categoria(detallePromocion[8], detallePromocion[9], detallePromocion[10])
                )
            )
            for detallePromocion in resultado
        )
        cerrarConn(cur, conn)
        if detallesPromocion:
            return detallesPromocion
        else:
            raise TypeError("No existen detalles")
    
    def detallePromocion(self, id_detalle_promocion: int) -> DetallePromocion:
        """Fetch a single promotion detail by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection and JOIN to avoid extra queries
        cur.execute(
            "SELECT dp.id_detalle_promocion, dp.id_promocion, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM detalle_promocion dp "
            "JOIN producto p ON dp.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE dp.id_detalle_promocion = %s",
            (id_detalle_promocion,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return DetallePromocion(
                resultado[0],
                resultado[1],
                Producto(
                    resultado[2], resultado[3], resultado[4],
                    resultado[5], resultado[6], resultado[7],
                    Categoria(resultado[8], resultado[9], resultado[10])
                )
            )
        else:
            raise TypeError("No existe el detalle")