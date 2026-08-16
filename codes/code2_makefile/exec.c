#include <stdio.h>

int main(void) {
    double total = 0.0;
    for (long i = 1; i < 50000000L; i++) {
        total += 1.0 / (double)i;
    }
    printf("total=%f\n", total);
    return 0;
}
