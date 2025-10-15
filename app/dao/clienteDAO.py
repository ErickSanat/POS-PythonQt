from .DB import DBConnection
from ..model import Cliente

class ClienteDAO:
    @staticmethod
    def clientes() -> list[Cliente]:
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
        return clientes
    
    @staticmethod
    def cliente(id_cliente: int) -> Cliente:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM cliente WHERE id_cliente = {id_cliente}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Cliente(resultado[0], resultado[1], resultado[2], resultado[3])