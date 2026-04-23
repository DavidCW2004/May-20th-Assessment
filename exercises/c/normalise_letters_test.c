#include "normalise_letters.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static void test_removes_non_letters_and_lowercases(void) {
    char *result = normalise_letters("Hello, WORLD! 123");

    assert(result != NULL);
    assert(strcmp(result, "helloworld") == 0);

    free(result);
}

static void test_empty_result_is_valid(void) {
    char *result = normalise_letters("1234!?");

    assert(result != NULL);
    assert(strcmp(result, "") == 0);

    free(result);
}

int main(void) {
    test_removes_non_letters_and_lowercases();
    test_empty_result_is_valid();
    return 0;
}
