from .DB import DBConnection
from ..model import Venta
from .usuarioDAO import UsuarioDAO
from .clienteDAO import ClienteDAO

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
                UsuarioDAO().usuario(venta[2]),
                ClienteDAO().cliente(venta[3]),
                venta[4]
                )
                for venta in resultado
            )
        cur.close()
        conn.close()
        return ventas
    
    def venta(self, id_venta: int) -> Venta:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM venta WHERE id_venta = {id_venta}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Venta(
                resultado[0],
                resultado[1],
                UsuarioDAO().usuario(resultado[2]),
                ClienteDAO().cliente(resultado[3]),
                resultado[4]
            )