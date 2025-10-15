from .DB import DBConnection
from ..model import Categoria

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
        return categorias
    
    def categoria(self, id_categoria: int) -> Categoria:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM categoria WHERE id_categoria = {id_categoria}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Categoria(resultado[0], resultado[1], resultado[2])