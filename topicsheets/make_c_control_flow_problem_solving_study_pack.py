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


OUT = Path(__file__).with_name("c-control-flow-problem-solving-study-pack.pdf")


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
        title="C Control Flow and Problem Solving Study Pack",
    )

    story = [
        p("C Control Flow and Problem Solving", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: if, for, while, factorial, numerical approximation of e, and compile/link/run workflow.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Conditions and truth", styles, "DarkHeading"),
        p(
            "In C, conditions use integer-style truth. Zero is false. Any non-zero value is true. Comparisons produce an integer result that can be used by <font face=\"Courier\">if</font>, <font face=\"Courier\">while</font>, and <font face=\"Courier\">for</font>.",
            styles,
        ),
        code(
            """
int n = 7;

if (n > 0) {
    printf("positive\\n");
} else if (n == 0) {
    printf("zero\\n");
} else {
    printf("negative\\n");
}
            """,
            styles,
        ),
        p(
            "The comparison <font face=\"Courier\">n > 0</font> is tested first. Only one branch of this chain runs.",
            styles,
        ),
        p("2. <font face=\"Courier\">for</font> loops", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">for</font> loop is useful when you know the counting pattern. The three parts are initialisation, condition, and update.",
            styles,
        ),
        code(
            """
for (int i = 0; i < 5; i++) {
    printf("%d\\n", i);
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">int i = 0</font> runs once before the loop starts.",
                "<font face=\"Courier\">i < 5</font> is checked before each iteration.",
                "<font face=\"Courier\">i++</font> runs after each loop body.",
                "The printed values are <font face=\"Courier\">0</font> through <font face=\"Courier\">4</font>, not <font face=\"Courier\">5</font>.",
            ],
            styles,
        ),
        p("3. <font face=\"Courier\">while</font> loops", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">while</font> loop is useful when the number of iterations depends on a condition that changes during the loop.",
            styles,
        ),
        code(
            """
int n = 10;

while (n > 1) {
    printf("%d\\n", n);
    n = n / 2;
}
            """,
            styles,
        ),
        p(
            "Make sure the loop body changes something involved in the condition. Otherwise the loop may never finish.",
            styles,
        ),
        p("4. Factorial pattern", styles, "DarkHeading"),
        p(
            "Factorial multiplies the integers from <font face=\"Courier\">1</font> to <font face=\"Courier\">n</font>. Start the accumulator at <font face=\"Courier\">1</font>, not <font face=\"Courier\">0</font>, because multiplying by zero destroys the result.",
            styles,
        ),
        code(
            """
int factorial(int n) {
    int result = 1;

    for (int i = 2; i <= n; i++) {
        result *= i;
    }

    return result;
}
            """,
            styles,
        ),
        p(
            "For <font face=\"Courier\">n == 5</font>, the updates are <font face=\"Courier\">1 * 2 * 3 * 4 * 5</font>, so the result is <font face=\"Courier\">120</font>.",
            styles,
        ),
        p("5. Approximating <font face=\"Courier\">e</font>", styles, "DarkHeading"),
        p(
            "The constant <font face=\"Courier\">e</font> can be approximated using the series <font face=\"Courier\">1 + 1/1! + 1/2! + 1/3! + ...</font>. This is a good loop exercise because each term depends on the previous factorial.",
            styles,
        ),
        code(
            """
double approximate_e(int terms) {
    double sum = 1.0;
    double factorial = 1.0;

    for (int n = 1; n < terms; n++) {
        factorial *= n;
        sum += 1.0 / factorial;
    }

    return sum;
}
            """,
            styles,
        ),
        p(
            "Use <font face=\"Courier\">1.0</font>, not <font face=\"Courier\">1</font>, when you need floating-point division.",
            styles,
        ),
        p("6. Early returns and input checks", styles, "DarkHeading"),
        p(
            "Small C programs are easier to reason about when invalid cases are rejected early. Check preconditions before doing the main work.",
            styles,
        ),
        code(
            """
int safe_factorial(int n, int *out) {
    if (n < 0) {
        return 0;
    }

    int result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }

    *out = result;
    return 1;
}
            """,
            styles,
        ),
        p(
            "Here the return value is a success flag. The output value is written only when the input is valid.",
            styles,
        ),
        p("7. Compile, link, and run", styles, "DarkHeading"),
        p(
            "For a single-file C program, one command can compile and link. For multiple files, you can compile to object files first and then link them.",
            styles,
        ),
        code(
            """
gcc -Wall -Wextra -std=c11 -o app main.c
./app

gcc -Wall -Wextra -std=c11 -c main.c
gcc -Wall -Wextra -std=c11 -c maths.c
gcc -o app main.o maths.o
./app
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">-c</font> compiles a source file to an object file without linking.",
                "The final link command combines object files into an executable.",
                "Warnings should be read as useful feedback, not ignored.",
            ],
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Trace the output of a loop that runs <font face=\"Courier\">for (int i = 0; i &lt; 4; i++)</font>.",
                "Write an <font face=\"Courier\">if</font> statement that prints whether an integer is negative, zero, or positive.",
                "Write a <font face=\"Courier\">while</font> loop that divides a value by two until it reaches zero.",
                "Write a factorial function for non-negative integers using a loop and an accumulator.",
                "Explain why a factorial accumulator starts at <font face=\"Courier\">1</font> instead of <font face=\"Courier\">0</font>.",
                "Write a loop that approximates <font face=\"Courier\">e</font> using <font face=\"Courier\">terms</font> terms.",
                "Given a function that cannot handle negative input, show the early-return check.",
                "Write the compile and run commands for <font face=\"Courier\">main.c</font> using <font face=\"Courier\">gcc</font>.",
                "For a program split across <font face=\"Courier\">main.c</font> and <font face=\"Courier\">maths.c</font>, write the commands that create <font face=\"Courier\">main.o</font> and <font face=\"Courier\">maths.o</font>, then link them into <font face=\"Courier\">app</font>.",
                "Explain why <font face=\"Courier\">1.0 / factorial(n)</font> is used in the <font face=\"Courier\">e</font> approximation instead of <font face=\"Courier\">1 / factorial(n)</font>.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Strong answers should trace loop state, not just quote syntax.", styles, "SourceText"),
        numbered(
            [
                "The loop prints <font face=\"Courier\">0</font>, <font face=\"Courier\">1</font>, <font face=\"Courier\">2</font>, and <font face=\"Courier\">3</font>. It stops when <font face=\"Courier\">i</font> becomes <font face=\"Courier\">4</font>.",
                "Expected: use <font face=\"Courier\">if (n &lt; 0)</font>, <font face=\"Courier\">else if (n == 0)</font>, and <font face=\"Courier\">else</font>.",
                "Expected shape: initialise <font face=\"Courier\">n</font>, test <font face=\"Courier\">n != 0</font> or <font face=\"Courier\">n > 0</font>, update <font face=\"Courier\">n = n / 2</font> in the body.",
                "Expected: <font face=\"Courier\">int result = 1;</font>, loop from <font face=\"Courier\">2</font> to <font face=\"Courier\">n</font>, multiply into <font face=\"Courier\">result</font>, then return it.",
                "Multiplication uses <font face=\"Courier\">1</font> as the neutral starting value. Starting at <font face=\"Courier\">0</font> would keep the result at zero.",
                "Expected: keep a running factorial and add <font face=\"Courier\">1.0 / factorial</font> each iteration.",
                "Expected shape: <font face=\"Courier\">if (n &lt; 0) return 0;</font> before the main calculation.",
                "Expected single-file command: <font face=\"Courier\">gcc -Wall -Wextra -std=c11 -o app main.c</font>, then <font face=\"Courier\">./app</font>.",
                "Expected: <font face=\"Courier\">gcc -Wall -Wextra -std=c11 -c main.c</font>, <font face=\"Courier\">gcc -Wall -Wextra -std=c11 -c maths.c</font>, then <font face=\"Courier\">gcc -o app main.o maths.o</font>.",
                "Using <font face=\"Courier\">1.0</font> forces floating-point division. With integer division, terms such as <font face=\"Courier\">1 / 2</font> and <font face=\"Courier\">1 / 6</font> become <font face=\"Courier\">0</font>.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Using <font face=\"Courier\">i &lt;= n</font> when the valid range should stop before <font face=\"Courier\">n</font>.",
                "Forgetting to update the variable used in a <font face=\"Courier\">while</font> condition.",
                "Starting a product accumulator at zero.",
                "Using integer division where floating-point division is needed.",
                "Ignoring compiler warnings during the compile-link-run cycle.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
