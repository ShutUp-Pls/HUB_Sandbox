import pandas as pd # Para extraer los datos del .xlsx facilmente
import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo Excel con pandas
data = pd.read_excel('Data.xlsx')

# Extraer los valores de voltajes y corrientes
voltajes = data.iloc[:, :3]
corrientes = data.iloc[:, 3:6]

# Función para calcular los valores pedidos (rms, valor medio, peak maximo, peak minimo)
def calcular_valores(signal):
    rms = np.sqrt(np.mean(signal**2)) # (Al interior de la raiz hay un calculo promedio de los valores al cuadrado)
    valor_medio = np.mean(signal)
    peak_max = np.max(signal)
    peak_min = np.min(signal)
    return rms, valor_medio, peak_max, peak_min

# Graficar los voltajes en un solo gráfico
plt.figure(figsize=(12, 8)) # Cambiar tamaño de la figura a gusto personal
for i in range(3):
    plt.plot(voltajes.index, voltajes.iloc[:, i], label=f'Fase {i+1}')
    rms, valor_medio, peak_max, peak_min = calcular_valores(voltajes.iloc[:, i])
    # .2f para indicar que se muestres solo 2 decimales
    plt.text(0.02, 0.95-i*0.05,
             f'Fase {i+1} - RMS: {rms:.2f}, Valor Medio: {valor_medio:.2f}, Peak Maximo: {peak_max:.2f}, Peak Minimo: {peak_min:.2f}',
             transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.6) # Agregamos una caja para visualizar mejor las etiquetas
             )

# Etiquetas, leyendas y textos
plt.title('Voltajes del Sistema Trifásico')
plt.xlabel('Muestras')
plt.ylabel('Voltaje (V)')
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.show()

# Graficar las corrientes en gráficos independientes
# "fig" no lo usamos pero es necesario porque plt.subplots devuelve 2 parametros y axs funciona como lista
fig, axs = plt.subplots(3, 1, figsize=(12, 12)) 
for i in range(3):
    axs[i].plot(corrientes.index, corrientes.iloc[:, i], label=f'Fase {i+1}')
    rms, valor_medio, peak_max, peak_min = calcular_valores(corrientes.iloc[:, i])
    # .2f para indicar que se muestres solo 2 decimales
    axs[i].text(0.02, 0.95, f'RMS: {rms:.2f}, Mean: {valor_medio:.2f}, Max: {peak_max:.2f}, Min: {peak_min:.2f}',
                transform=axs[i].transAxes, bbox=dict(facecolor='white', alpha=0.6)) # Agregamos una caja para visualizar mejor las etiquetas
    
    # Etiquetas, leyendas y textos
    axs[i].set_title(f'Corriente de la Fase {i+1}')
    axs[i].set_xlabel('Muestras')
    axs[i].set_ylabel('Corriente (A)')
    axs[i].legend(loc='upper right')
    axs[i].grid(True)

plt.tight_layout()
plt.subplots_adjust(hspace=0.4) # Para que no se superpongan "xlabel" con "title"
plt.show()
