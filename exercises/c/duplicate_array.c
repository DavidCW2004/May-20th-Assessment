#include "duplicate_array.h"
#include <stdio.h>   
#include <stdlib.h>

int *duplicate_array(const int *values, size_t n) {
    int* arr = malloc(n * sizeof(values[0]));

    for(size_t i = 0; i < n; i++) {
        arr[i] = values[i];
    }

    return arr;
}
