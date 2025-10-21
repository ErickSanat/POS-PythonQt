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
        self.usuarioDAO.updateUsuario(usuario)
    
    def deleteUsuario(self, id_usuario: int):
        self.usuarioDAO.deleteUsuario(id_usuario)
    
    def logIn(self, usuario: Usuario) -> Usuario | bool:
        self.jacheo.update(usuario.contrasena.encode('utf-8'))
        contrasenaJacheada = self.jacheo.hexdigest()
        if usuarioBD:=self.usuarioDAO.usuarioExistente(usuario):
            if contrasenaJacheada == usuarioBD.contrasena:
                return usuarioBD
            else:
                return False