#include "rectangle.hpp"

Rectangle::Rectangle(int left, int top, int width, int height)
    : left(left), top(top), width(width), height(height) {}

int Rectangle::area() const {
    return width * height;
}

bool Rectangle::contains(int x, int y) const {
    if (x >= left && x < left + width && y <= top && y > top - height) {
        return true;
    }

    return false;
}

int Rectangle::get_left() const {
    return left;
}

int Rectangle::get_top() const {
    return top;
}

int Rectangle::get_width() const {
    return width;
}

int Rectangle::get_height() const {
    return height;
}
