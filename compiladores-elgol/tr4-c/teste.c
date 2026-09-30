/* teste.c - arquivo de entrada para o analisador */
#include <stdio.h>

int fatorial(int n) {
    int resultado = 1;
    while (n > 1) {
        resultado *= n;
        n = n - 1;
    }
    return resultado;
}

int main(void) {
    float media = 3.5e2;      // constante em notacao cientifica
    char letra = 'A';
    int mascara = 0xFF;
    if (media >= 100.0 && mascara != 0) {
        printf("ok %d\n", fatorial(5));
    } else {
        media = media / 2;
    }
    return 0;
}
