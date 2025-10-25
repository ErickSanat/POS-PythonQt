from .DB import DBConnection
from ..model import Producto
from ..utils import cerrarCommit, cerrarConn
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
                producto[5],
                CategoriaDAO().categoria(producto[6])
                )
                for producto in resultado
            )
        cur.close()
        conn.close()
        if productos is not None:
            return productos
        else:
            raise TypeError("No existen productos")
    
    def producto(self, id_producto: int) -> Producto:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM producto WHERE id_producto = {id_producto}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return Producto(
                    resultado[0],
                    resultado[1],
                    resultado[2],
                    resultado[3],
                    resultado[4],
                    resultado[5],
                    CategoriaDAO().categoria(resultado[6])
                )
        else:
            raise TypeError("No existe el producto")
    
    def addProducto(self, producto: Producto):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO producto ("
                + "nombre,"
                + "descripcion,"
                + "precio,"
                + "stock,"
                + "imagen,"
                + "id_categoria"
            +") VALUES ("
                + f"'{producto.nombre}',"
                + f"'{producto.descripcion}',"
                + f"{producto.precio},"
                + f"{producto.stock},"
                + f"'{producto.imagen}',"
                + f"{producto.categoria.id_categoria})"
            )
        conn.commit()
        cur.close()
        conn.close()
    
    def updateProducto(self, producto: Producto):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE producto "
            + "SET "
                + f"nombre='{producto.nombre}', "
                + f"descripcion='{producto.descripcion}', "
                + f"precio={producto.precio}, "
                + f"stock={producto.stock}, "
                + f"imagen='{producto.imagen}', "
                + f"id_categoria={producto.categoria.id_categoria} "
            +"WHERE "
                + f"id_producto={producto.id_producto}"
            )
        cerrarCommit(cur, conn)
    
    def deleteProducto(self, id_producto: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            + "FROM "
                + "producto "
            +"WHERE "
                + f"id_producto={id_producto}"
            )
        cerrarCommit(cur, conn)
    def buscarProductos(self, columna: str, aBuscar: str) -> list[Producto]:
        if not aBuscar:
            raise TypeError("falta texto")
        productos: list[Producto] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * "
            + "FROM producto "
            + "JOIN categoria "
            + "ON producto.id_categoria = categoria.id_categoria "
            + f"WHERE CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
        resultado = cur.fetchall()
        productos.extend(
            Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                CategoriaDAO().categoria(producto[6])
                )
                for producto in resultado
            )
        cerrarConn(cur, conn)
        if productos is not None:
            return productos
        else:
            raise TypeError("No existen productos")
    
    def productoExistente(self, producto: Producto) -> Producto | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM producto "
            +"WHERE "
                + f"nombre = '{producto.nombre}'"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Producto(
                resultado[0],
                resultado[1],
                resultado[2],
                resultado[3],
                resultado[4],
                resultado[5],
                CategoriaDAO().categoria(resultado[6])
            )
        else:
            return False