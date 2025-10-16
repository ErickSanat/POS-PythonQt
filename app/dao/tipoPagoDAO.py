from .DB import DBConnection
from ..model import TipoPago

class TipoPagoDAO:
    def tiposPago(self) -> list[TipoPago]:
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
        if tiposPago is not None:
            return tiposPago
        else:
            raise TypeError("No existen tipos de pago")
    
    def tipoPago(self, id_tipo_pago: int) -> TipoPago:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM tipo_pago WHERE id_tipo_pago = {id_tipo_pago}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return TipoPago(resultado[0], resultado[1])
        else:
            raise TypeError("No existe el tipo de pago")