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


OUT = Path(__file__).with_name("c-files-streams-study-pack.pdf")


def make_styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="TopicTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            textColor=colors.HexColor("#111827"),
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            name="TopicBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=12,
            textColor=colors.HexColor("#111827"),
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            name="SourceText",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            name="BlueHeading",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=17,
            textColor=colors.HexColor("#1d4ed8"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            name="DarkHeading",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=colors.HexColor("#111827"),
            spaceBefore=6,
            spaceAfter=3,
        )
    )
    base.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.4,
            leading=9.1,
            backColor=colors.HexColor("#f3f4f6"),
            borderColor=colors.HexColor("#d1d5db"),
            borderWidth=0.4,
            borderPadding=4,
            spaceAfter=7,
        )
    )
    return base


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
        title="C Files and Streams Study Pack",
    )

    story = [
        p("C Files and Streams", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 files and streams material: "
            "L08 Files and Streams plus the red items in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Streams and standard streams", styles, "DarkHeading"),
        p(
            "A stream is an abstraction used for input/output. It gives the programmer a consistent interface "
            "regardless of the actual device or file. The standard streams are `stdin`, `stdout`, and `stderr`.",
            styles,
        ),
        bullets(
            [
                "A stream may be text or binary.",
                "Text streams are sequences of characters, and character translation may happen.",
                "Binary streams are sequences of bytes, with no character translation.",
                "Streams are buffered, so output is not always written immediately.",
            ],
            styles,
        ),
        p("2. Opening and closing files", styles, "DarkHeading"),
        p(
            "Use `FILE *` to hold a stream pointer. Open a file with `fopen`, check for `NULL`, then close it with "
            "`fclose` when finished.",
            styles,
        ),
        code(
            """
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    return 1;
}

/* use the file here */

fclose(fp);
            """,
            styles,
        ),
        p(
            "Common modes: `r`, `w`, `a` for text; `rb`, `wb`, `ab` for binary; `r+`, `w+`, `a+` for read/write.",
            styles,
        ),
        p("3. Console input and `scanf`", styles, "DarkHeading"),
        p(
            "`scanf` is formatted input. It returns the number of items successfully assigned, so it must be checked. "
            "For numeric input, pass the address of the variable.",
            styles,
        ),
        code(
            """
int k;
if (scanf("%d", &k) != 1) {
    /* input failed */
}
            """,
            styles,
        ),
        p("4. Reading and writing streams", styles, "DarkHeading"),
        bullets(
            [
                "`fgetc` / `getc`: read one character.",
                "`fputc` / `putc`: write one character.",
                "`fgets`: read a line or up to a size limit, and adds a null terminator.",
                "`fputs`: write a string, but not its null terminator.",
                "`fprintf`: like `printf`, but writes to a stream.",
                "`fscanf`: like `scanf`, but reads from a stream.",
            ],
            styles,
        ),
        p("5. Buffering and flushing", styles, "DarkHeading"),
        p(
            "Because streams are buffered, printed output may not appear immediately. `fflush(fp)` forces the output "
            "buffer for that stream to be written out. This matters for files and can matter for visible output timing.",
            styles,
        ),
        p("6. Error handling: `errno`, `strerror`, and `ferror`", styles, "DarkHeading"),
        p(
            "`errno` is updated by many library or system calls when an error occurs. The important exam rule is that "
            "you only inspect `errno` after an actual failure. A successful call does not reset it for you.",
            styles,
        ),
        code(
            """
FILE *fp = fopen(path, "r");
if (fp == NULL) {
    printf("Unable to read file %s: %d: %s\\n", path, errno, strerror(errno));
    return 1;
}
            """,
            styles,
        ),
        bullets(
            [
                "`ferror(fp)` checks whether the most recent file operation produced an error.",
                "`feof(fp)` tells you whether end-of-file has been reached.",
                "Do not write loops of the form `while (!feof(fp))` as the main control logic; check the read result instead.",
            ],
            styles,
        ),
        p("7. File position functions", styles, "DarkHeading"),
        p(
            "`rewind(fp)` resets the file position indicator to the start of the file. `fseek(stream, offset, whence)` "
            "moves the file position relative to the beginning, end, or current position.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Explain the difference between a text stream and a binary stream.",
                "Write the code to open `numbers.txt` for reading and safely handle failure.",
                "State what `scanf` returns and why `scanf(\"%d\", &k)` uses `&k`.",
                "Name three common stream input/output functions and say what each does.",
                "Explain why output from `printf` or `fprintf` may not appear immediately.",
                "State when it is valid to inspect `errno` and why checking it after a successful call is wrong.",
                "Explain the difference between `ferror(fp)` and `feof(fp)`.",
                "Write the code to rewind a file and then move 20 bytes from the beginning using `fseek`.",
                "Why is `while (!feof(fp))` usually a bad pattern for reading a file?",
                "Write a short code fragment that opens a file, writes one line with `fprintf`, flushes it, and closes it.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Marks should reward correct terminology and correct error-handling steps.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "A text stream is a sequence of characters and translation may occur, such as newline translation. A binary stream is a sequence of bytes and no character translation occurs.",
                "Expected pattern: `FILE *fp = fopen(\"numbers.txt\", \"r\"); if (fp == NULL) { ... }`. Full credit requires checking for `NULL` before use.",
                "`scanf` returns the number of items successfully assigned. `&k` is needed because `scanf` must write into the caller's variable, so it needs the address of `k`.",
                "Any correct three such as: `fgetc` reads one character, `fgets` reads a string/line up to a limit, `fprintf` writes formatted output to a stream, `fputc` writes one character, `fscanf` reads formatted input from a stream.",
                "Streams are buffered, so output may be held in memory before being written to the device or file. `fflush` forces the buffered output to be written.",
                "Inspect `errno` only after a function has actually failed, such as `fopen` returning `NULL`. A successful call may leave an old nonzero `errno`, so reading it after success is misleading.",
                "`ferror(fp)` reports whether the most recent file operation caused an error. `feof(fp)` reports whether end-of-file has been reached.",
                "Expected pattern: `rewind(fp); fseek(fp, 20, SEEK_SET);`.",
                "Because end-of-file is only known after a read attempt fails. Good file-reading logic checks the result of `fgets`, `fscanf`, `fgetc`, or similar directly.",
                "Expected pattern: open with `fopen`, check for `NULL`, call `fprintf(fp, ...)`, optionally `fflush(fp)`, then `fclose(fp)`.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main(void) {
    FILE *fp = fopen("out.txt", "w");
    if (fp == NULL) {
        printf("open failed: %d: %s\\n", errno, strerror(errno));
        return 1;
    }

    fprintf(fp, "Value = %d\\n", 42);
    fflush(fp);
    fclose(fp);
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
