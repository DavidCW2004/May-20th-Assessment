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


OUT = Path(__file__).with_name("c-memory-debugging-tools-study-pack.pdf")


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
        title="C Memory Debugging Tools Study Pack",
    )

    story = [
        p("C Memory Debugging Tools", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: Valgrind and address sanitiser for memory bugs.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. What these tools are for", styles, "DarkHeading"),
        p(
            "C lets you write outside arrays, use freed memory, leak allocations, and dereference invalid pointers. The compiler often cannot prove these mistakes from the source alone. Runtime memory tools run your program and report bad memory behaviour as it happens.",
            styles,
        ),
        bullets(
            [
                "AddressSanitizer: compiler instrumentation added at build time.",
                "Valgrind Memcheck: runs the program under a memory-checking tool.",
                "Both are for finding bugs such as out-of-bounds access, use-after-free, invalid reads/writes, and leaks.",
            ],
            styles,
        ),
        p("2. Compile with debug information", styles, "DarkHeading"),
        p(
            "Debug information lets tool reports point at useful source file names and line numbers. Use <font face=\"Courier\">-g</font> when building test/debug versions.",
            styles,
        ),
        code(
            """
gcc -g -Wall -Wextra -o app main.c
            """,
            styles,
        ),
        p(
            "Warnings are not a replacement for memory tools, but <font face=\"Courier\">-Wall -Wextra</font> catches many simple mistakes before runtime.",
            styles,
        ),
        p("3. AddressSanitizer", styles, "DarkHeading"),
        p(
            "AddressSanitizer, often shortened to ASan, is enabled by compiling and linking with <font face=\"Courier\">-fsanitize=address</font>. It makes the program slower, but it usually gives clear reports for memory errors.",
            styles,
        ),
        code(
            """
gcc -g -Wall -Wextra -fsanitize=address -o app main.c
./app
            """,
            styles,
        ),
        p(
            "A typical ASan report names the error type, such as stack-buffer-overflow or heap-use-after-free, and shows where the bad access happened.",
            styles,
        ),
        p("4. Example: out-of-bounds array write", styles, "DarkHeading"),
        code(
            """
#include <stdio.h>

int main(void) {
    int a[5] = {0};

    for (int i = 0; i <= 5; i++) {
        a[i] = i;
    }

    printf("%d\\n", a[0]);
    return 0;
}
            """,
            styles,
        ),
        p(
            "The bug is <font face=\"Courier\">i &lt;= 5</font>. Valid indexes are 0 to 4. ASan should report a stack-buffer-overflow because <font face=\"Courier\">a[5]</font> is one element past the array.",
            styles,
        ),
        code(
            """
for (int i = 0; i < 5; i++) {
    a[i] = i;
}
            """,
            styles,
        ),
        p("5. Example: use-after-free", styles, "DarkHeading"),
        code(
            """
#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof *p);
    if (p == NULL) {
        return 1;
    }

    *p = 42;
    free(p);

    return *p;  /* bug: p points at freed memory */
}
            """,
            styles,
        ),
        p(
            "After <font face=\"Courier\">free(p)</font>, the allocation no longer belongs to the program. Reading or writing through <font face=\"Courier\">p</font> is undefined behaviour. A common defensive pattern is to set the pointer to <font face=\"Courier\">NULL</font> after freeing if it may be used again.",
            styles,
        ),
        p("6. Valgrind Memcheck", styles, "DarkHeading"),
        p(
            "Valgrind runs an already-built program under a checker. It is slower than normal execution, but it is very useful for finding leaks and invalid memory use.",
            styles,
        ),
        code(
            """
gcc -g -Wall -Wextra -o app main.c
valgrind --leak-check=full --track-origins=yes ./app
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">Invalid read</font> or <font face=\"Courier\">Invalid write</font>: your program accessed memory it should not access.",
                "<font face=\"Courier\">Use of uninitialised value</font>: a value was read before being assigned.",
                "<font face=\"Courier\">definitely lost</font>: allocated memory was leaked because no pointer to it remains.",
                "<font face=\"Courier\">still reachable</font>: memory remains allocated at exit but is still pointed to.",
            ],
            styles,
        ),
        p("7. Example: memory leak", styles, "DarkHeading"),
        code(
            """
#include <stdlib.h>

int main(void) {
    int *values = malloc(10 * sizeof *values);
    if (values == NULL) {
        return 1;
    }

    values[0] = 99;
    return 0;  /* bug: missing free(values) */
}
            """,
            styles,
        ),
        p(
            "Valgrind should report this allocation as definitely lost. Fix it by freeing every successful allocation when the program no longer needs it.",
            styles,
        ),
        code(
            """
free(values);
return 0;
            """,
            styles,
        ),
        p("8. Reading reports pragmatically", styles, "DarkHeading"),
        numbered(
            [
                "Find the first reported invalid access. Later reports may be consequences.",
                "Use the file and line number to locate the exact operation.",
                "Identify the allocation, free, or stack object involved.",
                "Fix the ownership or bounds bug in the source code.",
                "Run the tool again to check that the report is gone.",
            ],
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write a GCC command that builds <font face=\"Courier\">main.c</font> with debug information, warnings, and AddressSanitizer.",
                "A loop writes <font face=\"Courier\">a[i]</font> for <font face=\"Courier\">i &lt;= 5</font> when <font face=\"Courier\">a</font> has five elements. Name the bug and fix the loop condition.",
                "Explain why reading <font face=\"Courier\">*p</font> after <font face=\"Courier\">free(p)</font> is invalid.",
                "Write a Valgrind command that enables full leak checking for <font face=\"Courier\">./app</font>.",
                "A Valgrind report says <font face=\"Courier\">definitely lost</font>. What kind of bug does that usually mean?",
                "Explain why <font face=\"Courier\">-g</font> is useful when running memory debugging tools.",
                "Given a function with three early returns after <font face=\"Courier\">malloc</font>, describe the cleanup issue you would check for.",
                "Which tool is enabled at compile time: AddressSanitizer or Valgrind?",
                "Which report should you usually investigate first when a tool prints many memory errors?",
                "Give one reason these tools are useful even when the program appears to print the correct answer.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Strong answers should connect each report to the underlying ownership or bounds mistake.", styles, "SourceText"),
        numbered(
            [
                "Expected: <font face=\"Courier\">gcc -g -Wall -Wextra -fsanitize=address -o app main.c</font>.",
                "It is an out-of-bounds write. Valid indexes for five elements are 0 to 4, so use <font face=\"Courier\">i &lt; 5</font>.",
                "After <font face=\"Courier\">free</font>, the allocation no longer belongs to the program. The pointer value is stale, so dereferencing it is undefined behaviour.",
                "Expected: <font face=\"Courier\">valgrind --leak-check=full ./app</font>; <font face=\"Courier\">--track-origins=yes</font> is also useful.",
                "It usually means allocated memory was leaked and no pointer to that allocation remains at program exit.",
                "<font face=\"Courier\">-g</font> includes source-level debug information so reports can name useful files and line numbers.",
                "Check whether every path after a successful allocation frees the allocation before returning.",
                "AddressSanitizer is enabled at compile/link time with <font face=\"Courier\">-fsanitize=address</font>.",
                "Usually start with the first invalid read/write, because later errors may be consequences of earlier corruption.",
                "Memory bugs are undefined behaviour. A program can appear to work while still corrupting memory, leaking allocations, or relying on invalid reads.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Trying to run AddressSanitizer without compiling with <font face=\"Courier\">-fsanitize=address</font>.",
                "Ignoring the first memory error and only looking at the final summary.",
                "Treating a leak as harmless because the program exits soon afterwards.",
                "Forgetting that one missing <font face=\"Courier\">free</font> on an error path is still a leak.",
                "Assuming correct output means the memory accesses were valid.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
