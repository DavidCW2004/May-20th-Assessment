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


OUT = Path(__file__).with_name("c-types-conversions-study-pack.pdf")


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
        title="C Types and Conversions Study Pack",
    )

    story = [
        p("C Types and Conversions", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 L03 More Types, chosen from a red C topic not yet covered in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Integer division", styles, "DarkHeading"),
        p(
            "When both operands of <font face=\"Courier\">/</font> are integers, C performs integer division. The fractional part is discarded and the result rounds towards zero.",
            styles,
        ),
        code(
            """
int a = 56;
int b = -56;
int d = 10;

printf("%d %d\\n", a / d, b / d);  /* 5 -5 */
            """,
            styles,
        ),
        p(
            "This is different from mathematical floor division. The result of <font face=\"Courier\">-56 / 10</font> is <font face=\"Courier\">-5</font>, not <font face=\"Courier\">-6</font>.",
            styles,
        ),
        p("2. Promotions in arithmetic", styles, "DarkHeading"),
        p(
            "Before arithmetic is performed, C may promote operands to a wider or more precise type. If an <font face=\"Courier\">int</font> is combined with a <font face=\"Courier\">float</font>, the calculation is done as floating-point arithmetic.",
            styles,
        ),
        code(
            """
int i = 56;
float denominator = 10.0f;

printf("%f\\n", i / denominator);  /* 5.600000 */
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">char</font> values are commonly promoted to <font face=\"Courier\">int</font> before arithmetic.",
                "Mixing integer and floating-point operands usually produces a floating-point calculation.",
                "In <font face=\"Courier\">printf</font>, <font face=\"Courier\">float</font> arguments are promoted to <font face=\"Courier\">double</font>.",
            ],
            styles,
        ),
        p("3. Explicit casts", styles, "DarkHeading"),
        p(
            "A cast asks C to treat a value as another type at that point in the expression. This is often used to force floating-point division when the original variables are integers.",
            styles,
        ),
        code(
            """
int numerator = 56;
int denominator = 10;

printf("%f\\n", numerator / (float)denominator);  /* 5.600000 */
printf("%d\\n", numerator / denominator);         /* 5 */
            """,
            styles,
        ),
        p(
            "The cast changes the calculation, not the stored type of the original variable. After <font face=\"Courier\">(float)denominator</font>, <font face=\"Courier\">denominator</font> is still an <font face=\"Courier\">int</font> variable.",
            styles,
        ),
        p("4. Weak typing and narrowing conversions", styles, "DarkHeading"),
        p(
            "C allows many implicit conversions. This is convenient, but it can silently lose information. Assigning a large value to a smaller type may wrap, truncate, or produce an implementation-dependent result.",
            styles,
        ),
        code(
            """
unsigned short x = 65535;
short y = x;
char c = x;

printf("%u\\n", x);
printf("%d\\n", y);
printf("%c\\n", c);
            """,
            styles,
        ),
        p(
            "The compiler may not stop this. You need to notice when a conversion is narrowing: large type to small type, floating-point to integer, or unsigned to signed.",
            styles,
        ),
        p("5. Characters are small integers", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">char</font> stores a character code. In arithmetic, it can be promoted to <font face=\"Courier\">int</font>. For ASCII-compatible systems, <font face=\"Courier\">'a'</font> has code <font face=\"Courier\">97</font>.",
            styles,
        ),
        code(
            """
char c = 'a';
int n = 10 * c;

printf("%c %d %d\\n", c, c, n);  /* a 97 970 */
            """,
            styles,
        ),
        p(
            "Use <font face=\"Courier\">%c</font> to print the character and <font face=\"Courier\">%d</font> to print its numeric code.",
            styles,
        ),
        p("6. <font face=\"Courier\">typedef</font> and <font face=\"Courier\">size_t</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">typedef</font> creates a new name for an existing type. It does not create a new runtime object or add type safety by itself; it mainly improves readability.",
            styles,
        ),
        code(
            """
typedef float Temperature;

Temperature today = 8.0f;
Temperature tomorrow = today - 2.0f;
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">size_t</font> is the unsigned integer type used for object sizes and array lengths. <font face=\"Courier\">sizeof</font> produces a <font face=\"Courier\">size_t</font> result, so print it with <font face=\"Courier\">%zu</font>.",
            styles,
        ),
        code(
            """
size_t bytes = sizeof(double);
printf("%zu\\n", bytes);
            """,
            styles,
        ),
        p("7. Structs as data types", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">struct</font> groups related fields into one compound type. Members are accessed with dot notation when you have the struct object itself.",
            styles,
        ),
        code(
            """
#include <stdbool.h>

struct Weather {
    float temperature;
    bool raining;
    int visibility;
};

struct Weather today;
today.temperature = 8.0f;
today.raining = true;
today.visibility = 3;
            """,
            styles,
        ),
        p(
            "A common pattern is to combine <font face=\"Courier\">typedef</font> with <font face=\"Courier\">struct</font> so variables can be declared without repeating the <font face=\"Courier\">struct</font> keyword.",
            styles,
        ),
        code(
            """
typedef struct Weather {
    float temperature;
    bool raining;
    int visibility;
} Weather;

Weather tomorrow = {12.0f, false, 8};
            """,
            styles,
        ),
        p("8. Enums and unions", styles, "DarkHeading"),
        p(
            "An <font face=\"Courier\">enum</font> defines named integer constants. It is useful when a variable should hold one value from a small set of choices.",
            styles,
        ),
        code(
            """
enum Direction {
    NORTH,
    EAST,
    SOUTH,
    WEST
};

enum Direction heading = EAST;
            """,
            styles,
        ),
        p(
            "A <font face=\"Courier\">union</font> lets different fields share the same memory. Only one member should be treated as active at a time. This saves space, but it is easier to misuse than a struct.",
            styles,
        ),
        code(
            """
union Number {
    int i;
    float f;
};

union Number n;
n.i = 42;    /* now the int member is the meaningful one */
            """,
            styles,
        ),
        p("9. Format specifiers must match", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">printf</font> does not know the real types of its extra arguments. The format string tells it how to interpret them, so mismatched format specifiers can print nonsense or cause undefined behaviour.",
            styles,
        ),
        code(
            """
int count = 3;
double value = 4.5;
size_t n = sizeof value;

printf("%d\\n", count);
printf("%f\\n", value);
printf("%zu\\n", n);
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Work out the values printed by <font face=\"Courier\">printf(\"%d %d\", 56 / 10, -56 / 10);</font>.",
                "Change <font face=\"Courier\">int a = 7, b = 2; printf(\"%d\", a / b);</font> so it prints a floating-point answer without changing the declarations.",
                "For <font face=\"Courier\">char c = 'a'; int n = 10 * c;</font>, work out the likely value of <font face=\"Courier\">n</font> on an ASCII-compatible system and explain the conversion.",
                "A program assigns <font face=\"Courier\">123456.789</font> to a <font face=\"Courier\">short</font>. Explain why C may compile it but the stored value should not be trusted.",
                "Create a typedef named <font face=\"Courier\">Temperature</font> for <font face=\"Courier\">float</font>, then declare a variable named <font face=\"Courier\">today</font> with value <font face=\"Courier\">8.0</font>.",
                "Write a <font face=\"Courier\">printf</font> line that safely prints the result of <font face=\"Courier\">sizeof(double)</font>.",
                "Define a <font face=\"Courier\">struct Weather</font> with temperature, raining, and visibility fields, then assign values to one variable.",
                "Rewrite the <font face=\"Courier\">struct Weather</font> definition using <font face=\"Courier\">typedef</font> so the type can be used as <font face=\"Courier\">Weather today;</font>.",
                "Choose between <font face=\"Courier\">enum</font>, <font face=\"Courier\">struct</font>, and <font face=\"Courier\">union</font> for a compass direction, a weather record, and memory shared between either an <font face=\"Courier\">int</font> or a <font face=\"Courier\">float</font>.",
                "Find the format-specifier bug in <font face=\"Courier\">size_t n = sizeof(int); printf(\"%d\", n);</font> and fix it.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should show the type of the expression, not just the final number.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "The values are <font face=\"Courier\">5</font> and <font face=\"Courier\">-5</font>. Integer division discards the fractional part and rounds towards zero.",
                "Cast one operand to a floating-point type and use a floating-point format, for example <font face=\"Courier\">printf(\"%f\", (float)a / b);</font>.",
                "On ASCII-compatible systems, <font face=\"Courier\">'a'</font> has code <font face=\"Courier\">97</font>. The <font face=\"Courier\">char</font> is promoted to <font face=\"Courier\">int</font>, so <font face=\"Courier\">n</font> is <font face=\"Courier\">970</font>.",
                "This is a narrowing conversion from floating-point to a smaller integer type. C may not report an error, but the fractional part is lost and the remaining value may not fit in <font face=\"Courier\">short</font>.",
                "Expected pattern: <font face=\"Courier\">typedef float Temperature;</font> then <font face=\"Courier\">Temperature today = 8.0f;</font>.",
                "Use <font face=\"Courier\">%zu</font>: <font face=\"Courier\">printf(\"%zu\\n\", sizeof(double));</font>.",
                "A valid answer uses fields such as <font face=\"Courier\">float temperature;</font>, <font face=\"Courier\">bool raining;</font>, and <font face=\"Courier\">int visibility;</font>, then assigns with dot notation.",
                "Expected pattern: <font face=\"Courier\">typedef struct Weather { ... } Weather;</font> followed by <font face=\"Courier\">Weather today;</font>.",
                "Use <font face=\"Courier\">enum</font> for compass direction, <font face=\"Courier\">struct</font> for a weather record with several fields, and <font face=\"Courier\">union</font> for storage shared between alternative representations.",
                "<font face=\"Courier\">sizeof</font> returns <font face=\"Courier\">size_t</font>, so use <font face=\"Courier\">%zu</font>: <font face=\"Courier\">printf(\"%zu\", n);</font>.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
#include <stdbool.h>
#include <stdio.h>

typedef float Temperature;

typedef struct Weather {
    Temperature temperature;
    bool raining;
    int visibility;
} Weather;

enum Direction {
    NORTH,
    EAST,
    SOUTH,
    WEST
};

int main(void) {
    Weather today = {8.0f, true, 3};
    size_t bytes = sizeof today;

    printf("%f %d %d\\n",
           today.temperature,
           today.raining,
           today.visibility);
    printf("%zu\\n", bytes);

    return 0;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
