def ejemplo():
    try:
        # Tu código aquí
        return "Valor de retorno desde try"
    except Exception as e:
        # Manejo de la excepción
        print("Se produjo una excepción:", e)
    finally:
        # Esto se ejecutará siempre
        print("Bloque finally ejecutándose")

print(ejemplo())
