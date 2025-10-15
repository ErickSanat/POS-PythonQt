from .DB import DBConnection
from ..model import Usuario
from .rolDAO import RolDAO

class UsuarioDAO:
    def usuarios(self) -> list[Usuario]:
        usuarios: list[Usuario] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario")
        resultado = cur.fetchall()
        usuarios.extend(
            Usuario(
                usuario[0],
                usuario[1],
                usuario[2],
                RolDAO().rol(usuario[3])
                )
                for usuario in resultado
            )
        cur.close()
        conn.close()
        return usuarios
    
    def usuario(self, id_usuario: int) -> Usuario:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM usuario WHERE id_usuario = {id_usuario}")
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return Usuario(
            resultado[0],
            resultado[1],
            resultado[2],
            RolDAO().rol(resultado[3])
        )