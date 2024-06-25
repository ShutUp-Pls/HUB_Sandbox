from PIL import Image

# Cargar la imagen original
original_image_1 = Image.open("C:\\Users\\marqu\\OneDrive\\Pictures\\Screenshots\\Captura de pantalla 2024-05-09 215821.png")

# Crear una miniatura de tamaño 100x100 sin copiar la imagen
thumbnail_1 = original_image_1
thumbnail_1.thumbnail((100, 100))

# Intentar crear otra miniatura de tamaño 200x200 usando la imagen modificada
thumbnail_2 = original_image_1
thumbnail_2.thumbnail((50, 50))

# Mostrar los tamaños de las imágenes
print("Tamaño de thumbnail_1:", thumbnail_1.size)  # Output: (100, 100)
print("Tamaño de thumbnail_2:", thumbnail_2.size)  # Output: (100, 100)

# Cargar la imagen original
original_image_2 = Image.open("C:\\Users\\marqu\\OneDrive\\Pictures\\Screenshots\\Captura de pantalla 2024-05-09 215821.png")

# Crear una miniatura de tamaño 100x100 copiando la imagen original
thumbnail_3 = original_image_2.copy()
thumbnail_3.thumbnail((100, 100))

# Crear otra miniatura de tamaño 200x200 copiando la imagen original
thumbnail_4 = original_image_2.copy()
thumbnail_4.thumbnail((50, 50))

# Mostrar los tamaños de las imágenes
print("Tamaño de thumbnail_3:", thumbnail_3.size)
print("Tamaño de thumbnail_4:", thumbnail_4.size)