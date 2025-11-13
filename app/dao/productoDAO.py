from .DB import DBConnection
from ..model import Producto, Categoria
from ..utils import cerrarCommit, cerrarConn

class ProductoDAO:
    def productos(self) -> list[Producto]:
        """Fetch all products with their categories in a single query using JOIN"""
        productos: list[Producto] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            "SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM producto p "
            "JOIN categoria c ON p.id_categoria = c.id_categoria"
        )
        resultado = cur.fetchall()
        productos.extend(
            Producto(
                producto[0],  # id_producto
                producto[1],  # nombre
                producto[2],  # descripcion
                producto[3],  # precio
                producto[4],  # stock
                producto[5],  # imagen
                Categoria(producto[6], producto[7], producto[8])  # categoria
            )
            for producto in resultado
        )
        cerrarConn(cur, conn)
        if productos:
            return productos
        else:
            raise TypeError("No existen productos")
    
    def producto(self, id_producto: int) -> Producto:
        """Fetch a single product by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM producto p "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE p.id_producto = %s",
            (id_producto,)
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
                Categoria(resultado[6], resultado[7], resultado[8])
            )
        else:
            raise TypeError("No existe el producto")
    
    def addProducto(self, producto: Producto):
        """Add a new product using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO producto (nombre, descripcion, precio, stock, imagen, id_categoria) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (producto.nombre, producto.descripcion, producto.precio, 
             producto.stock, producto.imagen, producto.categoria.id_categoria)
        )
        cerrarCommit(cur, conn)
    
    def updateProducto(self, producto: Producto):
        """Update a product using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE producto SET nombre=%s, descripcion=%s, precio=%s, stock=%s, "
            "imagen=%s, id_categoria=%s WHERE id_producto=%s",
            (producto.nombre, producto.descripcion, producto.precio, producto.stock,
             producto.imagen, producto.categoria.id_categoria, producto.id_producto)
        )
        cerrarCommit(cur, conn)
    
    def deleteProducto(self, id_producto: int):
        """Delete a product using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM producto WHERE id_producto=%s", (id_producto,))
        cerrarCommit(cur, conn)
        
    def buscarProductos(self, columna: str, aBuscar: str) -> list[Producto]:
        """Search products using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        productos: list[Producto] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation
        allowed_columns = ['nombre', 'descripcion', 'precio', 'stock', 'id_producto']
        if columna not in allowed_columns:
            columna = 'nombre'  # default to safe column
        
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            f"SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            f"c.id_categoria, c.nombre, c.descripcion "
            f"FROM producto p "
            f"JOIN categoria c ON p.id_categoria = c.id_categoria "
            f"WHERE CAST(p.{columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        productos.extend(
            Producto(
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4],
                producto[5],
                Categoria(producto[6], producto[7], producto[8])
            )
            for producto in resultado
        )
        cerrarConn(cur, conn)
        if productos:
            return productos
        else:
            raise TypeError("No existen productos")
    
    def productoExistente(self, producto: Producto) -> Producto | bool:
        """Check if a product exists by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM producto p "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE p.nombre = %s",
            (producto.nombre,)
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
                Categoria(resultado[6], resultado[7], resultado[8])
            )
        else:
            return False

    def porNombre(self, nombre: str) -> Producto:
        """Get product by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM producto p "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE p.nombre = %s",
            (nombre,)
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
                Categoria(resultado[6], resultado[7], resultado[8])
            )
        else:
            raise TypeError("No existe el producto")