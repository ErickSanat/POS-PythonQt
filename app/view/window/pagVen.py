import sys
import csv
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.ventaView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Venta, Empleado, Cliente, Promocion, Pago
from app.controller import (VentaController, EmpleadoController,
                            ClienteController, PromocionController,
                            PagoController)


class VentaTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Venta en un QTableView"""

    def __init__(self, ventas: list = None, parent=None):
        super().__init__(parent)
        self.ventas = ventas or []
        # Definir columnas: (atributo, encabezado)
        self._columns = [
            ("id_venta", "ID"),
            ("fecha", "Fecha"),
            ("empleado", "Empleado"),
            ("cliente", "Cliente"),
            ("promocion", "Promocion"),
            ("pago", "Pago"),
            ("total", "Total")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self.ventas)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        venta_obj = self.ventas[index.row()]
        attr, _header = self._columns[index.column()]

        # Manejar atributo compuesto (fecha)
        if attr == "fecha":
            fecha = getattr(venta_obj, "fecha", None)
            return fecha.strftime("%d/%m/%Y") if fecha is not None else ""

        # Manejar atributo compuesto (empleado.nombre)
        if attr == "empleado":
            empleado = getattr(venta_obj, "empleado", None)
            return str(empleado.nombre) if empleado is not None else ""

        # Manejar atributo compuesto (cliente.nombre)
        if attr == "cliente":
            cliente = getattr(venta_obj, "cliente", None)
            return str(cliente.nombre) if cliente is not None else ""

        # Manejar atributo compuesto (promocion.nombre)
        if attr == "promocion":
            promocion = getattr(venta_obj, "promocion", None)
            return str(promocion.nombre) if promocion is not None else ""

        # Manejar atributo compuesto (pago.metodo)
        if attr == "pago":
            pago = getattr(venta_obj, "pago", None)
            return str(pago.cantidad) if pago is not None else ""

        # Obtener valor del atributo
        valor = getattr(venta_obj, attr, "")
        return str(valor) if valor is not None else ""

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return self._columns[section][1]

        return str(section + 1)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setVentas(self, ventas: list):
        """Actualizar la lista de ventas en el modelo"""
        self.beginResetModel()
        self.ventas = ventas or []
        self.endResetModel()


class VenWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.ventaController = VentaController()
        self.clienteController = ClienteController()
        self.empleadoController = EmpleadoController()
        self.promocionController = PromocionController()
        self.pagoController = PagoController()
        self.venta = Venta()
        self.ventas = None
        self.labelEmpleado.setText(f"Empleado: {empleado.nombre}")

        # Llenar combobox de de categorias de busqueda
        self.comboCategorias.addItem("ID", "id_venta")
        self.comboCategorias.addItem("Fecha", "fecha")
        self.comboCategorias.addItem("Empleado", "empleado")
        self.comboCategorias.addItem("Cliente", "cliente")
        self.comboCategorias.addItem("Promocion", "promocion")
        self.comboCategorias.addItem("Pago", "pago")
        self.comboCategorias.addItem("Total", "total")

        # Configurar el modelo para la tabla
        self._table_model = VentaTableModel()
        self.tableView.setModel(self._table_model)

        # Configurar apariencia de la tabla
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        # self.tableView.doubleClicked.connect(self.handleDobleClic)

        # Conectar botones
        self.btnBuscar.clicked.connect(self.handleBuscarBtn)
        self.btnGenerarExcel.clicked.connect(self.handleGenerarExcelBtn)

        # Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()

    def handleGenerarExcelBtn(self):
        """Generar archivo CSV con los datos de ventas"""
        try:
            # Verificar si hay datos para exportar
            if self._table_model.rowCount() == 0:
                QMessageBox.warning(self, "Advertencia",
                                    "No hay datos de ventas para exportar.")
                return

            # Solicitar ubicación para guardar el archivo
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
            fileName, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Reporte de Ventas",
                f"reporte_ventas_{fecha_actual}.csv",
                "Archivos CSV (*.csv)"
            )

            if not fileName:
                return  # Usuario canceló la operación

            # Asegurar que el archivo tenga extensión .csv
            if not fileName.lower().endswith('.csv'):
                fileName += '.csv'

            # Generar el archivo CSV
            with open(fileName, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Escribir encabezado informativo
                writer.writerow(["Reporte de Ventas - Alquimia Pasteleria"])
                writer.writerow([f"Fecha de generacion: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"])
                writer.writerow([f"Total de registros: {self._table_model.rowCount()}"])
                writer.writerow([])  # Línea en blanco

                # Escribir encabezados de columnas
                headers = []
                for col in range(self._table_model.columnCount()):
                    headers.append(self._table_model.headerData(col, Qt.Horizontal, Qt.DisplayRole))
                writer.writerow(headers)

                # Escribir datos de las ventas
                for row in range(self._table_model.rowCount()):
                    row_data = []
                    for col in range(self._table_model.columnCount()):
                        index = self._table_model.index(row, col)
                        value = self._table_model.data(index, Qt.DisplayRole)
                        row_data.append(value)
                    writer.writerow(row_data)

                # Escribir resumen al final
                writer.writerow([])
                writer.writerow(["RESUMEN"])
                total_ventas = self.calcularTotalVentas()
                writer.writerow(["Total de ingresos:", f"${total_ventas:.2f}"])
                writer.writerow(["Promedio por venta:", f"${total_ventas / self._table_model.rowCount():.2f}"])

            # Mostrar mensaje de éxito
            QMessageBox.information(
                self,
                "Exportación Exitosa",
                f"Se generó el archivo CSV correctamente.\n\n"
                f"Ubicación: {fileName}\n"
                f"Registros exportados: {self._table_model.rowCount()}\n"
                f"Total exportado: ${total_ventas:.2f}"
            )

        except PermissionError:
            QMessageBox.critical(
                self,
                "Error de Permisos",
                "No se tiene permiso para guardar en la ubicación seleccionada.\n"
                "Por favor, elija otra carpeta."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error al Exportar",
                f"No se pudo generar el archivo CSV:\n{str(e)}"
            )

    def calcularTotalVentas(self):
        """Calcular el total de todas las ventas mostradas"""
        total = 0.0
        for row in range(self._table_model.rowCount()):
            # La columna "Total" es la última (índice 6)
            index = self._table_model.index(row, 6)  # Columna "Total"
            valor = self._table_model.data(index, Qt.DisplayRole)
            if valor:
                try:
                    # Remover símbolos y convertir a float
                    valor_limpio = valor.replace('$', '').replace(',', '').strip()
                    total += float(valor_limpio)
                except ValueError:
                    continue
        return total

    def handleBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.ventas = self.ventaController.buscar(columna, aBuscar)
        except Exception:
            self.labelInformacion.setText("Error al buscar")
            self.ventas = None
        self.lineDato.clear()
        self.mostrarTabla()

    def mostrarTabla(self):
        """Cargar y mostrar las ventas en la tabla"""
        try:
            ventas = self.ventas or self.ventaController.ventas()
            self._table_model.setVentas(ventas)
            self.ventas = None
            # Actualizar label informativo
            self.labelInformacion.setText(f"Mostrando {len(ventas)} ventas")
        except Exception as e:
            self.labelInformacion.setText("Error al cargar ventas")