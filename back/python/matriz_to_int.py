import random as random 

#definimos los numeros por la cantidad pixeles negros que muestra en pantalla  donde 0 es el que menos tiene y 4 el que mas
grupo_0 = [7,1]
grupo_1 = [2,4]
grupo_2 = [3,5,9]
grupo_3 = [8,0,6]
grupo_impar = [1,3,5,7,9]


def matrix_to_integer (arr : list) -> int :
    #definimos un string 
    numero = ""
    
    for i in range(0,len(arr)) :
        for j in range(0,len(arr)):
            if (arr [j][i] <= 64):
                numero += str(random.choice(grupo_0))
            elif(arr [j][i] > 64 and arr [j][i] <= 2*64):
                numero += str(random.choice(grupo_1))
            elif(arr [j][i] < 2*64 and arr [j][i] <= 3*64):
                numero += str(random.choice(grupo_2))
            else :
                numero += str(random.choice(grupo_2))
        if len(numero) > 0 and int(numero[-1]) not in grupo_impar:
            numero = numero[:-1] + str(random.choice(grupo_impar))
    return (numero)
