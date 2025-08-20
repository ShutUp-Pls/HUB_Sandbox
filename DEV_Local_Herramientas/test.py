def formatear_numero(numero):
    # Convertir el número a float para procesar ceros a la izquierda
    try:
        numero_float = float(numero)
    except ValueError:
        return "Entrada no válida"

    # Convertir a entero si no hay decimales significativos
    if numero_float.is_integer():
        numero_entero = int(numero_float)
        return f"{numero_entero:,}".replace(",", ".")
    
    # Si tiene decimales, mantener solo la parte significativa
    return f"{numero_float:,.0f}".replace(",", ".")

# Ejemplos de uso:
print(formatear_numero("1890.00"))  # "1.890"
print(formatear_numero(200.00))     # "200"
print(formatear_numero("2290"))     # "2.290"
print(formatear_numero(33.33))      # "33"
print(formatear_numero(790))        # "790"
print(formatear_numero("00456.00")) # "456"
