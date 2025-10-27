grupo_0 = [1, 7]
grupo_1 = [2, 4]
grupo_2 = [3, 5, 9]
grupo_3 = [0, 6, 8]
grupo_impar = [1, 3, 5, 7, 9]
#esta funcion solo toma dos str y se fija si los elementos en el indice i estan en en el mismo grupo y que el 25 porciento del numero cumola


def comparar (first : str, second:str ) -> bool:
    coincidencias = 0
    no_coincidencias = 0
    i = 0
    while no_coincidencias < 0.06*len(first) and i < len (first)-1  :
        if i in grupo_0 and second[i] in grupo_0 :
            coincidencias += 1
        elif i in grupo_1 and second[i] in grupo_1:
            coincidencias += 1 
        elif i in grupo_2 and second[i] in grupo_2:
            coincidencias += 1 
        elif i in grupo_3 and second[i] in grupo_3:
            coincidencias += 1 
        elif i in grupo_impar and second[i] in grupo_impar:
            coincidencias += 1 
        else :
            no_coincidencias += 1
        i += 1
    return no_coincidencias < 0.06 * len(first)