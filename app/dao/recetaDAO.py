from .DB import DBConnection
from ..model import Receta, Producto, Categoria
from ..utils import cerrarCommit, cerrarConn


class RecetaDAO:
    def recetas(self):
        """Fetch all recipes with products and categories in a single query using JOIN"""
        recetas: list[Receta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            "SELECT r.id_receta, r.descripcion, r.instrucciones, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM receta r "
            "JOIN producto p ON r.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria"
        )
        resultado = cur.fetchall()
        recetas.extend(
            Receta(
                receta[0],  # id_receta
                Producto(
                    receta[3], receta[4], receta[5], receta[6], receta[7], receta[8],
                    Categoria(receta[9], receta[10], receta[11])
                ),
                receta[1],  # descripcion
                receta[2]   # instrucciones
            )
            for receta in resultado
        )
        cerrarConn(cur, conn)
        if recetas:
            return recetas
        else:
            raise TypeError("No existen recetas")
    
    def receta(self, id_receta: int):
        """Fetch a single recipe by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection and JOIN to avoid extra queries
        cur.execute(
            "SELECT r.id_receta, r.descripcion, r.instrucciones, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM receta r "
            "JOIN producto p ON r.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE r.id_receta = %s",
            (id_receta,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Receta(
                resultado[0],
                Producto(
                    resultado[3], resultado[4], resultado[5], resultado[6],
                    resultado[7], resultado[8],
                    Categoria(resultado[9], resultado[10], resultado[11])
                ),
                resultado[1],
                resultado[2]
            )
        else:
            raise TypeError("No existe la receta")

    def recetaExistente(self, receta: Receta) -> Receta | bool:
        """Check if recipe exists by product ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT r.id_receta, r.descripcion, r.instrucciones, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM receta r "
            "JOIN producto p ON r.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE r.id_producto = %s",
            (receta.producto.id_producto,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Receta(
                resultado[0],
                Producto(
                    resultado[3], resultado[4], resultado[5], resultado[6],
                    resultado[7], resultado[8],
                    Categoria(resultado[9], resultado[10], resultado[11])
                ),
                resultado[1],
                resultado[2]
            )
        else:
            return False

    def addReceta(self, receta: Receta):
        """Add a new recipe using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO receta (id_producto, descripcion, instrucciones) VALUES (%s, %s, %s)",
            (receta.producto.id_producto, receta.descripcion, receta.instrucciones)
        )
        cerrarCommit(cur, conn)

    def updateReceta(self, receta: Receta):
        """Update a recipe using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE receta SET id_producto=%s, descripcion=%s, instrucciones=%s WHERE id_receta=%s",
            (receta.producto.id_producto, receta.descripcion, receta.instrucciones, receta.id_receta)
        )
        cerrarCommit(cur, conn)

    def deleteReceta(self, id_receta: int):
        """Delete a recipe using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM receta WHERE id_receta=%s", (id_receta,))
        cerrarCommit(cur, conn)

    def buscarRecetas(self, columna: str, aBuscar: str) -> list[Receta]:
        """Search recipes using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        recetas: list[Receta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['descripcion', 'instrucciones', 'id_receta']
        if columna not in allowed_columns:
            columna = 'descripcion'  # default to safe column
        
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            f"SELECT r.id_receta, r.descripcion, r.instrucciones, "
            f"p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            f"c.id_categoria, c.nombre, c.descripcion "
            f"FROM receta r "
            f"JOIN producto p ON r.id_producto = p.id_producto "
            f"JOIN categoria c ON p.id_categoria = c.id_categoria "
            f"WHERE CAST(r.{columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        recetas.extend(
            Receta(
                receta[0],
                Producto(
                    receta[3], receta[4], receta[5], receta[6], receta[7], receta[8],
                    Categoria(receta[9], receta[10], receta[11])
                ),
                receta[1],
                receta[2]
            )
            for receta in resultado
        )
        cerrarConn(cur, conn)
        if recetas:
            return recetas
        else:
            raise TypeError("No existen recetas")

    def recetaPorProducto(self, id_producto: int) -> Receta:
        """Get recipe by product ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT r.id_receta, r.descripcion, r.instrucciones, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM receta r "
            "JOIN producto p ON r.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE r.id_producto = %s",
            (id_producto,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Receta(
                resultado[0],
                Producto(
                    resultado[3], resultado[4], resultado[5], resultado[6],
                    resultado[7], resultado[8],
                    Categoria(resultado[9], resultado[10], resultado[11])
                ),
                resultado[1],
                resultado[2]
            )
        else:
            raise TypeError("No existe la receta")