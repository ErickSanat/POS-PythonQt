import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..generated.uiPagInicial import Ui_POS

class TestWindow(QMainWindow, Ui_POS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        if hasattr(self, 'clearButton'):
            self.clearButton.clicked.connect(self.test_function)
        print("Ventana cargada correctamente")

    def test_function(self):
        print("¡El botón funciona!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())