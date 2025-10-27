# Definimos los grupos según la cantidad de píxeles negros:
# 0 → menos píxeles, 4 → más píxeles
grupo_0 = [1, 7]
grupo_1 = [2, 4]
grupo_2 = [3, 5, 9]
grupo_3 = [0, 6, 8]
grupo_impar = [1, 3, 5, 7, 9]


# ------------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------------

def is_last(digito: int) -> bool:
    """Devuelve True si el dígito es el mayor de su conjunto."""
    return digito in (7, 4, 9, 8)


def next_conjunto(n: int) -> int:
    """Devuelve el siguiente número dentro del grupo correspondiente."""
    for grupo in (grupo_0, grupo_1, grupo_2, grupo_3):
        if n in grupo:
            i = grupo.index(n)
            return grupo[(i + 1) % len(grupo)]
    return n


def next_conjunto_final(n: int) -> int:
    """Devuelve el siguiente número dentro del grupo de impares."""
    if n in grupo_impar:
        i = grupo_impar.index(n)
        return grupo_impar[(i + 1) % len(grupo_impar)]
    return n


# ------------------------------------------------------------
# Función principal de iteración
# ------------------------------------------------------------

def iterar(numero: str, n: int = -1) -> str:
    """
    Recorre el número de atrás hacia adelante.
    Si el dígito actual es el mayor de su grupo, lo reemplaza por el menor
    y pasa al siguiente dígito (hacia la izquierda).
    Caso contrario, lo reemplaza por el siguiente en su grupo.
    """
    digitos = [int(c) for c in numero]

    # Si n = -1, empezamos desde el último dígito
    if n == -1:
        n = len(digitos) - 1

    if n < 0:
        # caso base: terminamos la iteración
        return ''.join(map(str, digitos))

    if is_last(digitos[n]):
        # reemplazar por el siguiente (vuelve al primero del grupo)
        digitos[n] = next_conjunto(digitos[n])
        # avanzar al siguiente dígito hacia la izquierda
        return iterar(''.join(map(str, digitos)), n - 1)
    else:
        # reemplazar y terminar
        digitos[n] = next_conjunto(digitos[n])
        return ''.join(map(str, digitos))
