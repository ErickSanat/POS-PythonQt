from .DB import DBConnection
from ..model import DetalleVenta, Venta, Producto, Categoria
from ..utils import cerrarConn, cerrarCommit

class DetalleVentaDAO:
    def detalleVentas(self) -> list[DetalleVenta]:
        """Fetch all sale details with products and categories in a single query using JOIN
        
        Note: Returns minimal Venta objects with only ID to avoid circular dependency with VentaDAO
        """
        detalleVentas: list[DetalleVenta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem, but only fetch venta ID to avoid circular dependency
        cur.execute(
            "SELECT dv.id_detalle, dv.id_venta, dv.cantidad, dv.subtotal, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM detalle_venta dv "
            "JOIN producto p ON dv.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria"
        )
        resultado = cur.fetchall()
        detalleVentas.extend(
            DetalleVenta(
                detalleVenta[0],  # id_detalle
                Venta(id_venta=detalleVenta[1]),  # minimal venta with just ID
                Producto(
                    detalleVenta[4], detalleVenta[5], detalleVenta[6],
                    detalleVenta[7], detalleVenta[8], detalleVenta[9],
                    Categoria(detalleVenta[10], detalleVenta[11], detalleVenta[12])
                ),
                detalleVenta[2],  # cantidad
                detalleVenta[3]   # subtotal
            )
            for detalleVenta in resultado
        )
        cerrarConn(cur, conn)
        if detalleVentas:
            return detalleVentas
        else:
            raise TypeError("No existen detalles")
    
    def detalleVenta(self, id_detalle: int) -> DetalleVenta:
        """Fetch a single sale detail by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection and JOIN to avoid extra queries
        cur.execute(
            "SELECT dv.id_detalle, dv.id_venta, dv.cantidad, dv.subtotal, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM detalle_venta dv "
            "JOIN producto p ON dv.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE dv.id_detalle = %s",
            (id_detalle,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return DetalleVenta(
                resultado[0],
                Venta(id_venta=resultado[1]),
                Producto(
                    resultado[4], resultado[5], resultado[6],
                    resultado[7], resultado[8], resultado[9],
                    Categoria(resultado[10], resultado[11], resultado[12])
                ),
                resultado[2],
                resultado[3]
            )
        else:
            raise TypeError("No existe el detalle")

    def detalleVentaExistente(self, detalleVenta: DetalleVenta) -> DetalleVenta | bool:
        """Check if sale detail exists by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT dv.id_detalle, dv.id_venta, dv.cantidad, dv.subtotal, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM detalle_venta dv "
            "JOIN producto p ON dv.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE dv.id_detalle = %s",
            (detalleVenta.id_detalle,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return DetalleVenta(
                resultado[0],
                Venta(id_venta=resultado[1]),
                Producto(
                    resultado[4], resultado[5], resultado[6],
                    resultado[7], resultado[8], resultado[9],
                    Categoria(resultado[10], resultado[11], resultado[12])
                ),
                resultado[2],
                resultado[3]
            )
        else:
            return False

    def addDetalleVenta(self, detalleVenta: DetalleVenta):
        """Add a new sale detail using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, subtotal) "
            "VALUES (%s, %s, %s, %s)",
            (detalleVenta.venta.id_venta, detalleVenta.producto.id_producto,
             detalleVenta.cantidad, detalleVenta.subtotal)
        )
        cerrarCommit(cur, conn)

    def updateDetalleVenta(self, detalleVenta: DetalleVenta):
        """Update a sale detail using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE detalle_venta SET id_venta=%s, id_producto=%s, cantidad=%s, "
            "subtotal=%s WHERE id_detalle=%s",
            (detalleVenta.venta.id_venta, detalleVenta.producto.id_producto,
             detalleVenta.cantidad, detalleVenta.subtotal, detalleVenta.id_detalle)
        )
        cerrarCommit(cur, conn)

    def deleteDetalleVenta(self, id_detalleVenta: int):
        """Delete a sale detail using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM detalle_venta WHERE id_detalle=%s", (id_detalleVenta,))
        cerrarCommit(cur, conn)

    def buscarDetalleVentas(self, columna: str, aBuscar: str) -> list[DetalleVenta]:
        """Search sale details using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        detalleVentas: list[DetalleVenta] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['id_detalle', 'id_venta', 'cantidad', 'subtotal']
        if columna not in allowed_columns:
            columna = 'id_detalle'  # default to safe column
        
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            f"SELECT dv.id_detalle, dv.id_venta, dv.cantidad, dv.subtotal, "
            f"p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            f"c.id_categoria, c.nombre, c.descripcion "
            f"FROM detalle_venta dv "
            f"JOIN producto p ON dv.id_producto = p.id_producto "
            f"JOIN categoria c ON p.id_categoria = c.id_categoria "
            f"WHERE CAST(dv.{columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        detalleVentas.extend(
            DetalleVenta(
                detalleVenta[0],
                Venta(id_venta=detalleVenta[1]),
                Producto(
                    detalleVenta[4], detalleVenta[5], detalleVenta[6],
                    detalleVenta[7], detalleVenta[8], detalleVenta[9],
                    Categoria(detalleVenta[10], detalleVenta[11], detalleVenta[12])
                ),
                detalleVenta[2],
                detalleVenta[3]
            )
            for detalleVenta in resultado
        )
        cerrarConn(cur, conn)
        if detalleVentas:
            return detalleVentas
        else:
            raise TypeError("No existen detalleVentas")

    def buscarPorVenta(self, venta: Venta) -> DetalleVenta:
        """Search sale details by sale using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT dv.id_detalle, dv.id_venta, dv.cantidad, dv.subtotal, "
            "p.id_producto, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, "
            "c.id_categoria, c.nombre, c.descripcion "
            "FROM detalle_venta dv "
            "JOIN producto p ON dv.id_producto = p.id_producto "
            "JOIN categoria c ON p.id_categoria = c.id_categoria "
            "WHERE dv.id_venta = %s",
            (venta.id_venta,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return DetalleVenta(
                resultado[0],
                venta,
                Producto(
                    resultado[4], resultado[5], resultado[6],
                    resultado[7], resultado[8], resultado[9],
                    Categoria(resultado[10], resultado[11], resultado[12])
                ),
                resultado[2],
                resultado[3]
            )
        else:
            raise TypeError("No existe el empleado")