from .DB import DBConnection
from ..model import Promocion

class PromocionDAO:
    @staticmethod
    def promociones() -> list[Promocion]:
        promociones: list[Promocion] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM promocion")
        resultado = cur.fetchall()
        promociones.extend(
            Promocion(
                promocion[0],
                promocion[1],
                promocion[2]
                )
                for promocion in resultado
            )
        cur.close()
        conn.close()
        return promociones
    
    @staticmethod
    def promocion(id_promocion: int) -> Promocion:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM promocion WHERE id_promocion = {id_promocion}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Promocion(resultado[0], resultado[1], resultado[2])