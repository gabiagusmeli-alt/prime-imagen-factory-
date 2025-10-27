from back.python.matriz_to_int import *
from back.python.procesamiento_imagen import *
from back.python.iteracion import *
from ctypes import CDLL, c_char_p, c_int
from back.python.comparacion import *
import os



# 1. Obtiene la ruta del directorio donde se encuentra este script (main.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Construye la ruta completa a libprimo.so en ese mismo directorio
#    Esta es la ruta relativa/absoluta correcta:
lib_path = os.path.join(script_dir, "libprimo.so")

# Cargar la librería usando la ruta construida
lib_primalidad = CDLL(lib_path) # ✅ Correcto

lib_primalidad.siguiente_primo_paralelo.argtypes = [c_char_p]
lib_primalidad.siguiente_primo_paralelo.restype = c_char_p


# Procesar la imagen
def main (imagen : str)-> str:
    matriz = tomar_imagen(imagen)
    matriz_intercambiada = matrix_to_integer(matriz)

    prime = True
    nuevo_primo = lib_primalidad.siguiente_primo_paralelo(matriz_intercambiada.encode('utf-8'))

    while not prime :
        prime = comparar(matriz_intercambiada,nuevo_primo)
        if prime :
            matriz_intercambiada = nuevo_primo
        else :
            nuevo_primo = lib_primalidad.siguiente_primo_paralelo(nuevo_primo.encode('utf-8'))

    return matriz_intercambiada


    
