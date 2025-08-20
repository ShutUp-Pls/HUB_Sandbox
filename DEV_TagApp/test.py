import win32gui
import win32ui
import win32print
from PIL import Image, ImageWin


def print_image_with_same_size(image_path, dpi=300):
    """
    Imprime la imagen dada por 'image_path' ajustando el tamaño de la página
    al tamaño (en pulgadas) de la imagen, asumiendo un DPI de 300 por defecto.
    """

    # 1) Cargar la imagen con Pillow
    img = Image.open(image_path)

    # 2) Calcular el tamaño en pulgadas
    width_in = img.width / dpi
    height_in = img.height / dpi

    # 3) Convertir a décimas de milímetro (PaperWidth, PaperLength)
    #    1 pulgada = 25.4 mm => *10 => décimas de mm
    width_mm_10 = int(width_in * 25.4 * 10)
    height_mm_10 = int(height_in * 25.4 * 10)

    # 4) Nombre de la impresora
    printer_name = win32print.GetDefaultPrinter()
    # printer_name = "Tu impresora"  # si quieres otra distinta a la predeterminada

    # 5) Abrir la impresora y obtener el devmode
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        printer_info = win32print.GetPrinter(hPrinter, 2)  # level=2 -> info detallada
        devmode = printer_info['pDevMode']

        # 6) Configurar devmode para papel personalizado (DMPAPER_USER = 256)
        devmode.PaperSize = 256
        devmode.PaperWidth = width_mm_10
        devmode.PaperLength = height_mm_10

        # 7) Crear el HDC nativo usando win32gui.CreateDC
        #    (driver = "WINSPOOL", device = printer_name, output = None, initData = devmode)
        hDC = win32gui.CreateDC("WINSPOOL", printer_name, None, devmode)

        # 8) Convertir ese handle en un PyCDC (dc) con CreateDCFromHandle
        dc = win32ui.CreateDCFromHandle(hDC)

        # 9) Iniciar impresión
        dc.StartDoc(image_path)
        dc.StartPage()

        # 10) Obtener área imprimible (HORZRES = 110, VERTRES = 111)
        printable_width = dc.GetDeviceCaps(110)
        printable_height = dc.GetDeviceCaps(111)

        # 11) Dibujar la imagen
        dib = ImageWin.Dib(img)
        dib.draw(dc.GetHandleOutput(), (0, 0, printable_width, printable_height))

        # 12) Finalizar
        dc.EndPage()
        dc.EndDoc()

        # 13) Liberar DC
        dc.DeleteDC()

    finally:
        # Cerrar la impresora
        win32print.ClosePrinter(hPrinter)


if __name__ == "__main__":
    # Prueba con tu imagen
    ruta_imagen = r"page_0.png"
    print_image_with_same_size(ruta_imagen, dpi=300)
