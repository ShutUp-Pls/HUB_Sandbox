import fitz  # PyMuPDF

def resize_pdf(input_pdf_path, output_pdf_path):
    # Dimensiones de A5 en puntos (1 punto = 1/72 pulgadas)
    A5_WIDTH = 148 * 72 / 25.4
    A5_HEIGHT = 210 * 72 / 25.4
    
    # Abrir el PDF de entrada
    document = fitz.open(input_pdf_path)
    
    # Crear un nuevo documento para el PDF reescalado
    new_document = fitz.open()
    
    for page_num in range(len(document)):
        # Obtener la página actual
        page = document.load_page(page_num)
        
        # Crear una nueva página en el nuevo documento con el tamaño de A5
        new_page = new_document.new_page(width=A5_WIDTH, height=A5_HEIGHT)
        
        # Obtener la matriz de transformación para escalar la página al tamaño de A5
        scale_x = A5_WIDTH / page.rect.width
        scale_y = A5_HEIGHT / page.rect.height
        matrix = fitz.Matrix(scale_x, scale_y)
        
        # Aplicar la transformación al contenido de la página y volcarlo en la nueva página
        new_page.show_pdf_page(new_page.rect, document, page_num, clip=page.rect, transform=matrix)
    
    # Guardar el nuevo PDF
    new_document.save(output_pdf_path)
    new_document.close()
    document.close()

# Ejemplo de uso
resize_pdf('PDF_Tools\\Guia_Ejercicios_1.pdf', 'output_a5.pdf')
