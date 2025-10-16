from .DB import DBConnection
from ..model import Pago
from .ventaDAO import VentaDAO
from .tipoPagoDAO import TipoPagoDAO

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
                VentaDAO().venta(pago[1]),
                TipoPagoDAO().tipoPago(pago[2]),
                pago[3]
                )
                for pago in resultado
            )
        cur.close()
        conn.close()
        if pagos is not None:
            return pagos
        else:
            raise TypeError("No existen pagos")
    
    def pago(self, id_pago: int) -> Pago:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM pago WHERE id_pago = {id_pago}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return Pago(
                resultado[0],
                VentaDAO().venta(resultado[1]),
                TipoPagoDAO().tipoPago(resultado[2]),
                resultado[3]
            )
        else:
            raise TypeError("No existe el pago")