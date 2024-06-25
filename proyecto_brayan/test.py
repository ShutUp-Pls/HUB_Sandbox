from graphviz import Digraph

# Crear un objeto Digraph
dot = Digraph(comment='Metodo')

# Nodo inicial
dot.node('Inicio', 'Inicio')

# Paso 1
dot.node('Paso1', 'Paso 1: Inicialización\na = 0, b = 4, num_iteraciones = 0')

# Bucle principal
dot.node('Bucle', 'Bucle')

# Paso 2
dot.node('Paso2', 'Paso 2: Calcular a0, fa, fb, f0\ny el error')

# Verificar tolerancia
dot.node('Verificar', 'Error <= Tolerancia?')

# Paso 6
dot.node('Paso6', 'Paso 6: Retornar a0, f0, num_iteraciones')

# Incrementar iteraciones
dot.node('Incrementar', 'Incrementar num_iteraciones')

# Paso 3
dot.node('Paso3', 'Paso 3: Calcular a1, a2, f1, f2')

# Paso 4
dot.node('Paso4', 'Paso 4: Actualizar a y b\nsegún las condiciones')

# Conexiones
dot.edges(['Inicio' + 'Paso1', 'Paso1' + 'Bucle', 'Bucle' + 'Paso2'])
dot.edge('Paso2', 'Verificar')
dot.edge('Verificar', 'Paso6', label='Sí')
dot.edge('Verificar', 'Incrementar', label='No')
dot.edge('Incrementar', 'Paso3')
dot.edge('Paso3', 'Paso4')
dot.edge('Paso4', 'Bucle')

# Guardar y visualizar el diagrama
dot.render('metodo_diagrama', format='png', view=True)
