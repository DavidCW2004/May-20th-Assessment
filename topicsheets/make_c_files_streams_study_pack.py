from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, Preformatted, SimpleDocTemplate


OUT = Path(__file__).with_name("c-files-streams-study-pack.pdf")


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
    return ListFlowable([ListItem(p(item, styles), leftIndent=4 * mm) for item in items], bulletType="bullet", leftIndent=6 * mm, bulletFontName="Helvetica", bulletFontSize=7)


def numbered(items, styles):
    return ListFlowable([ListItem(p(item, styles), leftIndent=5 * mm) for item in items], bulletType="1", leftIndent=7 * mm, bulletFontName="Helvetica-Bold", bulletFontSize=8)


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm, title="C Files and Streams Study Pack")
    story = [
        p("C Files and Streams", styles, "TopicTitle"),
        p("Based on ECM2433 L08 files and streams: standard streams, file modes, buffering, errno, ferror, feof, fseek, and rewind.", styles, "SourceText"),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Streams and standard streams", styles, "DarkHeading"),
        p("A stream is an input/output abstraction. The standard streams are stdin, stdout, and stderr. Streams may be text or binary and are usually buffered.", styles),
        p("2. Opening and closing files", styles, "DarkHeading"),
        code("""
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    return 1;
}

/* use fp */

fclose(fp);
        """, styles),
        p("Common modes include r, w, and a for text files, and rb, wb, and ab for binary files.", styles),
        p("3. Formatted console input", styles, "DarkHeading"),
        p("scanf returns the number of items successfully assigned. For numeric input, pass the address of the variable so scanf can write into it.", styles),
        code("""
int k;
if (scanf("%d", &k) != 1) {
    fprintf(stderr, "bad integer\\n");
    return 1;
}
        """, styles),
        p("4. Stream reading and writing", styles, "DarkHeading"),
        bullets([
            "<font face=\"Courier\">fgetc</font> reads one character.",
            "<font face=\"Courier\">fputc</font> writes one character.",
            "<font face=\"Courier\">fgets</font> reads a line or up to a size limit.",
            "<font face=\"Courier\">fputs</font> writes a string without its null terminator.",
            "<font face=\"Courier\">fprintf</font> writes formatted output to a stream.",
            "<font face=\"Courier\">fscanf</font> reads formatted input from a stream.",
        ], styles),
        p("5. Buffering and flushing", styles, "DarkHeading"),
        p("Output may be held in a buffer before it appears. Use fflush on an output stream when the buffered data must be written immediately.", styles),
        p("6. Errors and file positions", styles, "DarkHeading"),
        p("Inspect errno only after an actual failure. After read loops, use ferror to detect an error and feof to detect end-of-file. Use rewind and fseek to control the file position.", styles),
        code("""
rewind(fp);
fseek(fp, 20, SEEK_SET);
        """, styles),
        p("Practice Questions", styles, "BlueHeading"),
        numbered([
            "Explain the difference between a text stream and a binary stream.",
            "Write code to open <font face=\"Courier\">numbers.txt</font> for reading and handle failure safely.",
            "State what <font face=\"Courier\">scanf</font> returns and why numeric input needs the variable address.",
            "Name three stream input/output functions and say what each does.",
            "Explain why output from <font face=\"Courier\">printf</font> or <font face=\"Courier\">fprintf</font> may not appear immediately.",
            "State when it is valid to inspect <font face=\"Courier\">errno</font>.",
            "Explain the difference between <font face=\"Courier\">ferror(fp)</font> and <font face=\"Courier\">feof(fp)</font>.",
            "Write the calls to rewind a file and then move to byte offset 20 from the beginning.",
            "Explain why <font face=\"Courier\">while (!feof(fp))</font> is usually a bad file-reading loop pattern.",
            "Write a short fragment that opens a file, writes one line, flushes it, and closes it.",
        ], styles),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions.", styles, "SourceText"),
        numbered([
            "Text streams contain characters and may perform translations such as newline handling. Binary streams contain bytes with no translation.",
            "Expected pattern: <font face=\"Courier\">FILE *fp = fopen(\"numbers.txt\", \"r\");</font>, then check <font face=\"Courier\">fp == NULL</font> before use.",
            "It returns the number of successful assignments. Numeric input uses the variable address because scanf must write into the caller's object.",
            "Examples: fgetc reads a character, fgets reads a line up to a limit, fprintf writes formatted output to a stream.",
            "Streams are buffered. fflush forces buffered output to be written.",
            "Only inspect errno after a call has failed, such as fopen returning NULL. A successful call does not necessarily clear an old errno.",
            "ferror reports a stream error. feof reports that end-of-file has been reached after a read attempt.",
            "Expected: <font face=\"Courier\">rewind(fp); fseek(fp, 20, SEEK_SET);</font>.",
            "EOF is only known after a read attempt fails. Check the read function result directly instead.",
            "Open with fopen, check for NULL, call fprintf, call fflush if immediate output matters, then fclose.",
        ], styles),
        p("Useful Pattern", styles, "BlueHeading"),
        code("""
#include <errno.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *fp = fopen("out.txt", "w");
    if (fp == NULL) {
        fprintf(stderr, "open failed: %s\\n", strerror(errno));
        return 1;
    }

    fprintf(fp, "Value = %d\\n", 42);
    fflush(fp);
    fclose(fp);
    return 0;
}
        """, styles),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
