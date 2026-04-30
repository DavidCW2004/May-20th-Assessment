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


OUT = Path(__file__).with_name("c-command-line-arguments-study-pack.pdf")


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
        title="C Command-line Arguments Study Pack",
    )

    story = [
        p("C Command-line Arguments", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: argc, argv, quoting, atoi, atof, and safe conversion checks.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. The real shape of <font face=\"Courier\">main</font>", styles, "DarkHeading"),
        p(
            "A command-line C program can receive arguments through <font face=\"Courier\">main</font>. The operating system passes an argument count and an argument vector.",
            styles,
        ),
        code(
            """
int main(int argc, char *argv[]) {
    /* argc is the number of argument strings */
    /* argv is an array of pointers to those strings */
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">argc</font> is at least 1 for a normally launched program.",
                "<font face=\"Courier\">argv[0]</font> is the program name or path used to launch it.",
                "<font face=\"Courier\">argv[1]</font> is the first user-supplied argument.",
                "Each <font face=\"Courier\">argv[i]</font> has type <font face=\"Courier\">char *</font>, so it is a C string.",
            ],
            styles,
        ),
        p("2. Indexes and off-by-one checks", styles, "DarkHeading"),
        p(
            "The last valid argument index is <font face=\"Courier\">argc - 1</font>. Before reading <font face=\"Courier\">argv[1]</font> or later, check that enough arguments were supplied.",
            styles,
        ),
        code(
            """
#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s input output\\n", argv[0]);
        return 1;
    }

    printf("input: %s\\n", argv[1]);
    printf("output: %s\\n", argv[2]);
    return 0;
}
            """,
            styles,
        ),
        p(
            "For this program, <font face=\"Courier\">argc == 3</font> means the program name plus two user arguments. If the check fails, return before touching missing indexes.",
            styles,
        ),
        p("3. Quoting and spaces", styles, "DarkHeading"),
        p(
            "The shell splits command text into separate arguments before the C program starts. Spaces usually separate arguments. Quotes keep spaces inside one argument.",
            styles,
        ),
        code(
            """
./rename old.txt new.txt
/* argc == 3:
   argv[0] = "./rename"
   argv[1] = "old.txt"
   argv[2] = "new.txt"
*/

./rename "old name.txt" "new name.txt"
/* still argc == 3, because quotes group the file names */
            """,
            styles,
        ),
        p(
            "Your program receives the finished argument strings. It normally does not see the quote characters themselves.",
            styles,
        ),
        p("4. <font face=\"Courier\">atoi</font> and <font face=\"Courier\">atof</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">atoi</font> converts a string to <font face=\"Courier\">int</font>, and <font face=\"Courier\">atof</font> converts a string to <font face=\"Courier\">double</font>. They are short, but weak: they do not give a reliable error result for invalid input.",
            styles,
        ),
        code(
            """
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s count scale\\n", argv[0]);
        return 1;
    }

    int count = atoi(argv[1]);
    double scale = atof(argv[2]);

    printf("count=%d scale=%f\\n", count, scale);
    return 0;
}
            """,
            styles,
        ),
        p(
            "The trap is that <font face=\"Courier\">atoi(\"abc\")</font> returns <font face=\"Courier\">0</font>, but <font face=\"Courier\">atoi(\"0\")</font> also returns <font face=\"Courier\">0</font>. You cannot tell those cases apart from the return value.",
            styles,
        ),
        p("5. Safer conversion with <font face=\"Courier\">strtol</font>", styles, "DarkHeading"),
        p(
            "For checked integer parsing, use <font face=\"Courier\">strtol</font>. It tells you where parsing stopped, so you can reject non-numeric leftovers.",
            styles,
        ),
        code(
            """
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

