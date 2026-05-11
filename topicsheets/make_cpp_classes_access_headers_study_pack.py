from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, Preformatted, SimpleDocTemplate


OUT = Path(__file__).with_name("cpp-classes-access-headers-study-pack.pdf")


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
        title="C++ Classes, Headers, and Object Lifetime Study Pack",
    )

    story = [
        p("C++ Classes, Headers, and Object Lifetime", styles, "TopicTitle"),
        p(
            "Merged sheet based on ECM2433 L12 Classes and L13 Memory, Pointers, and "
            "References. It combines access control, headers, constructors, destructors, "
            "copying, member initializer lists, and g++ compilation.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),
        p("1. Access control and encapsulation", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">private</font> members are only accessible inside the "
            "class. <font face=\"Courier\">protected</font> members are also accessible "
            "inside derived classes. <font face=\"Courier\">public</font> members are "
            "available to outside code. A <font face=\"Courier\">class</font> defaults "
            "to private; a <font face=\"Courier\">struct</font> defaults to public.",
            styles,
        ),
        code(
            """
class Account {
    double balance;
public:
    double get_balance() const { return balance; }
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
};
            """,
            styles,
        ),
        p("2. this and member initializer lists", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">this</font> is a pointer to the current object. "
            "Use it when a parameter shadows a member name. A member initializer list "
            "initializes members and base classes before the constructor body runs.",
            styles,
        ),
        code(
            """
class Box {
    int width;
public:
    Box(int width) : width(width) {}
    int get_width() const { return width; }
};

class TemperatureSensor : public Sensor {
    double celsius;
public:
    TemperatureSensor(int id, const std::string& name, double celsius)
        : Sensor(id, name), celsius(celsius) {}
};
            """,
            styles,
        ),
        p("3. Headers and source files", styles, "DarkHeading"),
        p(
            "A header declares the class. A <font face=\"Courier\">.cpp</font> file "
            "defines member functions using the scope-resolution prefix, such as "
            "<font face=\"Courier\">Counter::increment</font>. Include guards prevent "
            "the same declarations being processed twice.",
            styles,
        ),
        code(
            """
/* counter.h */
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

/* counter.cpp */
#include "counter.h"

Counter::Counter() : count(0) {}
void Counter::increment() { count++; }
int Counter::get_count() const { return count; }
            """,
            styles,
        ),
        p("4. Constructors, copy constructors, and destructors", styles, "DarkHeading"),
        p(
            "A constructor initializes an object. A copy constructor builds a new object "
            "from an existing object. A destructor runs when an object is destroyed. "
            "If a class owns a raw resource, copying and destruction must be designed "
            "carefully; otherwise prefer RAII types such as <font face=\"Courier\">std::string</font> "
            "or smart pointers.",
            styles,
        ),
        code(
            """
class Trace {
public:
    Trace() { std::cout << "ctor\\n"; }
    Trace(const Trace&) { std::cout << "copy\\n"; }
    ~Trace() { std::cout << "dtor\\n"; }
};
            """,
            styles,
        ),
        p("5. Compiling multiple C++ files", styles, "DarkHeading"),
        code(
            """
g++ -std=c++17 -c counter.cpp -o counter.o
g++ -std=c++17 -c main.cpp -o main.o
g++ main.o counter.o -o app
            """,
            styles,
        ),
        p(
            "A pointer to a class member uses the class in the pointer type, for example "
            "<font face=\"Courier\">int Sensor::* field = &#38;Sensor::id;</font>. "
            "For an object <font face=\"Courier\">s</font>, access it with "
            "<font face=\"Courier\">s.*field</font>.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write a guarded <font face=\"Courier\">counter.h</font> declaration for a <font face=\"Courier\">Counter</font> class with private <font face=\"Courier\">int count</font>, a default constructor, <font face=\"Courier\">increment</font>, and <font face=\"Courier\">get_count</font>.",
                "In <font face=\"Courier\">counter.cpp</font>, define <font face=\"Courier\">increment</font>. Make sure you use the required class prefix.",
            ],
            styles,
        ),
        p("Question 3 - access control:", styles),
        code(
            """
class Base {
private:
    int x;
protected:
    int y;
public:
    int z;
};
            """,
            styles,
        ),
        numbered(["Which of <font face=\"Courier\">x</font>, <font face=\"Courier\">y</font>, and <font face=\"Courier\">z</font> can outside code access? Which can a derived class access?"], styles, start=3),
        p("Question 4 - complete the setter:", styles),
        code(
            """
class User {
    int age;
public:
    void set_age(int age) {
        /* reject negative ages, otherwise store the age */
    }
};
            """,
            styles,
        ),
        numbered(["Complete <font face=\"Courier\">set_age</font>. Use <font face=\"Courier\">this</font> if needed."], styles, start=4),
        p("Question 5 - fix the constructor bug:", styles),
        code(
            """
class Box {
    int width;
public:
    Box(int width) {
        width = width;
    }
};
            """,
            styles,
        ),
        numbered(["Explain the bug and fix it using either <font face=\"Courier\">this</font> or an initializer list."], styles, start=5),
        numbered(
            [
                "Write a constructor for <font face=\"Courier\">TemperatureSensor</font> that initializes the base <font face=\"Courier\">Sensor(id, name)</font> and member <font face=\"Courier\">celsius</font>.",
            ],
            styles,
            start=6,
        ),
        p("Question 7 - trace object lifetime:", styles),
        code(
            """
int main() {
    Trace a;
    Trace b = a;
}
            """,
            styles,
        ),
        numbered(["Identify where construction, copy construction, and destruction happen in <font face=\"Courier\">main</font>."], styles, start=7),
        p("Question 8 - copy constructor signature:", styles),
        code(
            """
class Buffer {
public:
    Buffer(const Buffer other) {}
};
            """,
            styles,
        ),
        numbered(["Fix the copy constructor parameter type and explain why it should be a const reference."], styles, start=8),
        numbered(
            [
                "A class only contains <font face=\"Courier\">std::string name;</font>. Is <font face=\"Courier\">~Thing() = default;</font> normally acceptable? Explain.",
                "Write the three <font face=\"Courier\">g++</font> commands to compile <font face=\"Courier\">counter.cpp</font> and <font face=\"Courier\">main.cpp</font> separately, then link them into <font face=\"Courier\">app</font>.",
            ],
            styles,
            start=9,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "Use <font face=\"Courier\">#ifndef COUNTER_H</font>, <font face=\"Courier\">#define COUNTER_H</font>, the class declaration, and <font face=\"Courier\">#endif</font>. Members before <font face=\"Courier\">public:</font> are private.",
                "<font face=\"Courier\">void Counter::increment() { count++; }</font>. The <font face=\"Courier\">Counter::</font> prefix says this is the class member function.",
                "Outside code can access only <font face=\"Courier\">z</font>. A derived class can access <font face=\"Courier\">y</font> and <font face=\"Courier\">z</font>, but not private <font face=\"Courier\">x</font>.",
                "Expected: <font face=\"Courier\">if (age &lt; 0) return; this-&#62;age = age;</font>",
                "<font face=\"Courier\">width = width</font> assigns the parameter to itself. Fix with <font face=\"Courier\">Box(int width) : width(width) {}</font> or <font face=\"Courier\">this-&#62;width = width;</font>.",
                "<font face=\"Courier\">TemperatureSensor(int id, const std::string&#38; name, double celsius) : Sensor(id, name), celsius(celsius) {}</font>",
                "<font face=\"Courier\">Trace a;</font> calls the default constructor. <font face=\"Courier\">Trace b = a;</font> calls the copy constructor. Destructors run for <font face=\"Courier\">b</font> then <font face=\"Courier\">a</font> at the end of main.",
                "Use <font face=\"Courier\">Buffer(const Buffer&#38; other)</font>. Passing by value would require copying before entering the copy constructor, causing recursion and unnecessary copying.",
                "Yes, normally. <font face=\"Courier\">std::string</font> cleans itself up through RAII, so a default destructor is enough unless the class owns some manual resource.",
                "<font face=\"Courier\">g++ -std=c++17 -c counter.cpp -o counter.o</font>; <font face=\"Courier\">g++ -std=c++17 -c main.cpp -o main.o</font>; <font face=\"Courier\">g++ main.o counter.o -o app</font>.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
