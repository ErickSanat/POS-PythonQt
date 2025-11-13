import os
from pathlib import Path
from PyQt5.QtGui import QPainter, QImage, QFont
from PyQt5.QtPrintSupport import QPrinter

def generarTicket(nombre_pdf, detalleVenta):
    try:
        # ✅ Ruta correcta base /app
        base_dir = Path(__file__).resolve().parent.parent
        ruta_logo = base_dir / "assets" / "Iconos" / "logo.png"

        print("DEBUG - Ruta imagen:", ruta_logo)

        imagen = QImage(str(ruta_logo))
        if imagen.isNull():
            print("❌ Imagen NO cargada")
        else:
            print("✅ Imagen cargada correctamente")

        # ✅ Crear PDF
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(nombre_pdf)

        painter = QPainter()
        painter.begin(printer)

        # ======== ESTILOS ========
        font_big = QFont("Arial", 12, QFont.Bold)
        font_normal = QFont("Arial", 9)
        font_small = QFont("Arial", 8)

        # ======== LOGO ========
        if not imagen.isNull():
            painter.drawImage(100, 20, imagen.scaled(90, 90))  # ✅ Más pequeño y nítido

        y = 130

        # ======== ENCABEZADO ========
        painter.setFont(font_big)
        painter.drawText(70, y, "PASTELERÍA ALQUIMIA")
        y += 30

        painter.setFont(font_normal)
        painter.drawText(100, y, "Tizayork")
        y += 25

        painter.drawText(60, y, f"Cliente: {detalleVenta[0].venta.cliente.nombre}")
        y += 20
        painter.drawText(60, y, f"Fecha: {detalleVenta[0].venta.fecha.strftime('%d/%m/%Y %H:%M')}")
        y += 20
        painter.drawText(60, y, f"ID Venta: {detalleVenta[0].venta.id_venta}")
        y += 30

        # ======== LÍNEA ========
        painter.drawLine(40, y, 380, y)
        y += 25

        # ======== TABLA ========
        painter.setFont(font_small)
        painter.drawText(40, y, "Producto")
        painter.drawText(160, y, "Cant.")
        painter.drawText(220, y, "P.Unit")
        painter.drawText(300, y, "Subtotal")
        y += 15
        painter.drawLine(40, y, 380, y)
        y += 25

        total = 0

        for d in detalleVenta:
            painter.drawText(40, y, d.producto.nombre[:12])
            painter.drawText(160, y, str(d.cantidad))
            painter.drawText(220, y, f"${d.producto.precio:.2f}")
            painter.drawText(300, y, f"${d.subtotal:.2f}")
            y += 20
            total += d.subtotal

        y += 10
        painter.drawLine(40, y, 380, y)
        y += 35

        # ======== TOTAL ========
        painter.setFont(font_big)
        painter.drawText(210, y, f"TOTAL: ${total:.2f}")

        y += 50

        # ======== MENSAJE FINAL ========
        painter.setFont(font_small)
        painter.drawText(120, y, "¡Gracias por su compra!")

        painter.end()
        print(f"✅ Ticket generado correctamente: {nombre_pdf}")

    except Exception as e:
        print("❌ Error al generar el ticket:", e)
