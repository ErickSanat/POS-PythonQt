from ..model import Usuario
from ..dao import UsuarioDAO

class UsuarioController:
    def __init__(self):
        self.usuarioDAO = UsuarioDAO()
    
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
    
    def addUsuario(self, usuario: Usuario):
        self.usuarioDAO.addUsuario(usuario)
    
    def updateUsuario(self, usuario: Usuario):
        self.usuarioDAO.updateUsuario(usuario)
    
    def deleteUsuario(self, id_usuario: int):
        self.usuarioDAO.deleteUsuario(id_usuario)