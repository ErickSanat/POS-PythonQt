from .DB import DBConnection
from ..model import Promocion, promocion
from ..utils import cerrarConn, cerrarCommit


class PromocionDAO:
    def promociones(self) -> list[Promocion]:
        promociones: list[Promocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM promocion")
        resultado = cur.fetchall()
        promociones.extend(
            Promocion(
                promocion[0],
                promocion[1],
                promocion[2],
                promocion[3]
                )
                for promocion in resultado
            )
        cur.close()
        conn.close()
        if promociones is not None:
            return promociones
        else:
            raise TypeError("No existen promociones")
    
    def promocion(self, id_promocion: int) -> Promocion:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM promocion WHERE id_promocion = {id_promocion}")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Promocion(resultado[0], resultado[1], resultado[2])
        else:
            return None

    def promocionExistente(self, promocion: Promocion) -> Promocion | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM promocion "
            +"WHERE "
                + f"nombre = '{promocion.nombre}'"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Promocion(resultado[0], resultado[1], resultado[2])
        else:
            return False

    def addPromocion(self, promocion: Promocion):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO promocion ("
                + "nombre,"
                + "porcentaje,"
                + "descripcion"
                +") VALUES ("
                    + f"'{promocion.nombre}',"
                    + f"{promocion.porcentaje},"
                    + f"'{promocion.descripcion}')"
            )
        cerrarCommit(cur, conn)

    def updatePromocion(self, promocion: Promocion):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE promocion "
            +"SET "
                + f"nombre='{promocion.nombre}',"
                + f"porcentaje={promocion.porcentaje},"
                + f"descripcion='{promocion.descripcion}'"
            +"WHERE "
                + f"id_promocion = {promocion.id_promocion}"
        )
        cerrarCommit(cur, conn)

    def deletePromocion(self, id_promocion: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            +"FROM promocion "
            +"WHERE "
            + f"id_promocion={id_promocion}"
        )
        cerrarCommit(cur, conn)

    def buscarPromociones(self, columna: str, aBuscar: str) -> list[Promocion]:
        if not aBuscar:
            raise TypeError("falta texto")
        promociones: list[Promocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM promocion "
            +"WHERE "
            + f"CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
        resultado = cur.fetchall()
        promociones.extend(
            Promocion(
                promocion[0],
                promocion[1],
                promocion[2],
                promocion[3]
            )
            for promocion in resultado
        )
        cerrarCommit(cur, conn)
        if promociones is not None:
            return promociones
        else:
            raise TypeError("No existen promociones")