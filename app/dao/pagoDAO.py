from .DB import DBConnection
from ..model import Pago, TipoPago
from ..utils import cerrarConn, cerrarCommit


class PagoDAO:
    def pagos(self) -> list[Pago]:
        """Fetch all payments with their types in a single query using JOIN"""
        pagos: list[Pago] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            "SELECT p.id_pago, p.cantidad, t.id_tipo_pago, t.nombre "
            "FROM pago p "
            "JOIN tipo_pago t ON p.id_tipo_pago = t.id_tipo_pago"
        )
        resultado = cur.fetchall()
        pagos.extend(
            Pago(
                pago[0],  # id_pago
                TipoPago(pago[2], pago[3]),  # tipo_pago
                pago[1]  # cantidad
            )
            for pago in resultado
        )
        cerrarConn(cur, conn)
        return pagos


    def pago(self, id_pago: int) -> Pago:
        """Fetch a single payment by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection and JOIN to avoid extra query
        cur.execute(
            "SELECT p.id_pago, p.cantidad, t.id_tipo_pago, t.nombre "
            "FROM pago p "
            "JOIN tipo_pago t ON p.id_tipo_pago = t.id_tipo_pago "
            "WHERE p.id_pago = %s",
            (id_pago,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Pago(
                resultado[0],
                TipoPago(resultado[2], resultado[3]),
                resultado[1]
            )
        else:
            raise TypeError("No existe el pago")

    def addPago(self, pago: Pago):
        """Add a new payment using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO pago (id_tipo_pago, cantidad) VALUES (%s, %s)",
            (pago.tipo_pago.id_tipo_pago, pago.cantidad)
        )
        cerrarCommit(cur, conn)

    def ultimoPago(self) -> Pago:
        """Fetch the most recent payment"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            "SELECT p.id_pago, p.cantidad, t.id_tipo_pago, t.nombre "
            "FROM pago p "
            "JOIN tipo_pago t ON p.id_tipo_pago = t.id_tipo_pago "
            "ORDER BY p.id_pago DESC LIMIT 1"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Pago(
                resultado[0],
                TipoPago(resultado[2], resultado[3]),
                resultado[1]
            )
        else:
            raise TypeError("No existe el pago")