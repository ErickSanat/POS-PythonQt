from .DB import DBConnection
from ..model import TipoPago

class TipoPagoDAO:
    @staticmethod
    def tiposPago() -> list[TipoPago]:
        tiposPago: list[TipoPago] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tipo_pago")
        resultado = cur.fetchall()
        tiposPago.extend(
            TipoPago(
                tipoPago[0],
                tipoPago[1]
                )
                for tipoPago in resultado
            )
        cur.close()
        conn.close()
        return tiposPago
    
    @staticmethod
    def tipoPago(id_tipo_pago: int) -> TipoPago:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM tipo_pago WHERE id_tipo_pago = {id_tipo_pago}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return TipoPago(resultado[0], resultado[1])