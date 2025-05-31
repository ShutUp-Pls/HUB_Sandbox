from datetime import date

# Definir fechas
fecha_inicio = date(2025, 3, 7)
fecha_fin = date(2025, 3, 31)

# Calcular diferencia en días
dias_diferencia = (fecha_fin - fecha_inicio).days

print(f"Días entre {fecha_inicio} y {fecha_fin}: {dias_diferencia}")