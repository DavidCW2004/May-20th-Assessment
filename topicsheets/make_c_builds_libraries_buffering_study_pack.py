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


OUT = Path(__file__).with_name("c-builds-libraries-buffering-study-pack.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TopicTitle", parent=styles["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#111827"), spaceAfter=8))
    styles.add(ParagraphStyle("TopicBody", parent=styles["Normal"], fontSize=9.1, leading=11.6, textColor=colors.HexColor("#111827"), spaceAfter=5))
    styles.add(ParagraphStyle("SourceText", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#4b5563"), spaceAfter=6))
    styles.add(ParagraphStyle("BlueHeading", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#1d4ed8"), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle("DarkHeading", parent=styles["Heading3"], fontSize=11, leading=13, textColor=colors.HexColor("#111827"), spaceBefore=6, spaceAfter=3))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.0, leading=8.4, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=6))
    return styles


def p(text, styles, style="TopicBody"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=92)


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
        title="C Builds, Libraries, and Stream Buffering Study Pack",
    )

    story = [
        p("C Builds, Libraries, and Stream Buffering", styles, "TopicTitle"),
        p(
            "Grounded in ECM2433 L08 files/streams and L10 program structure: stream buffering, setbuf, raw read/write, separate compilation, object files, libraries, and Makefiles.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),
        p("1. Streams are buffered", styles, "DarkHeading"),
        p(
            "A stream is an abstraction over input/output. Output is often stored in memory first, then written to the actual device later. This is buffering. A write call such as printf or fprintf may update the stream buffer without immediately showing text on screen or writing bytes to disk.",
            styles,
        ),
        bullets(
            [
                "Output to a terminal is commonly line-buffered, so a newline may flush it.",
                "Output may also be flushed when the buffer is full.",
                "The buffer size is implementation-dependent; lecture notes mention that 8192 bytes is common.",
                "Use <font face=\"Courier\">fflush(stdout)</font> or <font face=\"Courier\">fflush(fp)</font> when pending output must be forced out immediately.",
            ],
            styles,
        ),
        code(
            """
printf("Step 1, ");
fflush(stdout);      /* force pending stdout text to appear now */
printf("Step 2\\n"); /* newline may also flush terminal output */
            """,
            styles,
        ),
        p("2. setbuf and raw read/write", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">setbuf</font> changes the buffering used by a stream. Passing <font face=\"Courier\">NULL</font> requests unbuffered stream I/O. Raw unbuffered I/O can also be done with lower-level <font face=\"Courier\">read</font> and <font face=\"Courier\">write</font>, which work with file descriptors rather than <font face=\"Courier\">FILE *</font> streams.",
            styles,
        ),
        code(
            """
#include <stdio.h>

int main(void) {
    setbuf(stdout, NULL);  /* request unbuffered stdout */
    printf("appears without waiting for a full buffer");
    return 0;
}
            """,
            styles,
        ),
        p(
            "Do not mix up stream I/O and raw I/O. <font face=\"Courier\">fprintf</font>, <font face=\"Courier\">fgets</font>, and <font face=\"Courier\">fflush</font> use <font face=\"Courier\">FILE *</font>. Low-level <font face=\"Courier\">read</font> and <font face=\"Courier\">write</font> use integer file descriptors.",
            styles,
        ),
        p("3. Separate compilation and object files", styles, "DarkHeading"),
        p(
            "A larger C program is often split into multiple source files. Each <font face=\"Courier\">.c</font> file can be compiled into an object file with <font face=\"Courier\">gcc -c</font>. Object files contain compiled code, but they are not the final executable until the linker combines them.",
            styles,
        ),
        code(
            """
gcc -std=c99 -c stack.c -o stack.o
gcc -std=c99 -c main.c -o main.o
gcc main.o stack.o -o program
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">stack.c</font> can compile to <font face=\"Courier\">stack.o</font> even if it has no <font face=\"Courier\">main</font> function.",
                "The final executable needs one <font face=\"Courier\">main</font> somewhere.",
                "Object files can be reused with different programs without recompiling the original source every time.",
            ],
            styles,
        ),
        p("4. Linking and libraries", styles, "DarkHeading"),
        p(
            "Linking resolves calls between object files and libraries. A library is a collection of object files packaged as one unit. Static libraries become part of the application at link time. Shared libraries are linked at runtime.",
            styles,
        ),
        code(
            """
gcc -c myMaths.c -o myMaths.o
gcc myMaths.o -lm -o myMaths
            """,
            styles,
        ),
        p(
            "In this example, <font face=\"Courier\">-lm</font> asks the linker to use the maths library, usually named <font face=\"Courier\">libm.so</font> or <font face=\"Courier\">libm.a</font>. Including <font face=\"Courier\">math.h</font> gives declarations to the compiler, but the linker still needs the library that contains the implementation.",
            styles,
        ),
        p("5. Makefiles and dependencies", styles, "DarkHeading"),
        p(
            "A Makefile records targets, prerequisites, and commands. The target is what you want to build. The prerequisites are the files it depends on. The command is how to build it. Commands must be indented with a tab.",
            styles,
        ),
        code(
            """
CC = gcc
CFLAGS = -std=c99

program: main.o stack.o
<TAB>$(CC) $(CFLAGS) main.o stack.o -o program

main.o: main.c stack.h
<TAB>$(CC) $(CFLAGS) -c main.c -o main.o

stack.o: stack.c stack.h
<TAB>$(CC) $(CFLAGS) -c stack.c -o stack.o

clean:
<TAB>rm -f *.o program
            """,
            styles,
        ),
        p(
            "The first target is the default target. <font face=\"Courier\">make</font> rebuilds a target only when the target is missing or one of its prerequisites is newer. If <font face=\"Courier\">stack.h</font> changes, both <font face=\"Courier\">main.o</font> and <font face=\"Courier\">stack.o</font> may need rebuilding because both depend on the header.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        p("Question 1 - trace buffered output:", styles),
        code(
            """
printf("A");
printf("B");
fflush(stdout);
printf("C\\n");
            """,
            styles,
        ),
        numbered(["Explain what <font face=\"Courier\">fflush(stdout)</font> changes in this fragment."], styles),
        p("Question 2 - choose the right I/O layer:", styles),
        code(
            """
FILE *fp = fopen("out.txt", "w");
int fd = 1;
            """,
            styles,
        ),
        numbered(["For each variable, say whether it belongs with <font face=\"Courier\">fprintf</font>/<font face=\"Courier\">fflush</font> or with raw <font face=\"Courier\">write</font>."], styles, start=2),
        p("Question 3 - identify the missing build step:", styles),
        code(
            """
gcc -std=c99 -c main.c -o main.o
gcc -std=c99 -c stack.c -o stack.o
            """,
            styles,
        ),
        numbered(["Write the command that links these two object files into an executable called <font face=\"Courier\">program</font>."], styles, start=3),
        p("Question 4 - header vs library:", styles),
        code(
            """
#include <math.h>

int main(void) {
    return cosf(0.0f) == 1.0f ? 0 : 1;
}
            """,
            styles,
        ),
        numbered(["The compile succeeds but linking reports <font face=\"Courier\">undefined reference to cosf</font>. Give the link command fix and explain why the header alone was not enough."], styles, start=4),
        p("Question 5 - reuse an object file:", styles),
        code(
            """
stack.o already exists
main.c changed
stack.c did not change
            """,
            styles,
        ),
        numbered(["Give the compile/link commands that avoid recompiling <font face=\"Courier\">stack.c</font>."], styles, start=5),
        p("Question 6 - complete a Makefile rule:", styles),
        code(
            """
stack.o: stack.c stack.h
<TAB>/* command goes here */
            """,
            styles,
        ),
        numbered(["Write the command for this rule."], styles, start=6),
        p("Question 7 - decide what rebuilds:", styles),
        code(
            """
program: main.o stack.o
main.o: main.c stack.h
stack.o: stack.c stack.h
            """,
            styles,
        ),
        numbered(["If only <font face=\"Courier\">stack.h</font> changes, which targets should be rebuilt when making <font face=\"Courier\">program</font>?"], styles, start=7),
        p("Question 8 - find the Makefile bug:", styles),
        code(
            """
program: main.o stack.o
    gcc main.o stack.o -o program
            """,
            styles,
        ),
        numbered(["This command line is indented with spaces. Explain the problem and the fix."], styles, start=8),
        p("Question 9 - explain up-to-date behaviour:", styles),
        code(
            """
$ make program
make: 'program' is up to date
            """,
            styles,
        ),
        numbered(["What does this message mean about the target and its prerequisites?"], styles, start=9),
        p("Question 10 - complete the clean target:", styles),
        code(
            """
clean:
<TAB>/* command goes here */
            """,
            styles,
        ),
        numbered(["Write a suitable command for removing object files and the executable."], styles, start=10),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "<font face=\"Courier\">fflush(stdout)</font> forces pending buffered stdout output to be written immediately. Without it, <font face=\"Courier\">A</font> and <font face=\"Courier\">B</font> might sit in the buffer until newline, full buffer, or program exit.",
                "<font face=\"Courier\">fp</font> is a stream pointer for <font face=\"Courier\">fprintf</font>/<font face=\"Courier\">fflush</font>. <font face=\"Courier\">fd</font> is an integer file descriptor for raw <font face=\"Courier\">write</font>.",
                "<font face=\"Courier\">gcc main.o stack.o -o program</font>.",
                "Use <font face=\"Courier\">gcc main.o -lm -o program</font> or equivalent. <font face=\"Courier\">math.h</font> declares <font face=\"Courier\">cosf</font> for the compiler; <font face=\"Courier\">-lm</font> supplies the library implementation to the linker.",
                "Compile only <font face=\"Courier\">main.c</font>: <font face=\"Courier\">gcc -std=c99 -c main.c -o main.o</font>, then link <font face=\"Courier\">gcc main.o stack.o -o program</font>.",
                "<font face=\"Courier\">$(CC) $(CFLAGS) -c stack.c -o stack.o</font> or <font face=\"Courier\">gcc -std=c99 -c stack.c -o stack.o</font>.",
                "<font face=\"Courier\">main.o</font> and <font face=\"Courier\">stack.o</font> are rebuilt because both depend on <font face=\"Courier\">stack.h</font>. Then <font face=\"Courier\">program</font> is relinked.",
                "Makefile commands must start with a tab. Replace the leading spaces before <font face=\"Courier\">gcc</font> with a tab.",
                "The target exists and is newer than, or at least not older than, its prerequisites, so no command needs to run.",
                "Expected: <font face=\"Courier\">rm -f *.o program</font>.",
            ],
            styles,
        ),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
