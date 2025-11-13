from .DB import DBConnection
from ..utils import cerrarCommit, cerrarConn
from ..model import Usuario, Rol

class UsuarioDAO:
    def usuarios(self) -> list[Usuario]:
        """Fetch all users with their roles in a single query using JOIN"""
        usuarios: list[Usuario] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            "SELECT u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM usuario u "
            "JOIN rol r ON u.id_rol = r.id_rol"
        )
        resultado = cur.fetchall()
        usuarios.extend(
            Usuario(
                usuario[0],  # id_usuario
                usuario[1],  # usuario
                usuario[2],  # contrasena
                Rol(usuario[3], usuario[4])  # rol
            )
            for usuario in resultado
        )
        cerrarConn(cur, conn)
        if usuarios:
            return usuarios
        else:
            raise TypeError("No existen usuarios")
    
    def usuario(self, id_usuario: int) -> Usuario:
        """Fetch a single user by ID using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection and JOIN to avoid extra query
        cur.execute(
            "SELECT u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM usuario u "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "WHERE u.id_usuario = %s",
            (id_usuario,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Usuario(
                resultado[0],
                resultado[1],
                resultado[2],
                Rol(resultado[3], resultado[4])
            )
        else:
            raise TypeError("No existe el usuario")
    
    def usuarioExistente(self, usuario: Usuario) -> Usuario | bool:
        """Check if user exists by username using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM usuario u "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "WHERE u.usuario = %s",
            (usuario.usuario,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Usuario(resultado[0], resultado[1], resultado[2], Rol(resultado[3], resultado[4]))
        else:
            return False
        
    def addUsuario(self, usuario: Usuario):
        """Add a new user using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "INSERT INTO usuario (usuario, contrasena, id_rol) VALUES (%s, %s, %s)",
            (usuario.usuario, usuario.contrasena, usuario.rol.id_rol)
        )
        cerrarCommit(cur, conn)
    
    def updateUsuario(self, usuario: Usuario):
        """Update a user using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "UPDATE usuario SET usuario=%s, contrasena=%s, id_rol=%s WHERE id_usuario=%s",
            (usuario.usuario, usuario.contrasena, usuario.rol.id_rol, usuario.id_usuario)
        )
        cerrarCommit(cur, conn)
    
    def deleteUsuario(self, id_usuario: int):
        """Delete a user using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute("DELETE FROM usuario WHERE id_usuario=%s", (id_usuario,))
        cerrarCommit(cur, conn)

    def porNombre(self, nombre: str) -> Usuario:
        """Get user by username using parameterized query"""
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cur.execute(
            "SELECT u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            "FROM usuario u "
            "JOIN rol r ON u.id_rol = r.id_rol "
            "WHERE u.usuario = %s",
            (nombre,)
        )
        resultado = cur.fetchone()
        cerrarConn(cur, conn)
        if resultado is not None:
            return Usuario(
                resultado[0],
                resultado[1],
                resultado[2],
                Rol(resultado[3], resultado[4])
            )
        else:
            raise TypeError(f"No existe el usuario con nombre '{nombre}'")
    
    def buscarUsuarios(self, columna: str, aBuscar: str) -> list[Usuario]:
        """Search users using parameterized query"""
        if not aBuscar:
            raise TypeError("falta texto")
        usuarios: list[Usuario] = []
        conn = DBConnection.connection()
        cur = conn.cursor()
        # Use parameterized query with column validation to prevent SQL injection
        allowed_columns = ['usuario', 'id_usuario']
        if columna not in allowed_columns:
            columna = 'usuario'  # default to safe column
        
        # Use JOIN to avoid N+1 query problem
        cur.execute(
            f"SELECT u.id_usuario, u.usuario, u.contrasena, r.id_rol, r.nombre "
            f"FROM usuario u "
            f"JOIN rol r ON u.id_rol = r.id_rol "
            f"WHERE CAST(u.{columna} AS TEXT) LIKE %s",
            (f'%{aBuscar}%',)
        )
        resultado = cur.fetchall()
        usuarios.extend(
            Usuario(
                usuario[0],
                usuario[1],
                usuario[2],
                Rol(usuario[3], usuario[4])
            )
            for usuario in resultado
        )
        cerrarConn(cur, conn)
        if usuarios:
            return usuarios
        else:
            raise TypeError("No existen usuarios")