int parse_int(const char *text, int *out) {
    char *end = NULL;
    errno = 0;

    long value = strtol(text, &end, 10);

    if (end == text || *end != '\\0') {
        return 0;  /* not a whole integer */
    }
    if (errno == ERANGE || value < INT_MIN || value > INT_MAX) {
        return 0;  /* out of range for int */
    }

    *out = (int)value;
    return 1;
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">end == text</font> means no digits were consumed.",
                "<font face=\"Courier\">*end != '\\0'</font> means extra junk was left over, such as <font face=\"Courier\">12abc</font>.",
                "<font face=\"Courier\">errno == ERANGE</font> means the value was too large or too small for <font face=\"Courier\">long</font>.",
            ],
            styles,
        ),
        p("6. Safer conversion with <font face=\"Courier\">strtod</font>", styles, "DarkHeading"),
        p(
            "For checked floating-point parsing, use <font face=\"Courier\">strtod</font>. It has the same end-pointer idea as <font face=\"Courier\">strtol</font>.",
            styles,
        ),
        code(
            """
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int parse_double(const char *text, double *out) {
    char *end = NULL;
    errno = 0;

    double value = strtod(text, &end);

    if (end == text || *end != '\\0' || errno == ERANGE) {
        return 0;
    }

    *out = value;
    return 1;
}
            """,
            styles,
        ),
        p(
            "For many exam answers, saying that <font face=\"Courier\">atoi</font> and <font face=\"Courier\">atof</font> are simple but poor at error reporting is enough. If the question asks for robust input, use the <font face=\"Courier\">strto*</font> family.",
            styles,
        ),
        p("7. Complete argument handling pattern", styles, "DarkHeading"),
        code(
            """
#include <stdio.h>

int main(int argc, char *argv[]) {
    int repeats = 0;

    if (argc != 3) {
        fprintf(stderr, "usage: %s word repeats\\n", argv[0]);
        return 1;
    }
    if (!parse_int(argv[2], &repeats) || repeats < 0) {
        fprintf(stderr, "repeats must be a non-negative integer\\n");
        return 1;
    }

    for (int i = 0; i < repeats; i++) {
        printf("%s\\n", argv[1]);
    }

    return 0;
}
            """,
            styles,
        ),
        p(
            "The structure is: check <font face=\"Courier\">argc</font>, parse each argument, validate ranges, then do the real work.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "A program is run as <font face=\"Courier\">./prog alpha beta</font>. What are <font face=\"Courier\">argc</font>, <font face=\"Courier\">argv[0]</font>, <font face=\"Courier\">argv[1]</font>, and <font face=\"Courier\">argv[2]</font>?",
                "Write the <font face=\"Courier\">main</font> signature that receives command-line arguments.",
                "A program needs exactly one file name after the program name. Write the <font face=\"Courier\">argc</font> check and a usage message using <font face=\"Courier\">argv[0]</font>.",
                "Explain why reading <font face=\"Courier\">argv[2]</font> is unsafe when <font face=\"Courier\">argc == 2</font>.",
                "For <font face=\"Courier\">./prog \"hello world\" 3</font>, how many user-supplied arguments are there and what is <font face=\"Courier\">argv[1]</font>?",
                "Use <font face=\"Courier\">atoi</font> to parse <font face=\"Courier\">argv[1]</font>, then state the weakness of this approach.",
                "What does <font face=\"Courier\">atoi(\"abc\")</font> return, and why is that a problem?",
                "In a <font face=\"Courier\">strtol</font> parse, what does <font face=\"Courier\">end == text</font> mean?",
                "In a <font face=\"Courier\">strtol</font> parse, why check <font face=\"Courier\">*end == '\\0'</font>?",
                "Write a small argument-handling outline for a program that expects <font face=\"Courier\">name</font> and <font face=\"Courier\">count</font>, then prints the name <font face=\"Courier\">count</font> times.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Strong answers separate argument counting from argument parsing.", styles, "SourceText"),
        numbered(
            [
                "<font face=\"Courier\">argc == 3</font>. <font face=\"Courier\">argv[0]</font> is the program path/name, often <font face=\"Courier\">./prog</font>; <font face=\"Courier\">argv[1]</font> is <font face=\"Courier\">alpha</font>; <font face=\"Courier\">argv[2]</font> is <font face=\"Courier\">beta</font>.",
                "Expected: <font face=\"Courier\">int main(int argc, char *argv[])</font> or equivalent <font face=\"Courier\">char **argv</font>.",
                "Expected pattern: <font face=\"Courier\">if (argc != 2) { fprintf(stderr, \"usage: %s file\\n\", argv[0]); return 1; }</font>.",
                "When <font face=\"Courier\">argc == 2</font>, valid indexes are only <font face=\"Courier\">0</font> and <font face=\"Courier\">1</font>. <font face=\"Courier\">argv[2]</font> is past the supplied argument list.",
                "There are two user-supplied arguments. <font face=\"Courier\">argv[1]</font> is the single string <font face=\"Courier\">hello world</font> because quotes keep the space inside one argument.",
                "Expected: <font face=\"Courier\">int n = atoi(argv[1]);</font>. Weakness: invalid input and real zero can both produce <font face=\"Courier\">0</font>, so errors are not reliably detected.",
                "It returns <font face=\"Courier\">0</font>. That is a problem because <font face=\"Courier\">0</font> is also a valid parsed integer.",
                "It means no characters were converted, so the string did not start with a valid number.",
                "It rejects strings with trailing junk. For example, <font face=\"Courier\">12abc</font> should not be accepted as a clean integer.",
                "Expected outline: check <font face=\"Courier\">argc == 3</font>, parse <font face=\"Courier\">argv[2]</font> as an integer, reject bad or negative counts, then loop and print <font face=\"Courier\">argv[1]</font>.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Forgetting that <font face=\"Courier\">argv[0]</font> is the program name, not the first user argument.",
                "Checking <font face=\"Courier\">argc == 2</font> and then reading <font face=\"Courier\">argv[2]</font>.",
                "Using <font face=\"Courier\">atoi</font> as if it can report invalid input clearly.",
                "Assuming quote characters are included in the strings passed to the program.",
                "Parsing numbers before checking that the argument exists.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
