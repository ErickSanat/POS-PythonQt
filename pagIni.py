import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from uiPagInicial import Ui_POS  # Cambia por el nombre de tu archivo

class TestWindow(QMainWindow, Ui_POS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setup_resizable_window()

        # Conectar solo un botón para probar
        if hasattr(self, 'clearButton'):
            self.clearButton.clicked.connect(self.test_function)
        
        print("Ventana cargada correctamente")

    def setup_resizable_window(self):
        self.setWindowFlags(Qt.Window)
        self.setMinimumSize(800, 600)
        self.centralWidget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if hasattr(self, 'widget_2'):
            self.widget_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.horizontalLayoutWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frameLeft.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.frameRigth.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.productsScrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def test_function(self):
        print("¡El botón funciona!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
