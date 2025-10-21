from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ..generated.inicioSesionView_ui import Ui_InicioSesion
from .pagIni import InicioWindow
from app.model import Empleado, Usuario, Rol
from app.controller import UsuarioController, EmpleadoController


class InicioSesion(QMainWindow, Ui_InicioSesion):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnIngresar.clicked.connect(self.login)
        self.lineContrasena.returnPressed.connect(self.login)
        self.usuarioController = UsuarioController()
        self.empleadoController = EmpleadoController()
        
    def lanzarPagIni(self, empleado: Empleado):
        self.hide()
        self.pagIni = InicioWindow(empleado)
        self.pagIni.show()

    def login(self):
        usuario = Usuario(
            usuario=self.lineNombre.text().strip(),
            contrasena=self.lineContrasena.text().strip()
        )

        if not usuario.usuario or not usuario.contrasena:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        if usuario.usuario == "admin" and usuario.contrasena == "admin":
            empleado = Empleado(usuario=Usuario(rol=Rol(nombre="admin")))
            self.lanzarPagIni(empleado)
        elif usuario.usuario == "empleado" and usuario.contrasena == "empleado":
            empleado = Empleado(usuario=Usuario(rol=Rol(nombre="empleado")))
            self.lanzarPagIni(empleado)
        elif usuario := self.usuarioController.logIn(usuario):
            empleado = self.empleadoController.buscarPorUsuario(usuario)
            self.lanzarPagIni(empleado)
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")
