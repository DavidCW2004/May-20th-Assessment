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
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.25, leading=8.8, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=7))
    return styles


def p(text, styles, style="TopicBody"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=88)


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
        title="C Pointers, Arrays, and Generic Memory Study Pack",
    )

    story = [
        p("C Pointers, Arrays, and Generic Memory", styles, "TopicTitle"),
        p(
            "Merged sheet based on ECM2433 arrays/strings, functions with pointers, "
            "dynamic memory, 2D arrays, pointer arithmetic, and generic void-pointer "
            "programming material.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),
        p("1. Pointers, dereferencing, and caller updates", styles, "DarkHeading"),
        p(
            "A pointer stores an address. The address-of operator gets an address; "
            "dereferencing accesses the object at that address. C passes arguments by "
            "value, so a function updates the caller's variable by receiving a pointer.",
            styles,
        ),
        code(
            """
void set_to_42(int *p) {
    *p = 42;
}

int value = 5;
set_to_42(&value);
            """,
            styles,
        ),
        p("2. Arrays, strings, and allocation", styles, "DarkHeading"),
        p(
            "Arrays are contiguous. A C string is a character array ending in "
            "<font face=\"Courier\">'\\0'</font>. Dynamic memory from "
            "<font face=\"Courier\">malloc</font> must be checked and later freed.",
            styles,
        ),
        code(
            """
char s[] = "Hello";
printf("%zu\\n", sizeof s);   /* 6: includes '\\0' */
printf("%zu\\n", strlen(s));  /* 5: visible characters */

int *a = malloc(n * sizeof *a);
if (a == NULL) {
    return 1;
}
free(a);
            """,
            styles,
        ),
        p("3. 2D arrays and simulations", styles, "DarkHeading"),
        p(
            "A true 2D array parameter needs the column count in the type. A dynamically "
            "allocated <font face=\"Courier\">int **</font> grid uses one allocation for "
            "the row pointers and one allocation per row. Clean up earlier rows if a later "
            "allocation fails.",
            styles,
        ),
        code(
            """
void print_grid(int rows, int cols, int grid[rows][cols]) {
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            printf("%d ", grid[r][c]);
        }
        printf("\\n");
    }
}
            """,
            styles,
        ),
        p("4. Generic memory with void pointers", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">void *</font> can point at data of any object type, "
            "but it has no element size. Generic algorithms usually receive an element "
            "size and a comparison function. Cast to <font face=\"Courier\">char *</font> "
            "for byte-wise pointer arithmetic.",
            styles,
        ),
        code(
            """
void swap_bytes(void *a, void *b, size_t size) {
    char *pa = a;
    char *pb = b;
    for (size_t i = 0; i < size; i++) {
        char tmp = pa[i];
        pa[i] = pb[i];
        pb[i] = tmp;
    }
}
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "In <font face=\"Courier\">int x = 4; int *p = &#38;x;</font>, identify the stored integer, the address expression, the pointer value, and the dereferenced value.",
                "Write a function that sets a caller-owned integer to 42 through a pointer parameter.",
                "Write a pointer-based integer swap function.",
                "For <font face=\"Courier\">char s[20] = \"Hello\";</font>, compare <font face=\"Courier\">sizeof s</font> and <font face=\"Courier\">strlen(s)</font>.",
                "Write code that allocates <font face=\"Courier\">n</font> integers, checks the allocation, fills them with <font face=\"Courier\">0..n-1</font>, and frees them.",
            ],
            styles,
        ),
        p("Question 6 - explain the stale pointer:", styles),
        code(
            """
int *p = malloc(sizeof *p);
*p = 7;
free(p);
return *p;
            """,
            styles,
        ),
        numbered(["Explain why the final dereference is invalid and name the kind of behaviour C gives."], styles, start=6),
        p("Question 7 - complete manual string duplication:", styles),
        code(
            """
char *duplicate(const char *src) {
    char *copy = malloc(/* size here */);
    if (copy == NULL) {
        return NULL;
    }
    /* copy the string */
    return copy;
}
            """,
            styles,
        ),
        numbered(["Complete the allocation size and copy operation."], styles, start=7),
        numbered(
            [
                "Write the function header for a function that receives a 2D automatic array with <font face=\"Courier\">rows</font> and <font face=\"Courier\">cols</font> known at runtime.",
                "In a Game-of-Life style update, why should you write the next generation into a separate grid instead of changing the current grid in place?",
                "Write the key pointer-arithmetic expression for the address of element <font face=\"Courier\">i</font> in a generic array with base pointer <font face=\"Courier\">base</font> and element size <font face=\"Courier\">size</font>.",
            ],
            styles,
            start=8,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "<font face=\"Courier\">x</font> is the integer object. <font face=\"Courier\">&#38;x</font> is its address. <font face=\"Courier\">p</font> stores that address. <font face=\"Courier\">*p</font> is the integer stored there.",
                "<font face=\"Courier\">void set_to_42(int *p) { *p = 42; }</font>, called with <font face=\"Courier\">set_to_42(&#38;value);</font>",
                "<font face=\"Courier\">void swap(int *a, int *b) { int tmp = *a; *a = *b; *b = tmp; }</font>",
                "<font face=\"Courier\">sizeof s</font> is 20 because it is the whole array. <font face=\"Courier\">strlen(s)</font> is 5 because it stops before the null terminator.",
                "Expected pattern: <font face=\"Courier\">int *a = malloc(n * sizeof *a); if (a == NULL) return 1; for (...) a[i] = i; free(a);</font>",
                "After <font face=\"Courier\">free(p)</font>, the allocation no longer belongs to the program. <font face=\"Courier\">p</font> is stale/dangling, and <font face=\"Courier\">*p</font> is undefined behaviour.",
                "Use <font face=\"Courier\">malloc(strlen(src) + 1)</font>, check for <font face=\"Courier\">NULL</font>, then <font face=\"Courier\">strcpy(copy, src);</font>.",
                "<font face=\"Courier\">void f(int rows, int cols, int grid[rows][cols])</font>",
                "If you update in place, later cells may read already-changed neighbour values. A separate next grid keeps all decisions based on the original generation.",
                "<font face=\"Courier\">(char *)base + i * size</font>. Cast to <font face=\"Courier\">char *</font> because char pointer arithmetic advances one byte at a time.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
