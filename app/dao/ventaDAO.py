from .DB import DBConnection
from ..utils import cerrarConn, cerrarCommit
from ..model import Venta, Empleado, Cliente, Promocion, Pago
from .empleadoDAO import EmpleadoDAO
from .clienteDAO import ClienteDAO
from .promocionDAO import PromocionDAO
from .pagoDAO import PagoDAO

class VentaDAO:
    def ventas(self) -> list[Venta]:
        ventas: list[Venta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM venta")
        resultado = cur.fetchall()
        ventas.extend(
            Venta(
                venta[0],
                venta[1],
                EmpleadoDAO().empleado(venta[2]),
                ClienteDAO().cliente(venta[3]),
                PromocionDAO().promocion(venta[4]),
                PagoDAO().pago(venta[5]),
                venta[6]
                )
                for venta in resultado
            )
        cerrarConn(cur, conn)
        if ventas is not None:
            return ventas
        else:
            raise TypeError("No existen ventas")
    
    def venta(self, id_venta: int) -> Venta:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM venta WHERE id_venta = {id_venta}")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                EmpleadoDAO().empleado(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                PromocionDAO().promocion(resultado[4]),
                PagoDAO().pago(resultado[5]),
                resultado[6]
            )
        else:
            raise TypeError("No existe la venta")

    def addVenta(self, venta: Venta):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO venta ("
                + "fecha,"
                + "id_empleado,"
                + "id_cliente,"
                + "id_promocion,"
                + "id_pago,"
                + "total"
            +") VALUES ("
                + f"'{venta.fecha}',"
                + f"'{venta.empleado.id_empleado}',"
                + f"'{venta.cliente.id_cliente}',"
                + f"'{venta.promocion.id_promocion}',"
                + f"'{venta.pago.id_pago}',"
                + f"{venta.total})"
            )
        cerrarCommit(cur, conn)

    def ultimaVenta(self) -> Venta:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM venta ORDER BY id_venta DESC LIMIT 1")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                EmpleadoDAO().empleado(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                PromocionDAO().promocion(resultado[4]),
                PagoDAO().pago(resultado[5]),
                resultado[6]
            )
        else:
            raise TypeError("No existe el pago")
    def ventaExistente(self, venta: Venta) -> Venta | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM venta "
            +"WHERE "
                + f"id_venta = {venta.id_venta}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                EmpleadoDAO().empleado(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                PromocionDAO().promocion(resultado[4]),
                PagoDAO().pago(resultado[5]),
                resultado[6]
            )
        else:
            return False

    def buscarVentas(self, columna: str, aBuscar: str) -> list[Venta]:
        if not aBuscar:
            raise TypeError("falta texto")
        ventas: list[Venta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM venta "
            "JOIN empleado "
            "ON venta.id_empleado = empleado.id_empleado "
            "JOIN cliente "
            "ON venta.id_cliente = cliente.id_cliente "
            "JOIN promocion "
            "ON venta.id_promocion = promocion.id_promocion "
            "JOIN pago "
            "ON venta.id_pago = pago.id_pago "
            +"WHERE "
                + f"CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
        resultado = cur.fetchall()
        ventas.extend(
            Venta(
                venta[0],
                venta[1],
                EmpleadoDAO().empleado(venta[2]),
                ClienteDAO().cliente(venta[3]),
                PromocionDAO().promocion(venta[4]),
                PagoDAO().pago(venta[5]),
                venta[6]
            )
            for venta in resultado
        )
        cerrarConn(cur, conn)
        if ventas is not None:
            return ventas
        else:
            raise TypeError("No existen ventas")

    def buscarPorEmpleado(self, empleado: Empleado) -> list[Venta]:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM venta "
            f"WHERE id_empleado = {empleado.id_empleado}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                EmpleadoDAO().empleado(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                PromocionDAO().promocion(resultado[4]),
                PagoDAO().pago(resultado[5]),
                resultado[6]
            )
        else:
            raise TypeError("No existen ventas")

    def buscarPorCliente(self, cliente: Cliente) -> list[Venta]:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM venta "
            f"WHERE id_cliente = {cliente.id_cliente}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                EmpleadoDAO().empleado(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                PromocionDAO().promocion(resultado[4]),
                PagoDAO().pago(resultado[5])
            )
        else:
            raise TypeError("No existen ventas")

    def buscarPorPromocion(self, promocion: Promocion) -> list[Venta]:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM venta "
            f"WHERE id_promocion = {promocion.id_promocion}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                EmpleadoDAO().empleado(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                PromocionDAO().promocion(resultado[4]),
                PagoDAO().pago(resultado[5])
            )
        else:
            raise TypeError("No existen ventas")

    def buscarPorPago(self, pago: Pago) -> list[Venta]:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM venta "
            f"WHERE id_pago = {pago.id_pago}"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                EmpleadoDAO().empleado(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                PromocionDAO().promocion(resultado[4]),
                PagoDAO().pago(resultado[5])
            )
        else:
            raise TypeError("No existen ventas")