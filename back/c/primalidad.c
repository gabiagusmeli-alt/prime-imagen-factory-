#include <gmp.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h> // Necesario para la función que devuelve el string

// Definición de una estructura para pasar el resultado (el número primo) de vuelta
typedef struct {
    mpz_t primo_encontrado;
    int encontrado;
} ResultadoPrimo;

// Exportamos el símbolo para ctypes
__attribute__((visibility("default")))
char* siguiente_primo_paralelo(char *numero_str) {
    mpz_t n;
    mpz_init(n);

    // 1. Convertir la cadena de entrada a mpz_t
    if (mpz_set_str(n, numero_str, 10) != 0) {
        mpz_clear(n);
        // Devuelve una cadena de error en caso de fallo de conversión
        return strdup("Error de conversión de número");
    }

    // Inicializar el candidato, que será n + 1 (o n si ya es par)
    mpz_t candidato;
    mpz_init_set(candidato, n);

    // Si el número de entrada es 2, el siguiente es 3
    if (mpz_cmp_ui(n, 2) == 0) {
        mpz_clear(n);
        mpz_clear(candidato);
        return strdup("3");
    }

    // Si el número de entrada es par (y > 2), empezamos desde n+1 (impar)
    if (mpz_even_p(candidato)) {
        mpz_add_ui(candidato, candidato, 1);
    } else {
        // Si es impar, empezamos desde n+2
        mpz_add_ui(candidato, candidato, 2);
    }
    
    // Almacena el número primo encontrado (solo el que se encontró primero)
    // Se usa un array de 1 porque las estructuras no se pueden compartir con #pragma omp threadprivate
    ResultadoPrimo resultado[1];
    mpz_init(resultado[0].primo_encontrado);
    resultado[0].encontrado = 0; // Bandera para indicar si ya se encontró el primo

    int step = omp_get_max_threads() * 2; // El salto debe ser múltiplo de 2 (probando solo impares)
    
    // 2. Búsqueda paralela
    #pragma omp parallel 
    {
        mpz_t local_candidato;
        mpz_init(local_candidato);

        int local_encontrado = 0;
        int thread_id = omp_get_thread_num();

        // 2a. Asignar el punto de partida al hilo
        // (candidato + 2 * thread_id) para repartir los números impares a probar
        mpz_set(local_candidato, candidato);
        mpz_add_ui(local_candidato, local_candidato, thread_id * 2);

        // 2b. Bucle de búsqueda (los hilos salen en cuanto la bandera global es 1)
        while (resultado[0].encontrado == 0) {
            
            // Si el candidato actual es primo (o 'probablemente primo')
            // El segundo argumento es el número de iteraciones de Miller-Rabin. Usamos un valor alto para certeza.
            if (mpz_probab_prime_p(local_candidato, 25) > 0) {
                
                // 2c. Se encontró un primo, actualiza el resultado global de forma segura
                #pragma omp critical
                {
                    // Solo actualiza si aún no se ha encontrado un primo
                    if (resultado[0].encontrado == 0) {
                        mpz_set(resultado[0].primo_encontrado, local_candidato);
                        resultado[0].encontrado = 1;
                    }
                }
                
                // Si el primo encontrado es el más pequeño (el del hilo 0), los demás hilos
                // con candidatos mayores no deberían hacer nada, pero la bandera global
                // los sacará del while en la siguiente iteración.
            }
            
            // 2d. Avanzar al siguiente candidato (salto de 2 * num_hilos para probar el siguiente impar)
            mpz_add_ui(local_candidato, local_candidato, step);
        }

        mpz_clear(local_candidato);
    }

    // 3. Convertir el resultado a cadena C y liberar la memoria GMP
    // La función mpz_get_str retorna un puntero a un string que DEBE ser liberado por el llamador.
    // Usamos strdup para garantizar que el puntero devuelto sea seguro para ctypes y no la memoria interna de GMP.
    char *resultado_str = mpz_get_str(NULL, 10, resultado[0].primo_encontrado);
    
    // Se libera la memoria GMP local
    mpz_clear(n);
    mpz_clear(candidato);
    mpz_clear(resultado[0].primo_encontrado);

    // Se libera la memoria asignada por mpz_get_str y se duplica para devolver una copia
    char *primo_final = strdup(resultado_str);
    free(resultado_str);

    return primo_final; // El llamador DEBE liberar este puntero (e.g., free())
}