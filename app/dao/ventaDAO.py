from .DB import DBConnection
from ..utils import cerrarConn, cerrarCommit
from ..model import Venta, Empleado, Cliente, Promocion, Pago, Usuario, Rol, TipoPago

class VentaDAO:
    def ventas(self) -> list[Venta]:
        """Fetch all sales with related data in a single query using JOINs"""
        ventas: list[Venta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use LEFT JOIN for nullable promocion, JOIN for required fields
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago"
        )
        resultado = cur.fetchall()
        ventas.extend(
            Venta(
                venta[0],  # id_venta
                venta[1],  # fecha
                Empleado(venta[3], venta[4], venta[5], venta[6], 
                        Usuario(venta[7], venta[8], venta[9], Rol(venta[10], venta[11]))),
                Cliente(venta[12], venta[13], venta[14], venta[15]),
                Promocion(venta[16], venta[17], venta[18], venta[19]) if venta[16] is not None else None,
                Pago(venta[20], TipoPago(venta[22], venta[23]), venta[21]),
                venta[2]  # total
            )
            for venta in resultado
        )
        cerrarConn(cur, conn)
        if ventas:
            return ventas
        else:
            raise TypeError("No existen ventas")
    
    def venta(self, id_venta: int) -> Venta:
        """Fetch a single sale by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            "WHERE v.id_venta = %s",
            (id_venta,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                Empleado(resultado[3], resultado[4], resultado[5], resultado[6],
                        Usuario(resultado[7], resultado[8], resultado[9], Rol(resultado[10], resultado[11]))),
                Cliente(resultado[12], resultado[13], resultado[14], resultado[15]),
                Promocion(resultado[16], resultado[17], resultado[18], resultado[19]) if resultado[16] is not None else None,
                Pago(resultado[20], TipoPago(resultado[22], resultado[23]), resultado[21]),
                resultado[2]
            )
        else:
            raise TypeError("No existe la venta")

    def addVenta(self, venta: Venta):
        """Add a new sale using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        if venta.promocion and venta.promocion.id_promocion is not None:
            cur.execute(
                "INSERT INTO venta (fecha, id_empleado, id_cliente, id_promocion, id_pago, total) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (venta.fecha, venta.empleado.id_empleado, venta.cliente.id_cliente,
                 venta.promocion.id_promocion, venta.pago.id_pago, venta.total)
            )
        else:
            cur.execute(
                "INSERT INTO venta (fecha, id_empleado, id_cliente, id_pago, total) "
                "VALUES (%s, %s, %s, %s, %s)",
                (venta.fecha, venta.empleado.id_empleado, venta.cliente.id_cliente,
                 venta.pago.id_pago, venta.total)
            )
        cerrarCommit(cur, conn)

    def ultimaVenta(self) -> Venta:
        """Fetch the most recent sale"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            "ORDER BY v.id_venta DESC LIMIT 1"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                Empleado(resultado[3], resultado[4], resultado[5], resultado[6],
                        Usuario(resultado[7], resultado[8], resultado[9], Rol(resultado[10], resultado[11]))),
                Cliente(resultado[12], resultado[13], resultado[14], resultado[15]),
                Promocion(resultado[16], resultado[17], resultado[18], resultado[19]) if resultado[16] is not None else None,
                Pago(resultado[20], TipoPago(resultado[22], resultado[23]), resultado[21]),
                resultado[2]
            )
        else:
            raise TypeError("No existe el pago")
            
    def ventaExistente(self, venta: Venta) -> Venta | bool:
        """Check if sale exists by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            "WHERE v.id_venta = %s",
            (venta.id_venta,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                Empleado(resultado[3], resultado[4], resultado[5], resultado[6],
                        Usuario(resultado[7], resultado[8], resultado[9], Rol(resultado[10], resultado[11]))),
                Cliente(resultado[12], resultado[13], resultado[14], resultado[15]),
                Promocion(resultado[16], resultado[17], resultado[18], resultado[19]) if resultado[16] is not None else None,
                Pago(resultado[20], TipoPago(resultado[22], resultado[23]), resultado[21]),
                resultado[2]
            )
        else:
            return False

    def buscarVentas(self, columna: str, aBuscar: str) -> list[Venta]:
        """Search sales using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        ventas: list[Venta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['id_venta', 'fecha', 'total']
        if columna not in allowed_columns:
            columna = 'id_venta'  # default to safe column
        
        cur.execute(
            f"SELECT v.id_venta, v.fecha, v.total, "
            f"e.id_empleado, e.nombre, e.direccion, e.telefono, "
            f"u.id_usuario, u.usuario, u.contrasena, "
            f"r.id_rol, r.nombre, "
            f"c.id_cliente, c.nombre, c.telefono, c.correo, "
            f"pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            f"pa.id_pago, pa.cantidad, "
            f"tp.id_tipo_pago, tp.nombre "
            f"FROM venta v "
            f"JOIN empleado e ON v.id_empleado = e.id_empleado "
            f"JOIN usuario u ON e.id_usuario = u.id_usuario "
            f"JOIN rol r ON u.id_rol = r.id_rol "
            f"JOIN cliente c ON v.id_cliente = c.id_cliente "
            f"LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            f"JOIN pago pa ON v.id_pago = pa.id_pago "
            f"JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            f"WHERE CAST(v.{columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        ventas.extend(
            Venta(
                venta[0],
                venta[1],
                Empleado(venta[3], venta[4], venta[5], venta[6],
                        Usuario(venta[7], venta[8], venta[9], Rol(venta[10], venta[11]))),
                Cliente(venta[12], venta[13], venta[14], venta[15]),
                Promocion(venta[16], venta[17], venta[18], venta[19]) if venta[16] is not None else None,
                Pago(venta[20], TipoPago(venta[22], venta[23]), venta[21]),
                venta[2]
            )
            for venta in resultado
        )
        cerrarConn(cur, conn)
        if ventas:
            return ventas
        else:
            raise TypeError("No existen ventas")

    def buscarPorEmpleado(self, empleado: Empleado) -> list[Venta]:
        """Search sales by employee using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            "WHERE v.id_empleado = %s",
            (empleado.id_empleado,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                Empleado(resultado[3], resultado[4], resultado[5], resultado[6],
                        Usuario(resultado[7], resultado[8], resultado[9], Rol(resultado[10], resultado[11]))),
                Cliente(resultado[12], resultado[13], resultado[14], resultado[15]),
                Promocion(resultado[16], resultado[17], resultado[18], resultado[19]) if resultado[16] is not None else None,
                Pago(resultado[20], TipoPago(resultado[22], resultado[23]), resultado[21]),
                resultado[2]
            )
        else:
            raise TypeError("No existen ventas")

    def buscarPorCliente(self, cliente: Cliente) -> list[Venta]:
        """Search sales by client using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            "WHERE v.id_cliente = %s",
            (cliente.id_cliente,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                Empleado(resultado[3], resultado[4], resultado[5], resultado[6],
                        Usuario(resultado[7], resultado[8], resultado[9], Rol(resultado[10], resultado[11]))),
                Cliente(resultado[12], resultado[13], resultado[14], resultado[15]),
                Promocion(resultado[16], resultado[17], resultado[18], resultado[19]) if resultado[16] is not None else None,
                Pago(resultado[20], TipoPago(resultado[22], resultado[23]), resultado[21]),
                resultado[2]
            )
        else:
            raise TypeError("No existen ventas")

    def buscarPorPromocion(self, promocion: Promocion) -> list[Venta]:
        """Search sales by promotion using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            "WHERE v.id_promocion = %s",
            (promocion.id_promocion,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                Empleado(resultado[3], resultado[4], resultado[5], resultado[6],
                        Usuario(resultado[7], resultado[8], resultado[9], Rol(resultado[10], resultado[11]))),
                Cliente(resultado[12], resultado[13], resultado[14], resultado[15]),
                Promocion(resultado[16], resultado[17], resultado[18], resultado[19]),
                Pago(resultado[20], TipoPago(resultado[22], resultado[23]), resultado[21]),
                resultado[2]
            )
        else:
            raise TypeError("No existen ventas")

    def buscarPorPago(self, pago: Pago) -> list[Venta]:
        """Search sales by payment using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT v.id_venta, v.fecha, v.total, "
            "e.id_empleado, e.nombre, e.direccion, e.telefono, "
            "u.id_usuario, u.usuario, u.contrasena, "
            "r.id_rol, r.nombre, "
            "c.id_cliente, c.nombre, c.telefono, c.correo, "
            "pr.id_promocion, pr.nombre, pr.porcentaje, pr.descripcion, "
            "pa.id_pago, pa.cantidad, "
            "tp.id_tipo_pago, tp.nombre "
            "FROM venta v "
            "JOIN empleado e ON v.id_empleado = e.id_empleado "
            "JOIN usuario u ON e.id_usuario = u.id_usuario "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "JOIN cliente c ON v.id_cliente = c.id_cliente "
            "LEFT JOIN promocion pr ON v.id_promocion = pr.id_promocion "
            "JOIN pago pa ON v.id_pago = pa.id_pago "
            "JOIN tipo_pago tp ON pa.id_tipo_pago = tp.id_tipo_pago "
            "WHERE v.id_pago = %s",
            (pago.id_pago,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Venta(
                resultado[0],
                resultado[1],
                Empleado(resultado[3], resultado[4], resultado[5], resultado[6],
                        Usuario(resultado[7], resultado[8], resultado[9], Rol(resultado[10], resultado[11]))),
                Cliente(resultado[12], resultado[13], resultado[14], resultado[15]),
                Promocion(resultado[16], resultado[17], resultado[18], resultado[19]) if resultado[16] is not None else None,
                Pago(resultado[20], TipoPago(resultado[22], resultado[23]), resultado[21]),
                resultado[2]
            )
        else:
            raise TypeError("No existen ventas")