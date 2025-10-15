from .DB import DBConnection
from ..model import Receta
from .productoDAO import ProductoDAO

class RecetaDAO:
    def recetas(self):
        recetas: list[Receta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM receta")
        resultado = cur.fetchall()
        recetas.extend(
            Receta(
                receta[0],
                ProductoDAO().producto(receta[1]),
                receta[2],
                receta[3]
                )
                for receta in resultado
            )
        cur.close()
        conn.close()
        return recetas
    
    def receta(self, id_receta: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM receta WHERE id_receta = {id_receta}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Receta(
            resultado[0],
            ProductoDAO().producto(resultado[1]),
            resultado[2],
            resultado[3]
        )