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


OUT = Path(__file__).with_name("c-function-pointers-callbacks-study-pack.pdf")


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


def numbered(items, styles):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=5 * mm) for item in items],
        bulletType="1",
        leftIndent=7 * mm,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=8,
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
        title="C Function Pointers and Callbacks Study Pack",
    )

    story = [
        p("C Function Pointers and Callbacks", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 L06 Pointers to Functions and worksheet 4, chosen from a red C topic in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. What a function pointer is", styles, "DarkHeading"),
        p(
            "A function pointer stores the address of a function. The type must match the function's return type and parameter types. This lets code choose which function to call at run time.",
            styles,
        ),
        code(
            """
int Plus(int a, int b) {
    return a + b;
}

int Multiply(int a, int b) {
    return a * b;
}

int (*f)(int, int);
f = Plus;
printf("%d\\n", f(10, 6));      /* 16 */
            """,
            styles,
        ),
        p(
            "Read <font face=\"Courier\">int (*f)(int, int)</font> as: <font face=\"Courier\">f</font> is a pointer to a function that takes two <font face=\"Courier\">int</font> values and returns an <font face=\"Courier\">int</font>.",
            styles,
        ),
        p("2. Function names and calling syntax", styles, "DarkHeading"),
        p(
            "In most expressions, a function name can be used as the address of that function. The explicit address-of and dereference forms are allowed, but the shorter form is common.",
            styles,
        ),
        code(
            """
f = &Plus;          /* explicit address-of */
f = Plus;           /* common shorter form */

int a = (*f)(4, 5); /* explicit dereference */
int b = f(4, 5);    /* common shorter form */
            """,
            styles,
        ),
        p("3. Callbacks: passing behaviour into a function", styles, "DarkHeading"),
        p(
            "A callback is a function passed into another function. The receiving function can call it without knowing exactly which function was chosen by the caller.",
            styles,
        ),
        code(
            """
int doFunction(int a, int b, int (*operation)(int, int)) {
    return operation(a, b);
}

printf("%d\\n", doFunction(1, 3, Plus));      /* 4 */
printf("%d\\n", doFunction(1, 3, Multiply));  /* 3 */
            """,
            styles,
        ),
        bullets(
            [
                "The callback parameter includes the return type, pointer name, and parameter list.",
                "The callback's signature must match what the receiving function expects.",
                "Callbacks are useful when the same algorithm needs different behaviour plugged in.",
            ],
            styles,
        ),
        p("4. <font face=\"Courier\">qsort</font> and comparison functions", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">qsort</font> is a standard library sorting function. It does not know the element type, so it receives the array as generic memory and uses a callback to compare two elements.",
            styles,
        ),
        code(
            """
#include <stdlib.h>

void qsort(void *base,
           size_t nmemb,
           size_t size,
           int (*compar)(const void *, const void *));
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">base</font>: pointer to the first element of the array.",
                "<font face=\"Courier\">nmemb</font>: number of elements.",
                "<font face=\"Courier\">size</font>: size in bytes of one element.",
                "<font face=\"Courier\">compar</font>: callback used to order two elements.",
            ],
            styles,
        ),
        p("5. Comparator return values", styles, "DarkHeading"),
        p(
            "A comparator receives pointers to two elements. It returns a negative value if the first should come before the second, zero if they are equal, and a positive value if the first should come after the second.",
            styles,
        ),
        code(
            """
int compare_ints(const void *p, const void *q) {
    const int *a = p;
    const int *b = q;

    if (*a < *b) return -1;
    if (*a > *b) return 1;
    return 0;
}
            """,
            styles,
        ),
        p(
            "The parameters are <font face=\"Courier\">void *</font> because <font face=\"Courier\">qsort</font> is generic. Inside the comparator, cast or assign them to the correct pointer type before dereferencing.",
            styles,
        ),
        p("6. Sorting an integer array with <font face=\"Courier\">qsort</font>", styles, "DarkHeading"),
        code(
            """
int values[] = {4, 6, 8, 3, 2, 1, 5, 9, 0};
size_t len = sizeof values / sizeof values[0];

qsort(values, len, sizeof values[0], compare_ints);

for (size_t i = 0; i < len; i++) {
    printf("%d\\n", values[i]);
}
            """,
            styles,
        ),
        p(
            "Using <font face=\"Courier\">sizeof values[0]</font> means the element size stays correct if the array element type changes later.",
            styles,
        ),
        p("7. <font face=\"Courier\">void *</font> and generic memory", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">void *</font> means a pointer to data of unknown type. You cannot safely dereference it as a value until you convert it to the correct pointer type. For generic byte movement, use <font face=\"Courier\">char *</font> because a char is one byte.",
            styles,
        ),
        code(
            """
void print_int_value(void *p) {
    int *ip = p;
    printf("%d\\n", *ip);
}

char *bytes = array;
char *element_i = bytes + i * width;
            """,
            styles,
        ),
        p(
            "This is the idea behind worksheet 4's generic merge sort: pass the array as <font face=\"Courier\">void *</font>, pass the element width, and pass a comparator callback.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write the declaration for a function pointer named <font face=\"Courier\">op</font> that points to a function taking two <font face=\"Courier\">int</font> values and returning an <font face=\"Courier\">int</font>.",
                "Given <font face=\"Courier\">int Plus(int a, int b)</font>, assign <font face=\"Courier\">Plus</font> to <font face=\"Courier\">op</font> and call it with <font face=\"Courier\">10</font> and <font face=\"Courier\">6</font>.",
                "Explain why <font face=\"Courier\">int (*op)(int, int)</font> is different from <font face=\"Courier\">int *op(int, int)</font>.",
                "Write a function <font face=\"Courier\">apply</font> that takes two integers and a callback with the same type as <font face=\"Courier\">Plus</font>, then returns the callback result.",
                "Explain what a callback is in the context of <font face=\"Courier\">apply(1, 3, Plus)</font>.",
                "List the four arguments passed to <font face=\"Courier\">qsort</font> and what each one means.",
                "Write a comparator <font face=\"Courier\">compare_ints</font> suitable for sorting integers with <font face=\"Courier\">qsort</font>.",
                "Use <font face=\"Courier\">qsort</font> to sort <font face=\"Courier\">int values[] = {3, 1, 2};</font>.",
                "Why does a <font face=\"Courier\">qsort</font> comparator receive <font face=\"Courier\">const void *</font> rather than <font face=\"Courier\">int *</font>?",
                "In generic code, why is a <font face=\"Courier\">void *</font> often converted to <font face=\"Courier\">char *</font> before doing pointer arithmetic?",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should show the exact function pointer shape, callback idea, and safe comparator handling.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "Expected declaration: <font face=\"Courier\">int (*op)(int, int);</font>. Parentheses around <font face=\"Courier\">*op</font> are essential.",
                "Expected pattern: <font face=\"Courier\">op = Plus;</font> then <font face=\"Courier\">int result = op(10, 6);</font>. Using <font face=\"Courier\">&#38;Plus</font> and <font face=\"Courier\">(*op)(10, 6)</font> is also valid.",
                "<font face=\"Courier\">int (*op)(int, int)</font> is a pointer to a function. <font face=\"Courier\">int *op(int, int)</font> declares a function named <font face=\"Courier\">op</font> that returns a pointer to int.",
                "Expected pattern: <font face=\"Courier\">int apply(int a, int b, int (*fn)(int, int)) { return fn(a, b); }</font>.",
                "The callback is <font face=\"Courier\">Plus</font>. <font face=\"Courier\">apply</font> receives it as a function pointer and calls it to decide what operation to perform.",
                "<font face=\"Courier\">qsort</font> receives the base pointer, number of elements, size of each element, and comparator callback.",
                "A good comparator casts or assigns the generic pointers to <font face=\"Courier\">const int *</font>, compares the pointed-to values, and returns negative, zero, or positive.",
                "Expected pattern: compute <font face=\"Courier\">len</font> using <font face=\"Courier\">sizeof values / sizeof values[0]</font>, then call <font face=\"Courier\">qsort(values, len, sizeof values[0], compare_ints);</font>.",
                "<font face=\"Courier\">qsort</font> is generic and can sort arrays of many element types. It uses <font face=\"Courier\">const void *</font> so the comparator receives pointers to unknown read-only element types.",
                "Pointer arithmetic depends on the pointed-to type size. A <font face=\"Courier\">char *</font> moves one byte at a time, so generic code can calculate element addresses using byte offsets.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
int apply(int a, int b, int (*fn)(int, int)) {
    return fn(a, b);
}

int compare_ints(const void *p, const void *q) {
    const int *a = p;
    const int *b = q;

    if (*a < *b) return -1;
    if (*a > *b) return 1;
    return 0;
}

int values[] = {3, 1, 2};
size_t len = sizeof values / sizeof values[0];
qsort(values, len, sizeof values[0], compare_ints);
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
