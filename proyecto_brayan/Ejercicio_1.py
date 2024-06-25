def metodo (tolerancia):
    num_iteraciones = 0
    # Paso 1
    a = 0
    b = 4
    # Bucle para volver al Paso 2 en cada iteración
    while True:
        # Valores necesarios para el calculo del error
        a0 = (a+b)/2
        fa = f(a)
        fb = f(b)
        f0 = f(a0)
        # Se calcula el error
        u = (fa+f0+fb)/3
        error = ((fa-u)**2)+((f0-u)**2)+((fb-u)**2)
        # Paso 2
        if error <= tolerancia:
            # Paso 6
            return a0, f0, num_iteraciones
        else:
            num_iteraciones += 1
            # Paso 3 (No se calcula a0 ni f0 porque fue calculado antes)
            a1 = (a+a0)/2
            a2 = (b+a0)/2
            f1 = f(a1)
            f2 = f(a2)
            # Paso 4
            if f2 > f0 and f0 > f1:
                b = a0
            elif f1 > f0 and f0 > f2:
                a = a0
            elif f1 > f0 and f2 > f0:
                a = a1
                b = a2
            

# Diferentes valores de tolerancia
TOL_1 = 0.001
TOL_2 = 0.0001
TOL_3 = 0.00001

# Función que optimizaremos
def f(x): return 1-((x**2)/2)+((x**4)/24)

x, y, iteraciones = metodo(TOL_1)
print(f"Para una tolerancia de {TOL_1}\nse supera despues de {iteraciones} iteraciones")
print(f"Resultado: ({x}, {y})\n")

x, y, iteraciones = metodo(TOL_2)
print(f"Para una tolerancia de {TOL_2}\nse supera despues de {iteraciones} iteraciones")
print(f"Resultado: ({x}, {y})\n")

x, y, iteraciones = metodo(TOL_3)
print(f"Para una tolerancia de {TOL_3}\nse supera despues de {iteraciones} iteraciones")
print(f"Resultado: ({x}, {y})\n")

# Caso extra
tolerancia = 0.00000000000000000001
x, y, iteraciones = metodo(tolerancia)
print(f"Para una tolerancia de {tolerancia}\nse supera despues de {iteraciones} iteraciones")
print(f"Resultado: ({x}, {y})\n")

# A menor tolerancia, el resultado es mas exacto
# A menor tolerancia, mas iteraciones