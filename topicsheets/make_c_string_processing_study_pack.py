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


OUT = Path(__file__).with_name("c-string-processing-study-pack.pdf")


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
        title="C String Processing Study Pack",
    )

    story = [
        p("C String Processing", styles, "TopicTitle"),
        p(
            "Grounded in ECM2433 arrays, strings, and worksheet material. Focuses on "
            "null terminators, string storage, standard library functions, bounded "
            "copying, character classification, in-place editing, and common trace/fix tasks.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),

        p("1. C strings are null-terminated char arrays", styles, "DarkHeading"),
        p(
            "A C string is a sequence of characters stored in an array and ended by "
            "<font face=\"Courier\">'\\0'</font>. That terminator is how "
            "<font face=\"Courier\">printf</font>, <font face=\"Courier\">strlen</font>, "
            "and the string library know where the text stops. If the terminator is missing, "
            "string code can keep reading beyond the intended array.",
            styles,
        ),
        code(
            r"""
char s[] = "Hello";
/* stored as: H e l l o \0 */

printf("%s\n", s);     /* Hello */
s[2] = '\0';
printf("%s\n", s);     /* He */
            """,
            styles,
        ),

        p("2. sizeof and strlen answer different questions", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">sizeof</font> measures storage in bytes. "
            "<font face=\"Courier\">strlen</font> counts characters before the first "
            "<font face=\"Courier\">'\\0'</font>. Changing the contents of an array can "
            "change <font face=\"Courier\">strlen</font>, but not the array's "
            "<font face=\"Courier\">sizeof</font>.",
            styles,
        ),
        code(
            r"""
char text[20] = "Hello world";

sizeof(text)    /* 20: total array storage */
strlen(text)    /* 11: characters before \0 */

text[0] = '\0';
sizeof(text)    /* still 20 */
strlen(text)    /* now 0 */
            """,
            styles,
        ),

        p("3. Printing strings with width and precision", styles, "DarkHeading"),
        p(
            "For <font face=\"Courier\">printf</font> string formatting, width sets the "
            "minimum field width. Precision limits the maximum number of characters printed. "
            "A minus sign left-aligns the output.",
            styles,
        ),
        code(
            r"""
char name[] = "Elephants";

printf("*%s*\n",      name);   /* *Elephants* */
printf("*%20s*\n",    name);   /* right-aligned in width 20 */
printf("*%-20s*\n",   name);   /* left-aligned in width 20 */
printf("*%-20.3s*\n", name);   /* prints only Ele, then pads */
            """,
            styles,
        ),

        p("4. Standard library string functions", styles, "DarkHeading"),
        p(
            "Include <font face=\"Courier\">&#60;string.h&#62;</font> for the standard "
            "string functions. They all expect valid null-terminated strings.",
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">strlen(s)</font>: counts characters before "
                "<font face=\"Courier\">'\\0'</font>.",
                "<font face=\"Courier\">strcmp(a, b)</font>: returns 0 when the two "
                "strings have the same contents.",
                "<font face=\"Courier\">strcpy(dest, src)</font>: copies src into dest, "
                "but does not know the size of dest.",
                "<font face=\"Courier\">strncpy(dest, src, n)</font>: copies up to n "
                "characters, but may not add a null terminator if src is too long.",
                "<font face=\"Courier\">snprintf(buf, size, fmt, ...)</font>: writes "
                "formatted text into a bounded buffer.",
            ],
            styles,
        ),
        code(
            r"""
char dest[8];
strncpy(dest, src, sizeof dest - 1);
dest[sizeof dest - 1] = '\0';
            """,
            styles,
        ),

        p("5. Character classification and conversion", styles, "DarkHeading"),
        p(
            "Include <font face=\"Courier\">&#60;ctype.h&#62;</font> for functions such as "
            "<font face=\"Courier\">isalpha</font>, <font face=\"Courier\">isdigit</font>, "
            "<font face=\"Courier\">ispunct</font>, and <font face=\"Courier\">tolower</font>. "
            "These are useful when normalising text before comparing or searching it.",
            styles,
        ),
        code(
            r"""
for (int i = 0; s[i] != '\0'; i++) {
    if (isalpha((unsigned char)s[i]))
        s[i] = tolower((unsigned char)s[i]);
}
            """,
            styles,
        ),

        p("6. In-place string editing", styles, "DarkHeading"),
        p(
            "A common pattern is to read from one index and write to another. The read index "
            "visits every original character. The write index only advances when a character "
            "is kept. At the end, add a new null terminator.",
            styles,
        ),
        code(
            r"""
void remove_spaces(char s[]) {
    int write = 0;
    for (int read = 0; s[read] != '\0'; read++) {
        if (s[read] != ' ')
            s[write++] = s[read];
    }
    s[write] = '\0';
}
            """,
            styles,
        ),

        p("7. Palindrome checks use mirrored indexes", styles, "DarkHeading"),
        p(
            "To compare the first character with the last, use "
            "<font face=\"Courier\">s[len - 1 - i]</font>. The minus 1 matters because "
            "<font face=\"Courier\">s[len]</font> is the null terminator, not the final "
            "visible character.",
            styles,
        ),
        code(
            r"""
bool is_palindrome(char s[]) {
    int len = strlen(s);
    for (int i = 0; i < len / 2; i++) {
        if (s[i] != s[len - 1 - i])
            return false;
    }
    return true;
}
            """,
            styles,
        ),

        p("Practice Questions", styles, "BlueHeading"),
        p("Questions 1 and 2 use this declaration:", styles),
        code(
            r"""
char s[20] = "Hello world";
            """,
            styles,
        ),
        numbered(
            [
                "Calculate <font face=\"Courier\">sizeof(s)</font> and "
                "<font face=\"Courier\">strlen(s)</font>.",
                "After <font face=\"Courier\">s[0] = '\\0';</font>, calculate "
                "<font face=\"Courier\">sizeof(s)</font> and "
                "<font face=\"Courier\">strlen(s)</font> again.",
            ],
            styles,
        ),

        p("Question 3 uses this code:", styles),
        code(
            r"""
char name[] = "Elephants";
printf("*%-20.3s*\n", name);
            """,
            styles,
        ),
        numbered(
            [
                "Write the exact output, including the asterisks and spaces.",
            ],
            styles,
            start=3,
        ),

        p("Question 4 uses this code:", styles),
        code(
            r"""
char text[] = "abc123!";
int letters = 0, digits = 0, other = 0;

for (int i = 0; text[i] != '\0'; i++) {
    if (isalpha((unsigned char)text[i]))
        letters++;
    else if (isdigit((unsigned char)text[i]))
        digits++;
    else
        other++;
}

printf("%d %d %d\n", letters, digits, other);
            """,
            styles,
        ),
        numbered(
            [
                "Trace the loop and write what the program prints.",
            ],
            styles,
            start=4,
        ),

        p("Question 5: complete the function body.", styles),
        code(
            r"""
void strip_digits(const char *src, char *dst) {
    int write = 0;
    for (int read = 0; src[read] != '\0'; read++) {
        /* complete this */
    }
    /* complete this */
}
            """,
            styles,
        ),
        numbered(
            [
                "Complete the function so it copies src to dst while skipping digit characters.",
            ],
            styles,
            start=5,
        ),

        p("Question 6: complete the missing expression.", styles),
        code(
            r"""
bool is_palindrome(char s[]) {
    int len = strlen(s);
    for (int i = 0; i < len / 2; i++) {
        if (s[i] != s[________])
            return false;
    }
    return true;
}
            """,
            styles,
        ),
        numbered(
            [
                "Fill the blank with the mirrored index expression.",
            ],
            styles,
            start=6,
        ),

        p("Question 7: complete the function body.", styles),
        code(
            r"""
void normalise(char s[]) {
    int write = 0;
    for (int read = 0; s[read] != '\0'; read++) {
        /* keep letters/digits, remove punctuation/spaces, lowercase kept chars */
    }
    /* finish the string */
}
            """,
            styles,
        ),
        numbered(
            [
                "Complete the function and state the header needed for the character functions.",
            ],
            styles,
            start=7,
        ),

        p("Question 8 uses this code:", styles),
        code(
            r"""
char word[] = "racecar";
if (is_palindrome(word)) {
    printf("yes\n");
} else {
    printf("no\n");
}
            """,
            styles,
        ),
        numbered(
            [
                "Trace the condition and write what is printed.",
            ],
            styles,
            start=8,
        ),

        p("Question 9: complete the function.", styles),
        code(
            r"""
size_t mystrlen(const char *s) {
    size_t n = 0;
    /* complete this */
    return n;
}
            """,
            styles,
        ),
        numbered(
            [
                "Complete <font face=\"Courier\">mystrlen</font> without using any string library function.",
            ],
            styles,
            start=9,
        ),

        p("Question 10: complete the bounded copy.", styles),
        code(
            r"""
void string_copy(char *dest, size_t len, const char *src) {
    size_t i = 0;
    /* copy at most len - 1 characters */
    /* always add a null terminator */
}
            """,
            styles,
        ),
        numbered(
            [
                "Complete the function so it works for a destination buffer of size len.",
            ],
            styles,
            start=10,
        ),

        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Attempt the questions before checking. Equivalent code is fine if it has the "
            "same behaviour and still null-terminates strings correctly.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "<font face=\"Courier\">sizeof(s)</font> is 20. "
                "<font face=\"Courier\">strlen(s)</font> is 11.",
                "<font face=\"Courier\">sizeof(s)</font> is still 20. "
                "<font face=\"Courier\">strlen(s)</font> is 0 because the first character "
                "is now the null terminator.",
                "It prints an opening asterisk, <font face=\"Courier\">Ele</font>, "
                "17 spaces, then a closing asterisk. The precision prints 3 characters, "
                "then the width pads to 20 characters.",
                "It prints <font face=\"Courier\">3 3 1</font>: three letters, three digits, "
                "and one other character.",
                "Inside the loop, copy only non-digits: "
                "<font face=\"Courier\">if (!isdigit((unsigned char)src[read])) "
                "dst[write++] = src[read];</font>. After the loop, write "
                "<font face=\"Courier\">dst[write] = '\\0';</font>.",
                "Use <font face=\"Courier\">len - 1 - i</font>. "
                "The last visible character is at index len - 1.",
                "Include <font face=\"Courier\">&#60;ctype.h&#62;</font>. Keep only characters "
                "where <font face=\"Courier\">isalnum((unsigned char)s[read])</font> is true, "
                "store <font face=\"Courier\">tolower((unsigned char)s[read])</font>, and "
                "finish with <font face=\"Courier\">s[write] = '\\0';</font>.",
                "It prints <font face=\"Courier\">yes</font> because racecar reads the same "
                "forwards and backwards.",
                "Loop while <font face=\"Courier\">s[n] != '\\0'</font>, incrementing n. "
                "Return n.",
                "Loop while <font face=\"Courier\">i + 1 &#60; len</font> and "
                "<font face=\"Courier\">src[i] != '\\0'</font>, copying src[i] into dest[i]. "
                "Then set <font face=\"Courier\">dest[i] = '\\0';</font>.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            r"""
#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

size_t mystrlen(const char *s) {
    size_t n = 0;
    while (s[n] != '\0')
        n++;
    return n;
}

void string_copy(char *dest, size_t len, const char *src) {
    size_t i = 0;
    if (len == 0)
        return;
    while (i + 1 < len && src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}

void normalise(char s[]) {
    int write = 0;
    for (int read = 0; s[read] != '\0'; read++) {
        unsigned char ch = (unsigned char)s[read];
        if (isalnum(ch))
            s[write++] = (char)tolower(ch);
    }
    s[write] = '\0';
}

bool is_palindrome(char s[]) {
    int len = strlen(s);
    for (int i = 0; i < len / 2; i++) {
        if (s[i] != s[len - 1 - i])
            return false;
    }
    return true;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
