from .DB import DBConnection
from ..model import Pago
from .tipoPagoDAO import TipoPagoDAO
from ..utils import cerrarConn, cerrarCommit


class PagoDAO:
    def pagos(self) -> list[Pago]:
        pagos: list[Pago] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pago")
        resultado = cur.fetchall()
        pagos.extend(
            Pago(
                pago[0],
                TipoPagoDAO().tipoPago(pago[1]),
                pago[2]
            )
            for pago in resultado
        )
        cerrarConn(cur, conn)


    def pago(self, id_pago: int) -> Pago:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM pago WHERE id_pago = {id_pago}")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Pago(
                resultado[0],
                TipoPagoDAO().tipoPago(resultado[1]),
                resultado[2]
            )
        else:
            raise TypeError("No existe el pago")

    def addPago(self, pago: Pago):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pago ("
                + "id_tipo_pago,"
                + "cantidad"
            +") VALUES ("
                + f"'{pago.tipo_pago.id_tipo_pago}',"
                + f"{pago.cantidad})"
            )
        cerrarCommit(cur, conn)

    def ultimoPago(self) -> Pago:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pago ORDER BY id_pago DESC LIMIT 1")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Pago(
                resultado[0],
                TipoPagoDAO().tipoPago(resultado[1]),
                resultado[2]
            )
        else:
            raise TypeError("No existe el pago")