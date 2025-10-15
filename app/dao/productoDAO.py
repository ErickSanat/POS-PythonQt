from .DB import DBConnection
from ..model import Producto 
from .categoriaDAO import CategoriaDAO

class ProductoDAO:
    def productos(self) -> list[Producto]:
        productos: list[Producto] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM producto")
        resultado = cur.fetchall()
        productos.extend(
            Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                CategoriaDAO().categoria(producto[5])
                )
                for producto in resultado
            )
        cur.close()
        conn.close()
        return productos
    
    def producto(self, id_producto: int) -> Producto:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM producto WHERE id_producto = {id_producto}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Producto(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                resultado[4],
                CategoriaDAO().categoria(resultado[5])
            )