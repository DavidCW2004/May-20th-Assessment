#include "duplicate_array.h"

#include <assert.h>
#include <stdlib.h>

static void test_copies_values_into_new_memory(void) {
    int input[] = {3, 1, 4, 1, 5};
    int *copy = duplicate_array(input, 5);

    assert(copy != NULL);
    assert(copy != input);

    for (size_t i = 0; i < 5; i++) {
        assert(copy[i] == input[i]);
    }

    copy[0] = 99;
    assert(input[0] == 3);

    free(copy);
}

static void test_zero_length_is_allowed(void) {
    int input[] = {42};
    int *copy = duplicate_array(input, 0);

    /* free(NULL) is valid, so either NULL or malloc(0) is acceptable. */
    free(copy);
}

int main(void) {
    test_copies_values_into_new_memory();
    test_zero_length_is_allowed();
    return 0;
}
