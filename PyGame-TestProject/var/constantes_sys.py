### --- NOMBRE DEL PROYECTO Y VERSION --- ###
NAME_PROJECT = "UrbanQuest InDev(0.0.0)"

### --- COLORES --- ###
# Definición Blanco y Negro
CLR_BLACK = (0, 0, 0)
CLR_WHITE = (255, 255, 255)
# Definición RGB
CLR_RED = (255, 0, 0)
CLR_GREEN = (0, 255, 0)
CLR_BLUE = (0, 0, 255)

### --- RESOLUCIONES --- ###
class RSL_PANTALLA:
    def __init__(self, ancho, alto):
        self.width = ancho
        self.height = alto
        self.width_mid = ancho // 2
        self.height_mid = alto // 2
        self.tuple = (ancho, alto)
        self.tupla_mid = (self.width_mid, self.height_mid)

    def __repr__(self):
        return f"Resolucion(ancho={self.width}, alto={self.height})"