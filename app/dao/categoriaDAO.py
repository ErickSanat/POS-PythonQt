from .DB import DBConnection
from ..model import Categoria
from ..utils import cerrarConn, cerrarCommit

class CategoriaDAO:
    def categorias(self) -> list[Categoria]:
        """Fetch all categories"""
        categorias: list[Categoria] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM categoria")
        resultado = cur.fetchall()
        categorias.extend(
            Categoria(
                categoria[0],
                categoria[1],
                categoria[2]
            )
            for categoria in resultado
        )
        cerrarConn(cur, conn)
        if categorias:
            return categorias
        else:
            raise TypeError("No existen categorias")
    
    def categoria(self, id_categoria: int) -> Categoria:
        """Fetch a single category by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM categoria WHERE id_categoria = %s", (id_categoria,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Categoria(resultado[0], resultado[1], resultado[2])
        else:
            raise TypeError("No existe la categoria")

    def categoriaExistente(self, categoria: Categoria) -> Categoria | bool:
        """Check if category exists by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM categoria WHERE nombre = %s", (categoria.nombre,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Categoria(
                resultado[0],
                resultado[1],
                resultado[2]
            )
        else:
            return False

    def addCategoria(self, categoria: Categoria):
        """Add a new category using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO categoria (nombre, descripcion) VALUES (%s, %s)",
            (categoria.nombre, categoria.descripcion)
        )
        cerrarCommit(cur, conn)

    def updateCategoria(self, categoria: Categoria):
        """Update a category using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE categoria SET nombre=%s, descripcion=%s WHERE id_categoria=%s",
            (categoria.nombre, categoria.descripcion, categoria.id_categoria)
        )
        cerrarCommit(cur, conn)

    def deleteCategoria(self, id_categoria: int):
        """Delete a category using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM categoria WHERE id_categoria=%s", (id_categoria,))
        cerrarCommit(cur, conn)

    def buscarCategorias(self, columna: str, aBuscar: str) -> list[Categoria]:
        """Search categories using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        categorias: list[Categoria] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['nombre', 'descripcion', 'id_categoria']
        if columna not in allowed_columns:
            columna = 'nombre'  # default to safe column
        
        cur.execute(
            f"SELECT * FROM categoria WHERE CAST({columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        categorias.extend(
            Categoria(
                categoria[0],
                categoria[1],
                categoria[2]
            )
            for categoria in resultado
        )
        cerrarConn(cur, conn)
        if categorias:
            return categorias
        else:
            raise TypeError("No existen categorias")
    
    def porNombre(self, nombre: str) -> Categoria:
        """Get category by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM categoria WHERE nombre = %s", (nombre,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Categoria(resultado[0], resultado[1], resultado[2])
        else:
            raise TypeError("No existe la categoria")