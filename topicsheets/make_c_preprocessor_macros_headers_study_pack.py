from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, Preformatted, SimpleDocTemplate


OUT = Path(__file__).with_name("c-preprocessor-macros-headers-study-pack.pdf")


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
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm, title="C Preprocessor, Macros, and Headers Study Pack")
    story = [
        p("C Preprocessor, Macros, and Headers", styles, "TopicTitle"),
        p("Based on ECM2433 preprocessor and program-structure material: includes, macros, guards, extern, static, and separate compilation.", styles, "SourceText"),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. The preprocessor rewrites source before compilation", styles, "DarkHeading"),
        p("It handles directives such as #include, #define, #ifdef, and #ifndef before the compiler proper sees the translation unit.", styles),
        code("""
#include "stack.h"
#define MAGIC 42
        """, styles),
        p("2. Macro expansion is textual substitution", styles, "DarkHeading"),
        code("""
#define PI 3.1415926
#define ELEPHANT "Size of an elephant!"

printf(ELEPHANT);   /* macro expands */
printf("ELEPHANT"); /* quoted text does not */
        """, styles),
        p("3. Function-like macros need care", styles, "DarkHeading"),
        p("Macro arguments are substituted as text. Parenthesise parameters and the whole result, and avoid side effects in macro arguments.", styles),
        code("""
#define BAD_MAX(a,b) a > b ? a : b
#define MAX(a,b) ((a) > (b) ? (a) : (b))
        """, styles),
        p("4. Stringification and conditional compilation", styles, "DarkHeading"),
        code("""
#define REPORT_FLOAT(X) fprintf(stderr, "%s is %f\\n", #X, X)

#ifdef DEBUG
    REPORT_FLOAT(value);
#endif
        """, styles),
        p("5. Headers, include guards, static, and extern", styles, "DarkHeading"),
        p("Headers normally contain declarations and type definitions. Source files contain definitions. Include guards prevent duplicate processing of the same header contents.", styles),
        code("""
#ifndef STACK_H
#define STACK_H

typedef struct node *STACK;
extern STACK push(STACK stack, char value);
extern char pop(STACK *stack);

#endif
        """, styles),
        bullets([
            "static on a file-scope helper function limits visibility to that source file.",
            "extern declares an object or function defined elsewhere.",
            "Include guards should avoid reserved identifiers such as names beginning with double underscores.",
        ], styles),
        p("Practice Questions", styles, "BlueHeading"),
        numbered([
            "Explain what the C preprocessor does before compilation.",
            "State what <font face=\"Courier\">#include \"stack.h\"</font> does in practical terms.",
            "Write one object-like macro and say how it expands.",
            "Explain why <font face=\"Courier\">#define MAX(a,b) a &gt; b ? a : b</font> is dangerous with <font face=\"Courier\">MAX(3,2) + 5</font>.",
            "Write a safer fully parenthesised version of <font face=\"Courier\">MAX(a,b)</font>.",
            "Explain why <font face=\"Courier\">MAX(i++, j++)</font> can still be a problem.",
            "Compare a macro with a function for the same calculation.",
            "Explain stringification and give a short macro example.",
            "Write the basic pattern of an include guard for <font face=\"Courier\">stack.h</font>.",
            "Explain the difference between <font face=\"Courier\">static</font> and <font face=\"Courier\">extern</font> in separate source files.",
        ], styles),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions.", styles, "SourceText"),
        numbered([
            "It rewrites the source before compilation, handling include files, macro substitution, and conditional compilation.",
            "It copies the contents of the named header into the source file at that point before compilation.",
            "Example: <font face=\"Courier\">#define LIMIT 100</font>. The name is replaced textually in code.",
            "Direct substitution changes grouping. The expansion behaves like <font face=\"Courier\">3 &gt; 2 ? 3 : 2 + 5</font>, not like a grouped maximum plus five.",
            "Expected: <font face=\"Courier\">#define MAX(a,b) ((a) &gt; (b) ? (a) : (b))</font>.",
            "The chosen argument may be evaluated more than once, so increments or other side effects can happen more than once.",
            "A function is type-checked and evaluates each argument once. A macro is text substitution and is easier to misuse.",
            "Stringification uses <font face=\"Courier\">#</font> in a macro body to turn the argument text into a string, such as <font face=\"Courier\">#define REPORT(X) printf(\"%s\", #X)</font>.",
            "Expected: <font face=\"Courier\">#ifndef STACK_H</font>, <font face=\"Courier\">#define STACK_H</font>, header contents, then <font face=\"Courier\">#endif</font>.",
            "<font face=\"Courier\">static</font> limits a file-scope definition to the current source file. <font face=\"Courier\">extern</font> declares something defined elsewhere.",
        ], styles),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
