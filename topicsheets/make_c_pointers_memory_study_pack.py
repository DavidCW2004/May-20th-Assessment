from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, Preformatted, SimpleDocTemplate


OUT = Path(__file__).with_name("c-pointers-memory-study-pack.pdf")


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
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm, title="C Pointers and Memory Study Pack")

    story = [
        p("C Pointers and Memory", styles, "TopicTitle"),
        p("Based on ECM2433 pointer, arrays/strings, functions-with-pointers, and dynamic-memory material.", styles, "SourceText"),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Pointers store addresses", styles, "DarkHeading"),
        p("The address-of operator produces an address. A pointer stores an address. Dereferencing a pointer accesses the object at that address.", styles),
        code("""
int x = 4;
int *p = &x;
*p = 9;
printf("%d\\n", x);  /* 9 */
        """, styles),
        p("2. Arrays, strings, and bounds", styles, "DarkHeading"),
        p("Arrays are contiguous memory. C does not reliably stop out-of-bounds access. A C string is a char array ending with a null terminator.", styles),
        code("""
char s[] = "Hello";  /* H e l l o \\0 */
printf("%zu\\n", sizeof s);  /* 6 for this array */
printf("%zu\\n", strlen(s)); /* 5 visible characters */
        """, styles),
        p("3. Passing pointers to functions", styles, "DarkHeading"),
        p("C passes arguments by value. To update the caller's object, pass its address and write through the pointer.", styles),
        code("""
void update_integer(int *p) {
    *p = 42;
}

int value = 5;
update_integer(&value);
        """, styles),
        p("4. Dynamic memory", styles, "DarkHeading"),
        p("Use malloc for heap allocation, check for NULL, stay within bounds, and free each successful allocation exactly once.", styles),
        code("""
int *a = malloc(n * sizeof *a);
if (a == NULL) {
    return 1;
}

for (int i = 0; i < n; i++) {
    a[i] = i + 1;
}

free(a);
a = NULL;
        """, styles),
        p("5. Common memory bugs", styles, "DarkHeading"),
        bullets([
            "Wild pointer: using a pointer that was never initialised.",
            "Dangling pointer: using a pointer after the object it pointed at no longer exists.",
            "Double-free: freeing the same allocation twice.",
            "Memory leak: losing the last pointer to allocated memory before freeing it.",
            "Out-of-bounds access: reading or writing outside the valid range.",
        ], styles),
        p("Practice Questions", styles, "BlueHeading"),
        numbered([
            "In the code <font face=\"Courier\">int x = 4; int *p = &#38;x;</font>, identify the value, the address of <font face=\"Courier\">x</font>, the pointer value, and the dereferenced value.",
            "Predict the output after <font face=\"Courier\">*p = *p + 3</font> when <font face=\"Courier\">p</font> points at <font face=\"Courier\">x</font> and <font face=\"Courier\">x</font> starts at 4.",
            "Write a function that sets a caller-owned integer to 42 through a pointer parameter.",
            "Write a pointer-based integer swap function.",
            "For <font face=\"Courier\">char s[20] = \"Hello\";</font>, compare <font face=\"Courier\">sizeof s</font> and <font face=\"Courier\">strlen(s)</font>.",
            "Explain why writing <font face=\"Courier\">array[15]</font> is unsafe when an array has 10 elements.",
            "Write code that allocates <font face=\"Courier\">n</font> integers, checks allocation, fills them, and frees them.",
            "Explain the bug in <font face=\"Courier\">char *p; strcpy(p, \"Hello\");</font> and give a safe fix.",
            "Outline the allocation and cleanup pattern for a dynamic 2D array using <font face=\"Courier\">int **X</font>.",
            "Classify these bugs: use after free, double free, forgotten free, and dereferencing an uninitialised pointer.",
        ], styles),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Correct reasoning matters as much as final code.", styles, "SourceText"),
        numbered([
            "<font face=\"Courier\">x</font> is the integer object; the address of <font face=\"Courier\">x</font> is produced with the address-of operator; <font face=\"Courier\">p</font> stores that address; <font face=\"Courier\">*p</font> is the integer stored there.",
            "The output is <font face=\"Courier\">7</font>. The pointer refers to <font face=\"Courier\">x</font>, so assigning through it changes <font face=\"Courier\">x</font>.",
            "Expected pattern: <font face=\"Courier\">void update_integer(int *p) { *p = 42; }</font>, called by passing the address of the caller's variable.",
            "Expected body: <font face=\"Courier\">int tmp = *p; *p = *q; *q = tmp;</font>.",
            "<font face=\"Courier\">sizeof s</font> is 20 bytes for the whole array. <font face=\"Courier\">strlen(s)</font> is 5 because it counts visible characters before the null terminator.",
            "It writes outside the valid range. The behaviour is undefined: it may corrupt memory, crash, or appear to work.",
            "Use <font face=\"Courier\">malloc(n * sizeof *a)</font>, check for <font face=\"Courier\">NULL</font>, loop over valid indexes, then <font face=\"Courier\">free(a)</font>.",
            "The pointer is uninitialised and does not point at writable storage. Safe fixes include a large enough char array or allocated storage with a NULL check.",
            "Allocate the row-pointer array, allocate each row, clean up earlier rows if a later row fails, then free rows and finally the row-pointer array.",
            "Use-after-free/dangling pointer; double-free; memory leak; wild pointer or undefined behaviour.",
        ], styles),
        p("Useful 2D Cleanup Pattern", styles, "BlueHeading"),
        code("""
int **X = malloc(R * sizeof *X);
if (X == NULL) {
    return 1;
}

for (int r = 0; r < R; r++) {
    X[r] = malloc(C * sizeof *X[r]);
    if (X[r] == NULL) {
        for (int i = 0; i < r; i++) {
            free(X[i]);
        }
        free(X);
        return 1;
    }
}

for (int r = 0; r < R; r++) {
    free(X[r]);
}
free(X);
        """, styles),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
