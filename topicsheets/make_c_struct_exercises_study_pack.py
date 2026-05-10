from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
)


OUT = Path(__file__).with_name("c-struct-exercises-study-pack.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TopicTitle", parent=styles["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#111827"), spaceAfter=8))
    styles.add(ParagraphStyle("TopicBody", parent=styles["Normal"], fontSize=9.3, leading=12, textColor=colors.HexColor("#111827"), spaceAfter=6))
    styles.add(ParagraphStyle("SourceText", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#4b5563"), spaceAfter=6))
    styles.add(ParagraphStyle("BlueHeading", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#1d4ed8"), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle("DarkHeading", parent=styles["Heading3"], fontSize=11, leading=13, textColor=colors.HexColor("#111827"), spaceBefore=6, spaceAfter=3))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.3, leading=9.0, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=7))
    return styles


def p(text, styles, style="TopicBody"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=88)


def bullets(items, styles):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=4 * mm) for item in items],
        bulletType="bullet",
        leftIndent=6 * mm,
        bulletFontName="Helvetica",
        bulletFontSize=7,
    )


def numbered(items, styles, start=1):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=5 * mm) for item in items],
        bulletType="1",
        leftIndent=7 * mm,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=8,
        start=start,
    )


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="C Struct Exercises Study Pack",
    )

    story = [
        p("C Struct Exercises: Points and Rectangles", styles, "TopicTitle"),
        p(
            "Based on ECM2433 CA0 and L07 struct material. Practises defining structs with "
            "typedef, initialising and accessing fields, writing functions that take struct "
            "parameters, pass-by-value vs pass-by-pointer, and modelling geometric types.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),

        # --- Section 1: typedef struct ---
        p("1. Quick recap: typedef struct", styles, "DarkHeading"),
        p(
            "The <font face=\"Courier\">typedef</font> form lets you use the short name "
            "directly without writing <font face=\"Courier\">struct</font> each time.",
            styles,
        ),
        code(
            """
typedef struct {
    double x;
    double y;
} Point;

Point p;           /* declares a Point without writing 'struct Point' */
            """,
            styles,
        ),

        # --- Section 2: Initialising and accessing fields ---
        p("2. Quick recap: field access", styles, "DarkHeading"),
        p(
            "Initialise with a brace list in field order. Access fields with the dot operator "
            "on a struct value, or the arrow operator on a pointer to a struct.",
            styles,
        ),
        code(
            """
Point origin = {0.0, 0.0};
Point p      = {3.0, 4.0};

printf("x = %f\n", p.x);   /* dot: value */

Point *ptr = &p;
printf("x = %f\n", ptr->x); /* arrow: pointer */
            """,
            styles,
        ),

        # --- Section 3: Structs as function parameters ---
        p("3. Passing structs to functions", styles, "DarkHeading"),
        p(
            "Passing a struct by value copies all its fields into the function's local "
            "parameter. Any modification inside the function does not affect the caller's "
            "copy. Pass a pointer if the function needs to modify the struct.",
            styles,
        ),
        code(
            """
/* by value: caller's copy is unchanged */
double distance_sq(Point a, Point b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return dx*dx + dy*dy;
}

/* by pointer: modifies the caller's struct */
void move_point(Point *p, double dx, double dy) {
    p->x += dx;
    p->y += dy;
}
            """,
            styles,
        ),

        # --- Section 4: Nested structs (Rectangle) ---
        p("4. Structs containing other structs: Rectangle", styles, "DarkHeading"),
        p(
            "A struct field can itself be a struct. A rectangle with sides parallel to the "
            "axes is fully described by its bottom-left and top-right corners.",
            styles,
        ),
        code(
            """
typedef struct {
    Point bottom_left;
    Point top_right;
} Rectangle;

Rectangle r = {{1.0, 2.0}, {5.0, 6.0}};

/* access nested fields */
printf("%f\n", r.bottom_left.x);   /* 1.0 */
printf("%f\n", r.top_right.y);     /* 6.0 */
            """,
            styles,
        ),

        # --- Section 5: Writing predicates and measures ---
        p("5. Writing functions on geometric structs", styles, "DarkHeading"),
        p(
            "The width of a rectangle is the difference in x coordinates of its corners; "
            "the height is the difference in y coordinates. A point is inside the rectangle "
            "if its x coordinate is between the two corners' x values and similarly for y.",
            styles,
        ),
        code(
            """
double area(Rectangle r) {
    double width  = r.top_right.x - r.bottom_left.x;
    double height = r.top_right.y - r.bottom_left.y;
    return width * height;
}

/* returns 1 if p is strictly inside r, 0 otherwise */
int inside(Point p, Rectangle r) {
    return p.x > r.bottom_left.x && p.x < r.top_right.x
        && p.y > r.bottom_left.y && p.y < r.top_right.y;
}
            """,
            styles,
        ),

        # --- Practice Questions ---
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Repair this broken Point definition and explain what the final "
                "<font face=\"Courier\">Point</font> name is doing: "
                "<font face=\"Courier\">typedef struct { double x double y; } Point;</font>",

                "Given <font face=\"Courier\">Point path[3] = {{0,0},{3,4},{6,8}};</font> "
                "and <font face=\"Courier\">Point *p = &amp;path[1];</font>, write one "
                "dot expression and one arrow expression that both read the middle "
                "point's y coordinate.",
            ],
            styles,
        ),
        p("Question 3 — state what the following prints:", styles),
        code(
            """
typedef struct { double x; double y; } Point;
Point a = {1.5, 2.5};
Point b = {4.5, 0.5};
printf("%.1f\n", a.x + b.y);
            """,
            styles,
        ),
        numbered(
            [
                "State what the code above prints.",
                "Write <font face=\"Courier\">double distance_sq(Point a, Point b)</font> "
                "that returns the squared distance between the two points. "
                "(No need for <font face=\"Courier\">sqrt</font>.)",
                "Write a <font face=\"Courier\">typedef struct</font> for a "
                "<font face=\"Courier\">Rectangle</font> defined by a "
                "<font face=\"Courier\">bottom_left</font> Point and a "
                "<font face=\"Courier\">top_right</font> Point.",
                "Write <font face=\"Courier\">double area(Rectangle r)</font> that "
                "returns the area of the rectangle.",
                "Write <font face=\"Courier\">int inside(Point p, Rectangle r)</font> "
                "that returns 1 if <font face=\"Courier\">p</font> is strictly inside "
                "<font face=\"Courier\">r</font> (not on the boundary), 0 otherwise.",
            ],
            styles,
            start=3,
        ),
        p(
            "Question 8 — the function below is meant to translate a point by "
            "(dx, dy) but the change is not visible in the caller:",
            styles,
        ),
        code(
            """
void move_point(Point p, double dx, double dy) {
    p.x += dx;
    p.y += dy;
}

int main() {
    Point pt = {1.0, 2.0};
    move_point(pt, 1.0, 1.0);
    printf("%.1f %.1f\n", pt.x, pt.y);  /* still prints 1.0 2.0 */
}
            """,
            styles,
        ),
        numbered(
            [
                "Explain why the change does not appear in the caller and fix the function "
                "so it does. Show the corrected call site as well.",
            ],
            styles,
            start=8,
        ),
        p("Question 9 — choose the better parameter style:", styles),
        code(
            """
double distance_sq(Point a, Point b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return dx*dx + dy*dy;
}
            """,
            styles,
        ),
        numbered(
            [
                "For this function, explain why passing each Point by value is reasonable, "
                "rather than passing pointers.",
                "What does <font face=\"Courier\">sizeof(Point)</font> return for the "
                "Point defined in question 1, and why might the answer be larger than "
                "<font face=\"Courier\">2 * sizeof(double)</font>?",
            ],
            styles,
            start=9,
        ),

        # --- Mark Scheme ---
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Attempt all questions before checking. "
            "Any correct implementation scores full marks.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "<font face=\"Courier\">typedef struct { double x; double y; } Point;</font>. "
                "The final <font face=\"Courier\">Point</font> is the typedef alias, so "
                "you can declare <font face=\"Courier\">Point p;</font> without writing "
                "<font face=\"Courier\">struct</font>.",

                "Dot form: <font face=\"Courier\">path[1].y</font>. "
                "Arrow form: <font face=\"Courier\">p-&#62;y</font>.",

                "<font face=\"Courier\">2.0</font> — "
                "<font face=\"Courier\">a.x</font> is 1.5, "
                "<font face=\"Courier\">b.y</font> is 0.5, sum is 2.0.",

                "<font face=\"Courier\">double dx = a.x - b.x; double dy = a.y - b.y; "
                "return dx*dx + dy*dy;</font>",

                "<font face=\"Courier\">typedef struct { Point bottom_left; "
                "Point top_right; } Rectangle;</font>",

                "<font face=\"Courier\">return (r.top_right.x - r.bottom_left.x) "
                "* (r.top_right.y - r.bottom_left.y);</font>",

                "<font face=\"Courier\">return p.x &gt; r.bottom_left.x "
                "&amp;&amp; p.x &lt; r.top_right.x "
                "&amp;&amp; p.y &gt; r.bottom_left.y "
                "&amp;&amp; p.y &lt; r.top_right.y;</font>",

                "Structs are passed by value in C — the function receives its own copy "
                "of the Point, so changes to that copy are discarded when the function "
                "returns. Fix: change the parameter to "
                "<font face=\"Courier\">Point *p</font> and use "
                "<font face=\"Courier\">p-&#62;x += dx; p-&#62;y += dy;</font>. "
                "Call site: <font face=\"Courier\">move_point(&amp;pt, 1.0, 1.0);</font>",

                "The function only reads the two points and does not need to modify the "
                "caller's variables. <font face=\"Courier\">Point</font> is also small "
                "here, so copying two doubles per argument is simple and reasonable. "
                "Passing by value also prevents accidental writes to the caller's data.",

                "<font face=\"Courier\">sizeof(Point)</font> is typically 16 bytes "
                "(two <font face=\"Courier\">double</font> fields at 8 bytes each). "
                "On some platforms it could be larger due to struct padding/alignment, "
                "but for two doubles of the same type, padding is unlikely here.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
#include <stdio.h>
#include <stdbool.h>

typedef struct { double x; double y; } Point;
typedef struct { Point bottom_left; Point top_right; } Rectangle;

double area(Rectangle r) {
    return (r.top_right.x - r.bottom_left.x)
         * (r.top_right.y - r.bottom_left.y);
}

int inside(Point p, Rectangle r) {
    return p.x > r.bottom_left.x && p.x < r.top_right.x
        && p.y > r.bottom_left.y && p.y < r.top_right.y;
}

void move_point(Point *p, double dx, double dy) {
    p->x += dx;
    p->y += dy;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
