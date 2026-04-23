#ifndef RECTANGLE_HPP
#define RECTANGLE_HPP

class Rectangle {
private:
    int left;
    int top;
    int width;
    int height;

public:
    Rectangle(int left, int top, int width, int height);

    int area() const;
    /* Uses standard Cartesian coordinates: top is the largest y value. */
    bool contains(int x, int y) const;

    int get_left() const;
    int get_top() const;
    int get_width() const;
    int get_height() const;
};

#endif
