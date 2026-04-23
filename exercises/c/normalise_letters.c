#include "normalise_letters.h"
#include <stdio.h>   
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

char *normalise_letters(const char *src) {
    char* arr = malloc(sizeof(src));

    int j = 0;
    for(size_t i = 0; i < strlen(src); i++) {
        if (tolower(src[i]) >= 'a' && tolower(src[i]) <= 'z') {
            arr[j] = tolower(src[i]);
            j++;
        }
    }

    arr[j] = '\0';

    return arr;
}
