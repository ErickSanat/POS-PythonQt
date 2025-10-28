import sys
from ..model import DetalleVenta
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument


def generarTicket(nombre_archivo, detalleVenta: list[DetalleVenta] = None):
    """
    Genera un ticket de compra en formato PDF utilizando PyQt5.

    Args:
        nombre_archivo (str): El nombre del archivo PDF a crear.
        datos_compra (dict): Un diccionario con la información del ticket.
    """

    # -------------------
    # Generar el HTML del ticket
    # -------------------

    # Estilos CSS para el ticket
    estilos_css = """
    <style>
        body { font-family: Arial, sans-serif; font-size: 10pt; }
        .ticket { width: 300px; margin: 0 auto; padding: 15px; border: 1px solid black;}
        .header { text-align: center; border-bottom: 1px dashed black; padding-bottom: 10px; }
        .header h1 { font-size: 14pt; margin: 0; }
        .details { margin: 15px 0; font-size: 9pt; }
        .item-list { width: 100%; border-collapse: collapse; }
        .item-list th, .item-list td { padding: 4px 0; text-align: left; }
        .item-list th { border-bottom: 1px solid black; font-size: 9pt; }
        .item-list td { font-size: 8pt; }
        .total { text-align: right; font-weight: bold; margin-top: 15px; }
        .footer { text-align: center; margin-top: 20px; font-size: 8pt; color: #555; }
    </style>
    """

    # Generar el HTML para la lista de productos
    tabla_productos_html = ""
    total_general = detalleVenta[0].venta.total
    for detalle in detalleVenta:
        tabla_productos_html += f"""
        <tr>
            <td>{detalle.producto.nombre}</td>
            <td>{detalle.cantidad}</td>
            <td>${detalle.producto.precio:.2f}</td>
            <td>${detalle.subtotal:.2f}</td>
        </tr>
        """

    # Generar el HTML completo del ticket
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Ticket de Compra</title>
        {estilos_css}
    </head>
    <body>
        <div class="ticket">
            <div class="header">
                <h1>Pasteleria Alquimia</h1>
                <p>Dirección: Tizayork</p>
                <p>Fecha: {detalleVenta[0].venta.fecha.strftime('%d/%m/%Y %H:%M')}</p>
            </div>

            <div class="details">
                <strong>Cliente:</strong> {detalleVenta[0].venta.cliente.nombre}<br>
                <strong>ID de compra:</strong> {detalleVenta[0].venta.id_venta}<br>
            </div>

            <table class="item-list">
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Cant.</th>
                        <th>Precio unit.</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {tabla_productos_html}
                </tbody>
            </table>

            <div class="total">
                <span>TOTAL: ${total_general:.2f}</span>
            </div>

            <div class="footer">
                <p>¡Gracias por su compra!</p>
            </div>
        </div>
    </body>
    </html>
    """

    # -------------------
    # Convertir HTML a PDF con PyQt5
    # -------------------

    # Crear el documento de texto
    document = QTextDocument()
    document.setHtml(html_content)

    # Configurar el objeto QPrinter para generar un archivo PDF
    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(nombre_archivo)

    # Imprimir el documento a PDF
    document.print_(printer)

    print(f"¡Ticket de compra '{nombre_archivo}' generado con éxito usando PyQt5!")
