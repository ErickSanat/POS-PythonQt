from .DB import DBConnection
from ..model import Caja
from .usuarioDAO import UsuarioDAO

class CajaDAO:
    @staticmethod
    def cajas() -> list[Caja]:
        cajas: list[Caja] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM caja")
        resultado = cur.fetchall()
        cajas.extend(
            Caja(
                caja[0],
                caja[1],
                caja[2],
                caja[3],
                caja[4],
                caja[5],
                UsuarioDAO.usuario(caja[6])
                )
                for caja in resultado
            )
        cur.close()
        conn.close()
        return cajas
    
    @staticmethod
    def caja(id_caja: int) -> Caja:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM caja WHERE id_caja = {id_caja}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Caja(resultado[0],
                    resultado[1],
                    resultado[2],
                    resultado[3],
                    resultado[4],
                    resultado[5],
                    UsuarioDAO.usuario(resultado[6])
                    )