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

OUT = Path(__file__).with_name("cpp-classes-access-headers-study-pack.pdf")


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
        bulletType="bullet", leftIndent=6 * mm, bulletFontName="Helvetica", bulletFontSize=7,
    )


def numbered(items, styles, start=1):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=5 * mm) for item in items],
        bulletType="1", leftIndent=7 * mm, bulletFontName="Helvetica-Bold", bulletFontSize=8, start=start,
    )


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm,
        title="C++ Classes: Access Control and Header Files Study Pack",
    )

    story = [
        p("C++ Classes: Access Control and Header Files", styles, "TopicTitle"),
        p(
            "Based on ECM2433 L12 Classes, cppIntro, and L13 Memory slides. "
            "Covers private vs protected access, getters and setters, the this pointer, "
            "splitting classes across .h/.hpp and .cpp files, include guards, and "
            "separate compilation with g++.",
            styles, "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),

        p("1. private, protected, and public", styles, "DarkHeading"),
        p(
            "The key distinction from L12: "
            "<font face=\"Courier\">private</font> members are accessible only within the class itself. "
            "<font face=\"Courier\">protected</font> members are accessible within the class "
            "<b>and</b> within any derived class, but not from outside code. "
            "<font face=\"Courier\">public</font> members are accessible by anyone. "
            "A <font face=\"Courier\">class</font> defaults to private; "
            "a <font face=\"Courier\">struct</font> defaults to public.",
            styles,
        ),
        code(
            """
class Base {
    int i;          /* private: only Base's own functions */
protected:
    int j;          /* protected: Base + derived classes */
public:
    void set(int a, int b) { i = a; j = b; }
    void show() { printf("i=%d, j=%d\\n", i, j); }
};

class Derived : public Base {
    int k;
public:
    Derived(int x) { k = x; j = 0; }  /* j OK: protected */
    void showAll() { show(); }          /* show() OK: public */
    /* i = 5;  would be ERROR: private to Base */
};

int main() {
    Derived d(3);
    d.set(1, 2);   /* OK: public */
    d.show();      /* OK: public */
    /* d.j = 5;   ERROR: protected, not accessible from main */
}
            """,
            styles,
        ),

        p("2. Getters and setters", styles, "DarkHeading"),
        p(
            "When a member is private, external code cannot access it directly. "
            "Provide a public <b>getter</b> to read it and a public <b>setter</b> to write it. "
            "The setter can validate input before applying it.",
            styles,
        ),
        code(
            """
class Temperature {
    double celsius;
public:
    double get_celsius() const { return celsius; }
    void set_celsius(double c) {
        if (c < -273.15) return;   /* reject impossible value */
        celsius = c;
    }
};
            """,
            styles,
        ),

        p("3. The this pointer", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">this</font> is a pointer to the current object. "
            "It is used to disambiguate when a constructor parameter has the same name as "
            "a member variable.",
            styles,
        ),
        code(
            """
class NewClass {
    int a, b;
public:
    NewClass(int a, int b) {
        this->a = a;   /* this->a: member; a: parameter */
        this->b = b;
    }
};
            """,
            styles,
        ),

        p("4. Splitting a class across .h and .cpp", styles, "DarkHeading"),
        p(
            "The header file declares the class (what it has). "
            "The .cpp file defines the member functions (what they do), "
            "using the scope-resolution operator <font face=\"Courier\">::</font> "
            "to name the class they belong to.",
            styles,
        ),
        code(
            """
/* --- counter.h --- */
#ifndef COUNTER_H
#define COUNTER_H

class Counter {
    int count;
public:
    Counter();
    void increment();
    int get_count() const;
};

#endif

/* --- counter.cpp --- */
#include "counter.h"

Counter::Counter() { count = 0; }

void Counter::increment() { count++; }

int Counter::get_count() const { return count; }
            """,
            styles,
        ),

        p("5. Include guards", styles, "DarkHeading"),
        p(
            "If a header is included twice in the same translation unit "
            "(e.g., via two different headers both including the same file), "
            "the contents are processed twice and structures are defined twice — "
            "a compile error. An include guard prevents this.",
            styles,
        ),
        code(
            """
#ifndef STACK_H
#define STACK_H

/* content of stack.h */

#endif
            """,
            styles,
        ),

        p("6. Separate compilation and linking with g++", styles, "DarkHeading"),
        p(
            "Only the essentials are repeated here: compile each "
            "<font face=\"Courier\">.cpp</font> file to a "
            "<font face=\"Courier\">.o</font> object file with "
            "<font face=\"Courier\">g++</font>, then link the object files into the "
            "final executable. The "
            "<font face=\"Courier\">-std=c++17</font> flag selects the language standard.",
            styles,
        ),
        code(
            """
$ g++ -std=c++17 -c counter.cpp -o counter.o
$ g++ -std=c++17 -c main.cpp    -o main.o
$ g++ main.o counter.o -o myprogram
            """,
            styles,
        ),
        p(
            "C++ headers may use the <font face=\"Courier\">.h</font> extension or "
            "<font face=\"Courier\">.hpp</font> (some libraries such as Boost prefer "
            "<font face=\"Courier\">.hpp</font>).",
            styles,
        ),

        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write the <font face=\"Courier\">counter.h</font> class declaration for "
                "a <font face=\"Courier\">Counter</font> with private "
                "<font face=\"Courier\">int count</font> and public "
                "<font face=\"Courier\">Counter()</font>, "
                "<font face=\"Courier\">void increment()</font>, and "
                "<font face=\"Courier\">int get_count() const</font>.",
                "In <font face=\"Courier\">counter.cpp</font>, why must the function "
                "definition be written as "
                "<font face=\"Courier\">void Counter::increment()</font> rather than just "
                "<font face=\"Courier\">void increment()</font>?",
            ],
            styles,
        ),
        p("Question 3 — fix the naming conflict:", styles),
        code(
            """
class Box {
    int width;
public:
    Box(int width) {
        width = width;   /* bug: assigns parameter to itself */
    }
};
            """,
            styles,
        ),
        numbered(
            [
                "Explain the bug and rewrite the constructor body using "
                "<font face=\"Courier\">this</font> to fix it.",
                "Write a getter <font face=\"Courier\">get_age() const</font> and a setter "
                "<font face=\"Courier\">set_age(int)</font> for a private "
                "<font face=\"Courier\">int age</font> member. The setter must reject "
                "negative values.",
                "Write the complete include guard for a header file called "
                "<font face=\"Courier\">sensor.h</font>.",
            ],
            styles, start=3,
        ),
        p("Question 6 — this program does not compile:", styles),
        code(
            """
/* grandparent.h */
struct Data { int x; };

/* parent.h */
#include "grandparent.h"

/* child.cpp */
#include "parent.h"
#include "grandparent.h"   /* included again */
int main() { return 0; }
            """,
            styles,
        ),
        numbered(
            [
                "Explain the compile error and show what to add to "
                "<font face=\"Courier\">grandparent.h</font> to fix it.",
                "Given a class <font face=\"Courier\">Counter</font> declared in "
                "<font face=\"Courier\">counter.h</font> with a private "
                "<font face=\"Courier\">int count</font> and public "
                "<font face=\"Courier\">Counter()</font>, "
                "<font face=\"Courier\">void increment()</font>, and "
                "<font face=\"Courier\">int get_count() const</font>, "
                "write the <font face=\"Courier\">counter.cpp</font> file that implements "
                "all three using the <font face=\"Courier\">::</font> operator.",
                "State the three g++ commands needed to compile "
                "<font face=\"Courier\">counter.cpp</font> and "
                "<font face=\"Courier\">main.cpp</font> (both including counter.h) "
                "into an executable called <font face=\"Courier\">myprogram</font>, "
                "using the C++17 standard.",
            ],
            styles, start=6,
        ),
        p("Question 9 — the destructor is missing:", styles),
        code(
            """
class Buffer {
    char *data;
public:
    Buffer(int size) { data = new char[size]; }
    /* destructor missing */
};
            """,
            styles,
        ),
        numbered(
            [
                "Write the correct destructor for <font face=\"Courier\">Buffer</font>. "
                "Explain what happens if it is omitted.",
                "What is the key difference between C's "
                "<font face=\"Courier\">malloc</font> and C++'s "
                "<font face=\"Courier\">new</font> when allocating an object of a class? "
                "What about <font face=\"Courier\">free</font> vs "
                "<font face=\"Courier\">delete</font>?",
            ],
            styles, start=9,
        ),

        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "Expected header shape: "
                "<font face=\"Courier\">#ifndef COUNTER_H</font> / "
                "<font face=\"Courier\">#define COUNTER_H</font> / "
                "<font face=\"Courier\">class Counter { int count; public: "
                "Counter(); void increment(); int get_count() const; };</font> / "
                "<font face=\"Courier\">#endif</font>.",

                "<font face=\"Courier\">Counter::increment</font> says the function is "
                "the member function declared inside <font face=\"Courier\">Counter</font>. "
                "Without the scope-resolution prefix, the compiler sees a separate free "
                "function named <font face=\"Courier\">increment</font>.",

                "The bug: <font face=\"Courier\">width = width</font> assigns the parameter "
                "to itself; the member is never set. "
                "Fix: <font face=\"Courier\">this-&#62;width = width;</font>",

                "<font face=\"Courier\">int get_age() const { return age; }</font> and "
                "<font face=\"Courier\">void set_age(int a) { if (a &gt;= 0) age = a; }</font>",

                "<font face=\"Courier\">#ifndef SENSOR_H</font> / "
                "<font face=\"Courier\">#define SENSOR_H</font> / "
                "... header content ... / "
                "<font face=\"Courier\">#endif</font>",

                "The error is a redefinition of <font face=\"Courier\">struct Data</font> "
                "because grandparent.h is processed twice. "
                "Fix: add an include guard to grandparent.h: "
                "<font face=\"Courier\">#ifndef GRANDPARENT_H</font> / "
                "<font face=\"Courier\">#define GRANDPARENT_H</font> / content / "
                "<font face=\"Courier\">#endif</font>",

                "counter.cpp: <font face=\"Courier\">#include \"counter.h\"</font>. "
                "Then: "
                "<font face=\"Courier\">Counter::Counter() { count = 0; }</font> / "
                "<font face=\"Courier\">void Counter::increment() { count++; }</font> / "
                "<font face=\"Courier\">int Counter::get_count() const { return count; }</font>",

                "<font face=\"Courier\">g++ -std=c++17 -c counter.cpp -o counter.o</font> then "
                "<font face=\"Courier\">g++ -std=c++17 -c main.cpp -o main.o</font> then "
                "<font face=\"Courier\">g++ main.o counter.o -o myprogram</font>. "
                "Use g++ rather than gcc so the C++ standard library is linked correctly.",

                "<font face=\"Courier\">~Buffer() { delete[] data; }</font>. "
                "Without it, the heap memory allocated in the constructor is never freed "
                "(memory leak) every time a Buffer goes out of scope.",

                "malloc allocates raw memory without calling any constructor. "
                "new allocates memory then calls the constructor. "
                "free releases memory without calling the destructor. "
                "delete calls the destructor then deallocates memory.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
