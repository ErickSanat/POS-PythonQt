from .DB import DBConnection
from ..model import Cliente, cliente
from ..utils import cerrarConn, cerrarCommit


class ClienteDAO:
    def clientes(self) -> list[Cliente]:
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
        cur.close()
        conn.close()
        if clientes is not None:
            return clientes
        else:
            raise TypeError("No existen clientes")
    
    def cliente(self, id_cliente: int) -> Cliente:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM cliente WHERE id_cliente = {id_cliente}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        if resultado is not None:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            raise TypeError("No existe el cliente")

    def clienteExistente(self, cliente: Cliente) -> Cliente | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM cliente WHERE nombre = '{cliente.nombre}'")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            return False

    def addCliente(self, cliente: Cliente):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cliente ("
                + "nombre,"
                + "telefono,"
                + "correo"
            + ") VALUES ("
                + f"'{cliente.nombre}',"
                + f"{cliente.telefono},"
                + f"'{cliente.correo}')"
        )
        cerrarCommit(cur, conn)

    def updateCliente(self, cliente: Cliente):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE cliente "
            + "SET "
                + f"nombre='{cliente.nombre}', "
                + f"telefono={cliente.telefono}, "
                + f"correo='{cliente.correo}' "
            +"WHERE "
            + f"id_cliente={cliente.id_cliente}"
        )
        cerrarCommit(cur, conn)

    def deleteCliente(self, id_cliente: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            + "FROM "
                + "cliente "
            +"WHERE "
            + f"id_cliente={id_cliente}"
        )
        cerrarCommit(cur, conn)

    def porNombre(self, nombre: str) -> Cliente:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM cliente WHERE cliente ='{nombre}'")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])
        else:
            raise TypeError(f"No existe el cliente con nombre '{nombre}'")

    def buscarClientes(self, columna: str, aBuscar: str) -> list[Cliente]:
        if not aBuscar:
            raise TypeError("falta texto")
        clientes: list[Cliente] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * "
            + "FROM cliente "
            + f"WHERE CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
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
        if clientes is not None:
            return clientes
        else:
            raise TypeError("No existen clientes")