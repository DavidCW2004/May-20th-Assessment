#include "rectangle.hpp"

#include <cassert>

static void test_area_is_width_times_height(void) {
    Rectangle rect(10, 20, 4, 3);

    assert(rect.get_left() == 10);
    assert(rect.get_top() == 20);
    assert(rect.get_width() == 4);
    assert(rect.get_height() == 3);
    assert(rect.area() == 12);
}

static void test_contains_uses_half_open_edges(void) {
    Rectangle rect(10, 20, 4, 3);

    assert(rect.contains(10, 20));
    assert(rect.contains(13, 18));
    assert(!rect.contains(14, 18));
    assert(!rect.contains(13, 21));
    assert(!rect.contains(13, 17));
    assert(!rect.contains(9, 20));
}

int main() {
    test_area_is_width_times_height();
    test_contains_uses_half_open_edges();
}
