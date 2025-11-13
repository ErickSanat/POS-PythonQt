from .DB import DBConnection
from ..model import Cliente
from ..utils import cerrarConn, cerrarCommit


class ClienteDAO:
    def clientes(self) -> list[Cliente]:
        """Fetch all clients"""
        clientes: list[Cliente] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cliente")
        resultado = cur.fetchall()
        clientes.extend(
            Cliente(
                cliente[0],
                cliente[1],
                cliente[2],
                cliente[3]
            )
            for cliente in resultado
        )
        cerrarConn(cur, conn)
        if clientes:
            return clientes
        else:
            raise TypeError("No existen clientes")
    
    def cliente(self, id_cliente: int) -> Cliente:
        """Fetch a single client by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id_cliente,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            raise TypeError("No existe el cliente")

    def clienteExistente(self, cliente: Cliente) -> Cliente | bool:
        """Check if client exists by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM cliente WHERE nombre = %s", (cliente.nombre,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            return False

    def addCliente(self, cliente: Cliente):
        """Add a new client using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO cliente (nombre, telefono, correo) VALUES (%s, %s, %s)",
            (cliente.nombre, cliente.telefono, cliente.correo)
        )
        cerrarCommit(cur, conn)

    def updateCliente(self, cliente: Cliente):
        """Update a client using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE cliente SET nombre=%s, telefono=%s, correo=%s WHERE id_cliente=%s",
            (cliente.nombre, cliente.telefono, cliente.correo, cliente.id_cliente)
        )
        cerrarCommit(cur, conn)

    def deleteCliente(self, id_cliente: int):
        """Delete a client using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_cliente,))
        cerrarCommit(cur, conn)

    def porNombre(self, nombre: str) -> Cliente:
        """Get client by name using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("SELECT * FROM cliente WHERE nombre = %s", (nombre,))
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            raise TypeError(f"No existe el cliente con nombre '{nombre}'")

    def buscarClientes(self, columna: str, aBuscar: str) -> list[Cliente]:
        """Search clients using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        clientes: list[Cliente] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['nombre', 'telefono', 'correo', 'id_cliente']
        if columna not in allowed_columns:
            columna = 'nombre'  # default to safe column
        
        cur.execute(
            f"SELECT * FROM cliente WHERE CAST({columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        clientes.extend(
            Cliente(
                cliente[0],
                cliente[1],
                cliente[2],
                cliente[3]
            )
            for cliente in resultado
        )
        cerrarConn(cur, conn)
        if clientes:
            return clientes
        else:
            raise TypeError("No existen clientes")