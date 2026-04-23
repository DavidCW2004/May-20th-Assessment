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


OUT = Path(__file__).with_name("c-preprocessor-macros-headers-study-pack.pdf")


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
            fontSize=7.3,
            leading=9.0,
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
        title="C Preprocessor, Macros, and Headers Study Pack",
    )

    story = [
        p("C Preprocessor, Macros, and Headers", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 preprocessor and program structure material: "
            "L09 C preprocessor and L10 program structure, aligned to red items in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. What the preprocessor does", styles, "DarkHeading"),
        p(
            "Each C source file is preprocessed before compilation. The preprocessor handles directives such as "
            "`#include`, `#define`, `#ifdef`, and `#ifndef`. Its job is textual rewriting: it expands macros and "
            "copies included header contents into the source before the compiler sees the result.",
            styles,
        ),
        code(
            """
#include "myheader.h"
#define MAGIC 42

int main(void) {
    float k = MAGIC * PI;
}
            """,
            styles,
        ),
        p(
            "After preprocessing, `MAGIC` and anything from `myheader.h` have been substituted into the rewritten source.",
            styles,
        ),
        p("2. Simple macros with `#define`", styles, "DarkHeading"),
        p(
            "`#define` can create symbolic constants and function-like macros. Macro expansion is direct text substitution, "
            "so the compiler never sees the macro name itself.",
            styles,
        ),
        code(
            """
#define TRUE 1
#define PI 3.1415926
#define ELEPHANT "Size of an elephant!"
            """,
            styles,
        ),
        p(
            "Macro names are replaced in code, but not inside quoted strings. That is why `printf(ELEPHANT);` expands, "
            "while `printf(\"ELEPHANT\");` stays unchanged.",
            styles,
        ),
        p("3. Macro pitfalls: precedence and repeated evaluation", styles, "DarkHeading"),
        p(
            "Function-like macros are risky because text substitution ignores type checking and can interact badly with "
            "operator precedence and side effects.",
            styles,
        ),
        code(
            """
#define MAX(a,b) a > b ? a : b

int j = MAX(3,2) + 5;
/* expands to: 3 > 2 ? 3 : 2 + 5 */
            """,
            styles,
        ),
        p(
            "The standard first fix is full parenthesising:",
            styles,
        ),
        code(
            """
#define MAX(a,b) ((a) > (b) ? (a) : (b))
            """,
            styles,
        ),
        p(
            "But even fully parenthesised macros can still evaluate arguments more than once. "
            "`MAX(i++, j++)` is a classic bad example. When side effects matter, use a proper function instead.",
            styles,
        ),
        p("4. Macro vs function", styles, "DarkHeading"),
        bullets(
            [
                "Macros are expanded before compilation and do not obey normal function-call rules.",
                "Functions are type-checked and usually easier to debug.",
                "Macros can surprise you through precedence or repeated evaluation.",
                "Use macros carefully for constants, conditional compilation, or specific metaprogramming tasks.",
            ],
            styles,
        ),
        p("5. Stringification and conditional compilation", styles, "DarkHeading"),
        p(
            "Stringification uses `#ARG` inside a macro definition to turn the argument text into a string literal. "
            "This is useful for debugging output.",
            styles,
        ),
        code(
            """
#define REPORT_FLOAT(X) fprintf(stderr, "%s is %f\\n", #X, X)
            """,
            styles,
        ),
        p(
            "Conditional compilation uses directives such as `#ifdef`, `#ifndef`, `#else`, `#elif`, and `#endif` "
            "to include or exclude code depending on whether a symbol is defined.",
            styles,
        ),
        p("6. Headers, include guards, `static`, and `extern`", styles, "DarkHeading"),
        p(
            "Headers usually contain declarations, typedefs, structs, and function prototypes. "
            "Source files contain the function definitions. If the same header can be included more than once, "
            "it needs an include guard to prevent duplicate definitions.",
            styles,
        ),
        code(
            """
#ifndef __STACK_H
#define __STACK_H

typedef struct node *STACK;
extern STACK push(STACK, char);
extern char pop(STACK *);

#endif
            """,
            styles,
        ),
        bullets(
            [
                "`static` on a function in a `.c` file makes it private to that source file.",
                "`extern` declares a function or object that is accessible from other translation units.",
                "Include guards stop the same header contents being processed multiple times in one compilation unit.",
            ],
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Explain what the C preprocessor does before compilation.",
                "State what `#include` does in practical terms.",
                "Write one example of a simple object-like macro and say how it is expanded.",
                "Explain why `#define MAX(a,b) a > b ? a : b` is dangerous, using `MAX(3,2) + 5` as the example.",
                "Write a safer fully parenthesised version of `MAX(a,b)`.",
                "Explain why `MAX(i++, j++)` can still be a problem even with parentheses.",
                "Explain the difference between using a macro and using a function for the same calculation.",
                "What does stringification mean in a macro? Give a short example.",
                "Write the basic pattern of an include guard and explain why it is needed.",
                "Explain the difference between `static` and `extern` for functions in separate source files.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should use the language of substitution, scope, declarations, and translation units.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "The preprocessor rewrites the source before compilation. It handles directives such as `#include`, `#define`, and conditional compilation by performing textual substitution and inclusion.",
                "`#include` finds the named header and copies its contents into the current source file at that point before compilation.",
                "Any valid example such as `#define PI 3.1415926`. Full credit requires saying the name is replaced textually wherever it is used in code.",
                "Because direct substitution changes precedence. `MAX(3,2) + 5` expands to `3 > 2 ? 3 : 2 + 5`, so the result is not the intended fully grouped maximum-plus-five expression.",
                "Expected: `#define MAX(a,b) ((a) > (b) ? (a) : (b))`.",
                "Because macro arguments may be evaluated more than once. With `i++` or `j++`, the increments can happen multiple times, creating surprising results.",
                "A function is type-checked and evaluates its arguments once. A macro is raw textual substitution, so it is more prone to precedence and side-effect problems.",
                "Stringification means turning the macro argument text into a string literal with `#ARG`. Example: `#define REPORT(X) printf(\"%s\\n\", #X)`.",
                "Expected pattern: `#ifndef NAME`, `#define NAME`, header contents, `#endif`. It prevents multiple inclusion causing redefinitions.",
                "`static` makes a function private to the current source file. `extern` is used for functions or objects intended to be visible across source files.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
#define MAX(a,b) ((a) > (b) ? (a) : (b))
#define REPORT_FLOAT(X) fprintf(stderr, "%s is %f\\n", #X, X)

#ifndef __MY_HEADER_H
#define __MY_HEADER_H

extern int api_function(int x);

#endif

static int helper(int x) {
    return x + 1;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
