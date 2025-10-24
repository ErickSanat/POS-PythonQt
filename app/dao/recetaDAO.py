from .DB import DBConnection
from ..model import Receta, receta
from .productoDAO import ProductoDAO
from ..utils import cerrarCommit, cerrarConn


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
        if recetas is not None:
            return recetas
        else:
            raise TypeError("No existen recetas")
    
    def receta(self, id_receta: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM receta WHERE id_receta = {id_receta}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return Receta(
                resultado[0],
                ProductoDAO().producto(resultado[1]),
                resultado[2],
                resultado[3]
            )
        else:
            raise TypeError("No existe la receta")

    def recetaExistente(self, receta: Receta) -> Receta | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM receta WHERE id_receta = {receta.id_receta}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return Receta(
                resultado[0],
                ProductoDAO().producto(resultado[1]),
                resultado[2],
                resultado[3]
            )
        else:
            return False

    def addReceta(self, receta: Receta):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO receta ("
                + "id_producto,"
                + "descripcion,"
                + "instrucciones"
                + " VALUES ("
                    + f"{receta.producto.id_producto},"
                    + f"'{receta.descripcion}',"
                    + f"'{receta.instrucciones}')"
            )
        conn.commit()

    def updateReceta(self, receta: Receta):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE receta "
            + "SET "
                + f"descripcion='{receta.descripcion}', "
                + f"instrucciones='{receta.instrucciones}'"
            +"WHERE "
                + f"id_receta={receta.id_receta}"
        )
        cerrarCommit(cur, conn)

    def deleteReceta(self, id_receta: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            +"FROM "
                + "receta "
            +"WHERE "
                + f"id_receta={id_receta}"
            )
        cerrarCommit(cur, conn)

    def buscarRecetas(self, columna: str, aBuscar: str) -> list[Receta]:
        if not aBuscar:
            raise TypeError("falta texto")
        recetas: list[Receta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * "
            + "FROM receta "
            + "WHERE "
                + f"CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
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
        cerrarCommit(cur, conn)
        if recetas is not None:
            return recetas
        else:
            raise TypeError("No existen recetas")

    def recetaPorProducto(self, id_producto: int) -> Receta:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * "
            + "FROM receta "
            + "WHERE "
                + f"id_producto={id_producto}"
        )
        resultado = cur.fetchone()
        cerrarCommit(cur, conn)
        if resultado is not None:
            return Receta(
                resultado[0],
                ProductoDAO().producto(resultado[1]),
                resultado[2],
                resultado[3]
            )
        else:
            raise TypeError("No existe la receta")