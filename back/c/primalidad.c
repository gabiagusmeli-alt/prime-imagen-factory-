#include <gmp.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

// Exportamos el símbolo para ctypes
__attribute__((visibility("default")))
int es_primo(char *numero) {
    mpz_t n;
    mpz_init(n);

    if (mpz_set_str(n, numero, 10) != 0) {
        mpz_clear(n);
        return -1;
    }

    int resultado_global = 1; // asumimos "probablemente primo"

    // Paralelizamos varias pruebas probabilísticas independientes
    #pragma omp parallel
    {
        // Cada hilo mantiene su propio estado de GMP (seguro)
        mpz_t local_n;
        mpz_init_set(local_n, n);

        int local_result = 1; // cada hilo asume primo hasta probar lo contrario

        // Cada hilo ejecuta parte de las 100 iteraciones totales
        #pragma omp for schedule(static)
        for (int i = 0; i < 100; i++) {
            // Si ya se encontró un compuesto, salimos
            if (resultado_global == 0) continue;

            int r = mpz_probab_prime_p(local_n, 1); // una ronda de test
            if (r == 0) {
                #pragma omp critical
                {
                    resultado_global = 0; // número compuesto
                }
            }
        }

        mpz_clear(local_n);
    }

    mpz_clear(n);
    return resultado_global;
}
