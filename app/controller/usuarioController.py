from ..model import Usuario
from ..dao import UsuarioDAO
import hashlib

class UsuarioController:
    def __init__(self):
        self.usuarioDAO = UsuarioDAO()
        self.jacheo = hashlib.md5()
    
    def usuarios(self) -> list[Usuario]:
        try:
            return self.usuarioDAO.usuarios()
        except Exception as e:
            return e
    
    def usuario(self, id_usuario) -> Usuario:
        try:
            return self.usuarioDAO.usuario(id_usuario)
        except Exception as e:
            return e
    
    def addUsuario(self, usuario: Usuario) -> str:
        if not self.usuarioDAO.usuarioExistente(usuario):
            self.jacheo.update(usuario.contrasena.encode('utf-8'))
            usuario.contrasena = self.jacheo.hexdigest()
            self.usuarioDAO.addUsuario(usuario)
            return "Añadido exitosamente"
        else:
            return "El nombre de usuario ya existe"
    
    def updateUsuario(self, usuario: Usuario):
        if self.usuario(usuario.id_usuario).contrasena != usuario.contrasena:
            usuario.contrasena = self.jacheado(usuario.contrasena)
        self.usuarioDAO.updateUsuario(usuario)
    
    def deleteUsuario(self, id_usuario: int):
        self.usuarioDAO.deleteUsuario(id_usuario)
        
    def buscar(self, columna: str, aBuscar: str) -> list[Usuario]:
        try:
            return self.usuarioDAO.buscarUsuarios(columna, aBuscar)
        except Exception as e:
            raise e
    
    def logIn(self, usuario: Usuario) -> Usuario | bool:
        if usuarioBD:=self.usuarioDAO.usuarioExistente(usuario):
            if self.jacheado(usuario.contrasena) == usuarioBD.contrasena:
                return usuarioBD
            else:
                return False
    
    def jacheado(self, contrasena: str) -> str:
        self.jacheo.update(contrasena.encode('utf-8'))
        return self.jacheo.hexdigest()
