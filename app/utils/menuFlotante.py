from PyQt5.QtWidgets import QApplication

class MenuFlotante:
    """Mixin para manejar menú flotante que ya existe en la UI"""
    
    def setupFloatingMenu(self):
        """Configurar las propiedades del menú flotante"""
        # Verificar que el frameFlotante existe antes de usarlo
        if not hasattr(self, 'frameFlotante'):
            print("Advertencia: frameFlotante no existe en la UI")
            return
            
        # Ocultar inicialmente el menú
        self.frameFlotante.hide()

        # Configurar tamaño y posición inicial
        self.frameFlotante.setFixedSize(331, 321)

        # Conectar los botones del menú flotante
        self.connectMenuButtons()
        
        # Conectar el botón principal del menú
        if hasattr(self, 'btnMenu'):
            self.btnMenu.clicked.connect(self.toggleFloatingMenu)
        else:
            print("Advertencia: btnMenu no encontrado")
        
    def connectMenuButtons(self):
        """Conectar los botones del menú flotante a sus funciones"""
        # Verificar que todos los botones existen antes de conectarlos
        button_mappings = {
            'btnMenuInicio': self.menuInicio,
            'btnVentas': self.menuVentas,
            'btnPromociones': self.menuPromociones,
            'btnClientes': self.menuClientes,
            'btnProveedores': self.menuProveedores,
            'btnProductos': self.menuProductos,
            'btnRecetas': self.menuRecetas,
            'btnEmpleados': self.menuEmpleados,
            'btnCerrarSesion': self.menuCerrarSesion
        }
        
        for button_name, function in button_mappings.items():
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                button.clicked.connect(function)
            else:
                print(f"Advertencia: Botón {button_name} no encontrado")

    def toggleFloatingMenu(self):
        """Mostrar u ocultar el menú flotante"""
        if not hasattr(self, 'frameFlotante'):
            return
            
        if self.frameFlotante.isVisible():
            self.hideFloatingMenu()
        else:
            self.showFloatingMenu()

    def showFloatingMenu(self):
        """Mostrar el menú flotante con animación"""
        if not hasattr(self, 'frameFlotante') or not hasattr(self, 'btnMenu'):
            return
            
        # Posicionar el menú debajo del botón
        buttonPos = self.btnMenu.pos()
        menuX = buttonPos.x() - self.frameFlotante.width() + self.btnMenu.width()
        menuY = buttonPos.y() + self.btnMenu.height() + 5

        self.frameFlotante.move(menuX, menuY)
        self.frameFlotante.show()
        self.frameFlotante.raise_()

    def hideFloatingMenu(self):
        """Ocultar el menú flotante"""
        if hasattr(self, 'frameFlotante'):
            self.frameFlotante.hide()

    def mousePressEvent(self, event):
        """Ocultar el menú flotante al hacer clic fuera de él"""
        if (hasattr(self, 'frameFlotante') and hasattr(self, 'btnMenu') and
                self.frameFlotante.isVisible() and
                not self.frameFlotante.geometry().contains(event.globalPos()) and
                not self.btnMenu.geometry().contains(self.btnMenu.mapFromGlobal(event.globalPos()))):
            self.hideFloatingMenu()
        
        # ✅ IMPORTANTE: Llamar al método padre correctamente
        if hasattr(super(), 'mousePressEvent'):
            super().mousePressEvent(event)

    # Funciones para los botones del menú
    def menuInicio(self):
        if hasattr(self, 'pagInicio'):
            self.pagInicio.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagIni import InicioWindow
            self.pagInicio = InicioWindow()
            self.pagInicio.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar InicioWindow: {e}")
        self.hideFloatingMenu()

    def menuVentas(self):
        if hasattr(self, 'pagVen'):
            self.pagVen.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagVen import VenWindow
            self.pagVen = VenWindow()
            self.pagVen.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar VenWindow: {e}")
        self.hideFloatingMenu()

    def menuPromociones(self):
        if hasattr(self, 'pagProm'):
            self.pagProm.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagProm import PromWindow
            self.pagProm = PromWindow()
            self.pagProm.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar PromWindow: {e}")
        self.hideFloatingMenu()

    def menuClientes(self):
        if hasattr(self, 'pagUser'):
            self.pagUser.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagUser import UserWindow
            self.pagUser = UserWindow()
            self.pagUser.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar UserWindow: {e}")
        self.hideFloatingMenu()

    def menuProveedores(self):
        if hasattr(self, 'pagProv'):
            self.pagProv.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagProv import ProvWindow
            self.pagProv = ProvWindow()
            self.pagProv.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar ProvWindow: {e}")
        self.hideFloatingMenu()


    def menuProductos(self):
        if hasattr(self, 'pagPro'):
            self.pagPro.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagPro import ProWindow
            self.pagPro = ProWindow()
            self.pagPro.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar ProWindow: {e}")
        self.hideFloatingMenu()


    def menuRecetas(self):
        if hasattr(self, 'pagRec'):
            self.pagRec.show()
            self.window.hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagRec import RecWindow
            self.pagRec = RecWindow()
            self.pagRec.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar RecWindow: {e}")
        self.hideFloatingMenu()

    def menuEmpleados(self):
        if hasattr(self, 'pagEmp'):
            self.pagEmp.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagEmp import EmpWindow
            self.pagEmp = EmpWindow()
            self.pagEmp.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar EmpWindow: {e}")
        self.hideFloatingMenu()

    def menuCerrarSesion(self):
        if hasattr(self, 'pagIni'):
            self.pagIni.show()
            self.window().hide()
            self.hideFloatingMenu()
            return
        try:
            from app.view.window.pagInicioSesion import InicioSesion
            self.pagIni = InicioSesion()
            self.pagIni.show()
            self.window().hide()
            self.hideFloatingMenu()
        except ImportError as e:
            print(f"Error al importar InicioWindow: {e}")
        self.hideFloatingMenu()

