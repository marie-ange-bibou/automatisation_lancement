#include <stdio.h>

int is_prime(int n) {
    if (n < 2) return 0;
    for (int i = 2; (long)i * i <= n; i++) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int main(void) {
    int count = 0;
    for (int i = 2; i < 2000000; i++) {
        if (is_prime(i)) count++;
    }
    printf("primes=%d\n", count);
    return 0;
}
