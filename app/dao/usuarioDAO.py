from .DB import DBConnection
from ..utils import cerrarCommit, cerrarConn
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
        cerrarConn(cur, conn)
        if usuarios is not None:
            return usuarios
        else:
            raise TypeError("No existen usuarios")
    
    def usuario(self, id_usuario: int) -> Usuario:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM usuario WHERE id_usuario = {id_usuario}")
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Usuario(
                resultado[0],
                resultado[1],
                resultado[2],
                RolDAO().rol(resultado[3])
            )
        else:
            raise TypeError("No existe el usuario")
    
    def usuarioExistente(self, usuario: Usuario) -> Usuario | bool:
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM usuario "
            +"WHERE "
                + f"usuario = '{usuario.usuario}'"
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Usuario(resultado[0], resultado[1], resultado[2], RolDAO().rol(resultado[3]))
        else:
            return False
        
    def addUsuario(self, usuario: Usuario):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuario ("
                + "usuario,"
                + "contrasena,"
                + "id_rol"
            +") VALUES ("
                + f"'{usuario.usuario}',"
                + f"'{usuario.contrasena}',"
                + f"{usuario.rol.id_rol})"
        )
        cerrarCommit(cur, conn)
    
    def updateUsuario(self, usuario: Usuario):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuario "
            + "SET "
                + f"usuario='{usuario.usuario}', "
                + f"contrasena='{usuario.contrasena}', "
                + f"id_rol={usuario.rol.id_rol} "
            +"WHERE "
                + f"id_usuario={usuario.id_usuario}"
            )
        cerrarCommit(cur, conn)
    
    def deleteUsuario(self, id_usuario: int):
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE "
            + "FROM "
                + "usuario "
            +"WHERE "
                + f"id_usuario={id_usuario}"
            )
        cerrarCommit(cur, conn)
    
    def buscarUsuarios(self, columna: str, aBuscar: str) -> list[Usuario]:
        if not aBuscar:
            raise TypeError("falta texto")
        usuarios: list[Usuario] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * "
            + "FROM usuario "
            + "JOIN rol "
            + "ON usuario.id_rol = rol.id_rol "
            + f"WHERE CAST({columna} AS TEXT) LIKE '%{aBuscar}%'")
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
        cerrarConn(cur, conn)
        if usuarios is not None:
            return usuarios
        else:
            raise TypeError("No existen usuarios")