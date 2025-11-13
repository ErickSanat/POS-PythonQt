from .DB import DBConnection
from ..model import TipoPago
from ..utils import cerrarConn

class TipoPagoDAO:
    def tiposPago(self) -> list[TipoPago]:
        """Fetch all payment types"""
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
        cerrarConn(cur, conn)
        if tiposPago:
            return tiposPago
        else:
            raise TypeError("No existen tipos de pago")
    
    def tipoPago(self, id_tipo_pago: int) -> TipoPago:
        """Fetch a single payment type by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM tipo_pago WHERE id_tipo_pago = %s", (id_tipo_pago,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return TipoPago(resultado[0], resultado[1])
        else:
            raise TypeError("No existe el tipo de pago")