from back.python.matriz_to_int import *
from back.python.procesamiento_imagen import *
from back.python.iteracion import *
from ctypes import CDLL, c_char_p, c_int
import os

# En PROYECTO_IMAGEN_PRIMO/python/main.py


# 1. Obtiene la ruta del directorio donde se encuentra este script (main.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Construye la ruta completa a libprimo.so en ese mismo directorio
#    Esta es la ruta relativa/absoluta correcta:
lib_path = os.path.join(script_dir, "libprimo.so")

# Cargar la librería usando la ruta construida
lib_primalidad = CDLL(lib_path) # ✅ Correcto

lib_primalidad.es_primo.argtypes = [c_char_p]
lib_primalidad.es_primo.restype = c_int

# ... (el resto de tu función main)

# Procesar la imagen
def main (imagen : str)-> str:
    matriz = tomar_imagen(imagen)
    matriz_intercambiada = matrix_to_integer(matriz)

    prime = lib_primalidad.es_primo(matriz_intercambiada.encode('utf-8'))
    iteracion = 0

    #par = (int(matriz_intercambiada)%2)
    while prime not in (1, 2):
        matriz_intercambiada = iterar(matriz_intercambiada)
        prime = lib_primalidad.es_primo(matriz_intercambiada.encode('utf-8'))
    return matriz_intercambiada


    
