from .DB import DBConnection
from ..model import Categoria
from ..utils import cerrarConn, cerrarCommit

class CategoriaDAO:
    def categorias(self) -> list[Categoria]:
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
        cur.close()
        conn.close()
        if categorias is not None:
            return categorias
        else:
            raise TypeError("No existen categorias")
    
    def categoria(self, id_categoria: int) -> Categoria:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM categoria WHERE id_categoria = {id_categoria}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return Categoria(resultado[0], resultado[1], resultado[2])
        else:
            raise TypeError("No existe la categoria")

    def categoriaExistente(self, categoria: Categoria) -> Categoria | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM categoria WHERE nombre = '{categoria.nombre}'")
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
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO categoria ("
                + "nombre,"
                + "descripcion"
            +") VALUES ("
                + f"'{categoria.nombre}',"
                + f"'{categoria.descripcion}')"
        )
        cerrarCommit(cur, conn)

    def updateCategoria(self, categoria: Categoria):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE categoria "
            +"SET "
                + f"nombre='{categoria.nombre}',"
                + f"descripcion='{categoria.descripcion}'"
            +"WHERE "
                + f"id_categoria={categoria.id_categoria}"
        )
        cerrarCommit(cur, conn)

    def deleteCategoria(self, id_categoria: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            +"FROM "
                + "categoria "
            +"WHERE "
                + f"id_categoria={id_categoria}"
            )
        cerrarCommit(cur, conn)

    def buscarCategorias(self, columna: str, aBuscar: str) -> list[Categoria]:
        if not aBuscar:
            raise TypeError("falta texto")
        categorias: list[Categoria] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * "
            + "FROM categoria "
            + "WHERE "
                + f"CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
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
        if categorias is not None:
            return categorias
        else:
            raise TypeError("No existen categorias")
    
    def porNombre(self, nombre: str) -> Categoria:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM categoria WHERE nombre = '{nombre}'")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Categoria(resultado[0], resultado[1], resultado[2])
        else:
            raise TypeError("No existe la categoria")