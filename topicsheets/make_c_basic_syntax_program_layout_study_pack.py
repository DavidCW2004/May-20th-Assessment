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


OUT = Path(__file__).with_name("c-basic-syntax-program-layout-study-pack.pdf")


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
        title="C Basic Syntax and Program Layout Study Pack",
    )

    story = [
        p("C Basic Syntax and Program Layout", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: main, includes, blocks, semicolons, printf, escape sequences, variables, stack allocation, static typing, and format specifiers.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Minimal C program shape", styles, "DarkHeading"),
        p(
            "A normal C program starts running in <font face=\"Courier\">main</font>. Header files are included before compilation so the compiler knows about library functions such as <font face=\"Courier\">printf</font>.",
            styles,
        ),
        code(
            """
#include <stdio.h>

int main(void) {
    printf("Hello\\n");
    return 0;
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">#include &lt;stdio.h&gt;</font> gives declarations for standard input and output functions.",
                "<font face=\"Courier\">int main(void)</font> says the program takes no command-line arguments and returns an integer status.",
                "<font face=\"Courier\">return 0;</font> means successful program completion.",
            ],
            styles,
        ),
        p("2. Statements, semicolons, and blocks", styles, "DarkHeading"),
        p(
            "Most C statements end with a semicolon. Curly braces group statements into a block, usually for a function, loop, or branch.",
            styles,
        ),
        code(
            """
int x = 4;          /* declaration statement */
x = x + 1;          /* assignment statement */
printf("%d\\n", x);  /* function-call statement */

if (x > 0) {
    printf("positive\\n");
}
            """,
            styles,
        ),
        p(
            "A missing semicolon usually causes the compiler to complain on the next line because it is still trying to parse the unfinished statement.",
            styles,
        ),
        p("3. Comments", styles, "DarkHeading"),
        p(
            "Comments are ignored by the compiler. Use them to explain intent, not to repeat obvious code.",
            styles,
        ),
        code(
            """
// One-line comment

/*
   Multi-line comment
*/
            """,
            styles,
        ),
        p("4. Static typing and automatic variables", styles, "DarkHeading"),
        p(
            "C is statically typed: each variable has a declared type, and that type controls how the stored bits are interpreted. Local variables declared inside a block are automatic variables. They normally live until execution leaves that block.",
            styles,
        ),
        code(
            """
int main(void) {
    int count = 3;
    double price = 2.50;
    char grade = 'A';

    count = count + 1;
    /* count = "hello";  not valid: count is an int */

    return 0;
}
            """,
            styles,
        ),
        p(
            "Automatic local variables are commonly stored on the call stack. Do not return a pointer to a local variable, because the variable stops existing after the function returns.",
            styles,
        ),
        p("5. Printing with <font face=\"Courier\">printf</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">printf</font> uses a format string. Each conversion specifier must match the type of the argument you pass.",
            styles,
        ),
        code(
            """
int count = 4;
double average = 2.75;
char letter = 'Z';
char name[] = "Ada";

printf("count=%d\\n", count);
printf("average=%f\\n", average);
printf("letter=%c\\n", letter);
printf("name=%s\\n", name);
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">%d</font> prints an <font face=\"Courier\">int</font>.",
                "<font face=\"Courier\">%f</font> prints a <font face=\"Courier\">double</font>.",
                "<font face=\"Courier\">%c</font> prints a single character.",
                "<font face=\"Courier\">%s</font> prints a null-terminated C string.",
                "<font face=\"Courier\">%zu</font> prints a <font face=\"Courier\">size_t</font> value.",
            ],
            styles,
        ),
        p("6. Escape sequences", styles, "DarkHeading"),
        p(
            "Escape sequences let you put special characters into strings and character constants.",
            styles,
        ),
        code(
            """
printf("first line\\nsecond line\\n");
printf("column1\\tcolumn2\\n");
printf("She said \\"hi\\"\\n");
printf("backslash: \\\\ \\n");
            """,
            styles,
        ),
        p(
            "The source code contains two characters such as backslash and <font face=\"Courier\">n</font>, but the actual output contains one newline character.",
            styles,
        ),
        p("7. Expression values and assignments", styles, "DarkHeading"),
        p(
            "An expression computes a value. Assignment changes an existing object. Comparison computes true or false as an integer result.",
            styles,
        ),
        code(
            """
int x = 5;
int y = x + 2;    /* y is 7 */

x = y * 3;        /* x is now 21 */

if (x == 21) {    /* comparison, not assignment */
    printf("match\\n");
}
            """,
            styles,
        ),
        p(
            "Use <font face=\"Courier\">=</font> for assignment and <font face=\"Courier\">==</font> for equality comparison.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        p(
            "Use this broken program for question 2:",
            styles,
        ),
        code(
            """
#include <stdio.h>

int main(void) {
    int x = 4
    double y = 2.5
    printf("%d %f\\n", x, y)
    return 0;
}
            """,
            styles,
        ),
        numbered(
            [
                "Write a complete C program that prints <font face=\"Courier\">Ready</font> followed by a newline and returns success.",
                "Find and fix the missing semicolons in the broken program above.",
                "For <font face=\"Courier\">int n = 7; double x = 2.5;</font>, choose the correct <font face=\"Courier\">printf</font> format specifiers.",
                "Explain why a local variable declared inside a function cannot safely be returned by address.",
                "Write one output statement that prints a tab between two numbers and a newline at the end.",
                "Explain the difference between <font face=\"Courier\">=</font> and <font face=\"Courier\">==</font> in an <font face=\"Courier\">if</font> condition.",
                "Explain why a missing semicolon can make the compiler report an error on the following line instead of the line where the semicolon is missing.",
                "State what <font face=\"Courier\">return 0;</font> from <font face=\"Courier\">main</font> normally means.",
                "Declare three automatic local variables inside <font face=\"Courier\">main</font>: an <font face=\"Courier\">int</font>, a <font face=\"Courier\">double</font>, and a <font face=\"Courier\">char</font>.",
                "Write a <font face=\"Courier\">printf</font> call that prints a literal double quote character inside the output.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Strong answers should connect syntax to what the compiler sees.", styles, "SourceText"),
        numbered(
            [
                "Expected: include <font face=\"Courier\">stdio.h</font>, define <font face=\"Courier\">int main(void)</font>, call <font face=\"Courier\">printf(\"Ready\\n\")</font>, then <font face=\"Courier\">return 0;</font>.",
                "The fixed lines are <font face=\"Courier\">int x = 4;</font>, <font face=\"Courier\">double y = 2.5;</font>, and <font face=\"Courier\">printf(\"%d %f\\n\", x, y);</font>.",
                "Use <font face=\"Courier\">%d</font> for <font face=\"Courier\">int</font> and <font face=\"Courier\">%f</font> for <font face=\"Courier\">double</font>.",
                "The local automatic variable stops existing when the function returns, so the returned address would point at storage that is no longer valid.",
                "Expected shape: <font face=\"Courier\">printf(\"%d\\t%d\\n\", a, b);</font>.",
                "<font face=\"Courier\">=</font> assigns a new value; <font face=\"Courier\">==</font> compares two values.",
                "A missing semicolon leaves the previous statement unfinished, so the next line is often where the compiler first sees tokens that no longer fit the unfinished statement.",
                "It normally reports successful program termination to the operating system.",
                "Expected shape: <font face=\"Courier\">int count = 3;</font>, <font face=\"Courier\">double price = 2.50;</font>, and <font face=\"Courier\">char grade = 'A';</font> inside a block such as <font face=\"Courier\">main</font>.",
                "Expected shape: <font face=\"Courier\">printf(\"She said \\\"hi\\\"\\n\");</font>. The double quote inside the string is written as <font face=\"Courier\">\\\"</font>.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Forgetting the semicolon after declarations and function calls.",
                "Using the wrong <font face=\"Courier\">printf</font> specifier for the argument type.",
                "Confusing assignment with equality comparison.",
                "Forgetting that local automatic variables do not live forever.",
                "Writing a newline as <font face=\"Courier\">/n</font> instead of <font face=\"Courier\">\\n</font>.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
