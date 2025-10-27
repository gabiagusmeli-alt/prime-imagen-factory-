from PIL import Image

def promedio_matriz (x1 : int,x2 : int ,y1 : int, y2 : int ,arr : list) -> int:
    promedio = 0

    for i in range (x1,x2):
        for j in range(y1,y2):
            promedio += arr[i][j]
    return int(promedio / ((x2 - x1 )*(y2-y1)))


def tomar_imagen ( im : str) -> list:
    with Image.open (im) as imagen:

        #ahora la recortamos para que sea cuadrada

        if (imagen.size[0]<imagen.size[1]):
            coordena_0 = 0
            coordenada_1 = (0.5*imagen.size[1]) - (0.5*imagen.size[0])
            coordenada_2 = imagen.size[0]
            coordenada_3 = (0.5*imagen.size[1] + (0.5*imagen.size[0]))
            box = (coordena_0,coordenada_1,coordenada_2,coordenada_3)
            imagen_centrada = imagen.crop(box)

        elif (imagen.size[0] >= imagen.size[1]):
            coordena_0 = (0.5*imagen.size[0]) - (0.5*imagen.size[1])
            coordenada_1 = 0
            coordenada_2 = (0.5*imagen.size[0] + (0.5*imagen.size[1]))
            coordenada_3 = imagen.size[1]
            box = (coordena_0,coordenada_1,coordenada_2,coordenada_3)
            imagen_centrada = imagen.crop(box)

        
        #la convertimos a escala de grises 
        imagen_centrada = imagen_centrada.convert("L")
        
        #ahora lo que queremos hacer es hacer que la cantidad de pixeles sea multiplo de 50, como ya sabemos que la imagen es cuadrada, lo primero que hacemos es 
        #calcular cuantos pixeles le falta para que la imagen llegue a un ,multiplo de 50
        
        nuevo_tam = imagen_centrada.size[1]
        #cuando termine este ciclo voy a tener lo que busco a tamaño multiplo de 50

        while(nuevo_tam % 50) != 0 :
            nuevo_tam += 1

        #ahora la reescalamos a lo que buscamos

        imagen_procesada =  imagen_centrada.resize((nuevo_tam, nuevo_tam), Image.Resampling.LANCZOS)

        #ahora voy a crear la matriz n x n donde voy a guardar los valores y uno con otodos los pixeles


        array_temporal = [[imagen_procesada.getpixel((i,j)) for i in range (0,imagen_procesada.size[1])]for j in range (0,imagen_procesada.size[1])]


        #ahora voy a almmacenar en ina variabble que tada cuantos pixeles tengno que ir avanzando ne la matriz

        tam_iteracion = int(nuevo_tam // 50)
        #vamos ahora a calcular el promedio pero vamos a usar una funcion  auxiliar 



        array_final = [[promedio_matriz(i * tam_iteracion,(i *tam_iteracion)+tam_iteracion, j*tam_iteracion,(j*tam_iteracion)+tam_iteracion,array_temporal) for i in range (0,int(imagen_procesada.size[1]/tam_iteracion))] for j in range(0,int(imagen_procesada.size[1]/tam_iteracion))]

        return array_final
