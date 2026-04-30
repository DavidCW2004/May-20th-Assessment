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


OUT = Path(__file__).with_name("cpp-moving-from-c-study-pack.pdf")


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
        title="C++ Moving from C Study Pack",
    )

    story = [
        p("C++ Moving from C", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 Moving to C++ slides, chosen from a red C++ topic not yet covered in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. C++ source, standards, and build flow", styles, "DarkHeading"),
        p(
            "C++ source files commonly use <font face=\"Courier\">.cpp</font> and headers often use <font face=\"Courier\">.hpp</font> or <font face=\"Courier\">.h</font>. The compile and link model is still source to object file to executable, but use the C++ compiler driver.",
            styles,
        ),
        code(
            """
g++ -std=c++17 -c main.cpp -o main.o
g++ -std=c++17 -c stack.cpp -o stack.o
g++ main.o stack.o -o program
            """,
            styles,
        ),
        p(
            "The <font face=\"Courier\">-std=c++17</font> flag selects the C++ standard expected by the course material.",
            styles,
        ),
        p("2. Standard streams", styles, "DarkHeading"),
        p(
            "C++ standard streams are type-aware alternatives to C's <font face=\"Courier\">printf</font> and <font face=\"Courier\">scanf</font>. Include <font face=\"Courier\">&#60;iostream&#62;</font> and use names from the <font face=\"Courier\">std</font> namespace.",
            styles,
        ),
        code(
            """
#include <iostream>

int main() {
    int count = 42;

    std::cout << "Count: " << count << '\\n';
    std::cerr << "Error count: " << count << std::endl;

    return 0;
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">std::cout</font> writes to standard output.",
                "<font face=\"Courier\">std::cerr</font> writes to standard error.",
                "<font face=\"Courier\">std::endl</font> prints a newline and flushes; <font face=\"Courier\">'\\n'</font> only prints a newline.",
                "<font face=\"Courier\">std::cin &#62;&#62; value;</font> reads formatted input into <font face=\"Courier\">value</font>.",
            ],
            styles,
        ),
        p("3. Scope resolution and namespaces", styles, "DarkHeading"),
        p(
            "The standard library lives mostly in namespace <font face=\"Courier\">std</font>. The scope resolution operator <font face=\"Courier\">::</font> selects a name from a namespace or class.",
            styles,
        ),
        code(
            """
std::cout << "Hello" << std::endl;
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">using namespace std;</font> removes the need to write <font face=\"Courier\">std::</font>, but it brings many names into the global scope and can cause name conflicts. Prefer explicit <font face=\"Courier\">std::</font> in revision answers unless the question shows otherwise.",
            styles,
        ),
        p("4. Boolean values", styles, "DarkHeading"),
        p(
            "C++ has a built-in <font face=\"Courier\">bool</font> type. No <font face=\"Courier\">&#60;stdbool.h&#62;</font> is needed.",
            styles,
        ),
        code(
            """
bool flag = false;
bool truthy = true;

std::cout << flag << ' ' << truthy << '\\n';  // 0 1
std::cout << std::boolalpha << flag << '\\n'; // false
            """,
            styles,
        ),
        p(
            "A non-zero numeric value converts to <font face=\"Courier\">true</font>; zero converts to <font face=\"Courier\">false</font>.",
            styles,
        ),
        p("5. <font face=\"Courier\">std::string</font> instead of C strings", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">std::string</font> is a class that manages its own dynamic character storage. It supports assignment, comparison, and concatenation more naturally than fixed C character arrays.",
            styles,
        ),
        code(
            """
#include <string>

std::string s1 = "Hello";
std::string s2 = " world";

s1 = "hello";
if (s1 == s2) {
    std::cout << "same\\n";
}

std::string combined = s1 + s2;
            """,
            styles,
        ),
        p(
            "Unlike a fixed <font face=\"Courier\">char</font> array, a <font face=\"Courier\">std::string</font> can resize as needed and handles its memory automatically.",
            styles,
        ),
        p("6. <font face=\"Courier\">using</font> aliases", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">using</font> creates a clearer type alias in C++. It is often easier to read than <font face=\"Courier\">typedef</font>, especially for long standard-library types.",
            styles,
        ),
        code(
            """
#include <string>
#include <utility>
#include <vector>

using Grade = std::pair<int, std::string>;
using GradeList = std::vector<Grade>;

GradeList grades;
            """,
            styles,
        ),
        p("7. <font face=\"Courier\">auto</font> is still statically typed", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">auto</font> asks the compiler to deduce the type from the initializer. Once deduced, the variable still has one fixed type.",
            styles,
        ),
        code(
            """
auto x = 10;       // int
auto y = 3.14;     // double
auto z = x + y;    // double

x = "hello";       // error: x is still int
            """,
            styles,
        ),
        p(
            "Use <font face=\"Courier\">auto</font> when the type is obvious from context, very long, or less important than the operation being performed.",
            styles,
        ),
        p("8. Function overloading", styles, "DarkHeading"),
        p(
            "C++ can have multiple functions with the same name if their parameter lists differ. The compiler chooses the overload from the argument types at the call site.",
            styles,
        ),
        code(
            """
int myabs(int x) {
    return x < 0 ? -x : x;
}

double myabs(double x) {
    return x < 0.0 ? -x : x;
}

std::cout << myabs(-3) << '\\n';     // int overload
std::cout << myabs(-4.6) << '\\n';   // double overload
            """,
            styles,
        ),
        p(
            "Return type alone is not enough to overload a function. The number or types of parameters must differ.",
            styles,
        ),
        p("9. Default parameters", styles, "DarkHeading"),
        p(
            "A default parameter lets a caller omit an argument. Defaults belong in the declaration that callers see, usually the header.",
            styles,
        ),
        code(
            """
void repeat(std::string text, int times = 1);

repeat("Hi");      // times is 1
repeat("Hi", 3);   // times is 3
            """,
            styles,
        ),
        p(
            "Put default parameters at the end of the parameter list so calls are not ambiguous.",
            styles,
        ),
        p("10. Pass by reference", styles, "DarkHeading"),
        p(
            "A reference parameter gives a function another name for the caller's object. This lets the function modify the caller's value without passing a pointer explicitly.",
            styles,
        ),
        code(
            """
void swap_ints(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

int x = 2;
int y = 5;
swap_ints(x, y);
            """,
            styles,
        ),
        p(
            "Use a const reference for large read-only values, such as <font face=\"Courier\">const std::string &#38;name</font>, to avoid copying while preventing modification.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write the two commands that compile <font face=\"Courier\">main.cpp</font> and <font face=\"Courier\">stack.cpp</font> as C++17 object files, then link them into <font face=\"Courier\">program</font>.",
                "Rewrite <font face=\"Courier\">printf(\"Count: %d\\n\", count);</font> using <font face=\"Courier\">std::cout</font>.",
                "Write a line that reads an integer from standard input into <font face=\"Courier\">count</font> using C++ streams.",
                "Fix a C++ program that uses <font face=\"Courier\">bool flag = false;</font> but includes <font face=\"Courier\">&#60;stdbool.h&#62;</font> instead of the C++ stream/string headers it actually needs.",
                "Replace a fixed C string buffer with <font face=\"Courier\">std::string</font>, then concatenate <font face=\"Courier\">\" world\"</font> safely.",
                "Given <font face=\"Courier\">std::vector&#60;std::pair&#60;int, std::string&#62;&#62;</font>, create a clearer alias using <font face=\"Courier\">using</font>.",
                "For <font face=\"Courier\">auto x = 10;</font>, explain why <font face=\"Courier\">x = \"hello\";</font> fails.",
                "Write two overloads named <font face=\"Courier\">myabs</font>, one for <font face=\"Courier\">int</font> and one for <font face=\"Courier\">double</font>, then show which call uses each.",
                "Add a default parameter so <font face=\"Courier\">repeat(\"Hi\")</font> repeats once but <font face=\"Courier\">repeat(\"Hi\", 3)</font> repeats three times.",
                "Write a C++ reference-based swap function for two integers, then call it on <font face=\"Courier\">x</font> and <font face=\"Courier\">y</font>.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should use C++ language features directly, not C workarounds.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "Expected pattern: <font face=\"Courier\">g++ -std=c++17 -c main.cpp -o main.o</font>, <font face=\"Courier\">g++ -std=c++17 -c stack.cpp -o stack.o</font>, then <font face=\"Courier\">g++ main.o stack.o -o program</font>.",
                "Expected pattern: <font face=\"Courier\">std::cout &#60;&#60; \"Count: \" &#60;&#60; count &#60;&#60; '\\n';</font>.",
                "Expected pattern: <font face=\"Courier\">std::cin &#62;&#62; count;</font>.",
                "C++ has built-in <font face=\"Courier\">bool</font>, so <font face=\"Courier\">&#60;stdbool.h&#62;</font> is not needed. Use headers such as <font face=\"Courier\">&#60;iostream&#62;</font> or <font face=\"Courier\">&#60;string&#62;</font> for streams and strings.",
                "Expected pattern: <font face=\"Courier\">std::string text = \"Hello\"; text = text + \" world\";</font>. The string manages resizing automatically.",
                "Expected pattern: <font face=\"Courier\">using Grade = std::pair&#60;int, std::string&#62;; using GradeList = std::vector&#60;Grade&#62;;</font>.",
                "<font face=\"Courier\">auto</font> deduces <font face=\"Courier\">x</font> as <font face=\"Courier\">int</font>. It does not make the variable dynamically typed, so assigning a string literal later fails.",
                "The overloads must differ by parameter type, for example <font face=\"Courier\">int myabs(int)</font> and <font face=\"Courier\">double myabs(double)</font>. <font face=\"Courier\">myabs(-3)</font> uses the int version; <font face=\"Courier\">myabs(-4.6)</font> uses the double version.",
                "Expected declaration: <font face=\"Courier\">void repeat(std::string text, int times = 1);</font>. Calls that omit <font face=\"Courier\">times</font> use <font face=\"Courier\">1</font>.",
                "Expected pattern: <font face=\"Courier\">void swap_ints(int &#38;a, int &#38;b) { int temp = a; a = b; b = temp; }</font>, then <font face=\"Courier\">swap_ints(x, y);</font>.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
#include <iostream>
#include <string>
#include <utility>
#include <vector>

using Grade = std::pair<int, std::string>;
using GradeList = std::vector<Grade>;

void repeat(std::string text, int times = 1);

void swap_ints(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    std::string text = "Hello";
    text = text + " world";

    int count = 0;
    std::cin >> count;
    std::cout << text << " " << count << '\\n';

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
