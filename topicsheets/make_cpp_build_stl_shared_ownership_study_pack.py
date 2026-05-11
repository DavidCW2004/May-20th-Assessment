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


OUT = Path(__file__).with_name("cpp-build-stl-shared-ownership-study-pack.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TopicTitle", parent=styles["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#111827"), spaceAfter=8))
    styles.add(ParagraphStyle("TopicBody", parent=styles["Normal"], fontSize=9.0, leading=11.4, textColor=colors.HexColor("#111827"), spaceAfter=5))
    styles.add(ParagraphStyle("SourceText", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#4b5563"), spaceAfter=6))
    styles.add(ParagraphStyle("BlueHeading", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#1d4ed8"), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle("DarkHeading", parent=styles["Heading3"], fontSize=11, leading=13, textColor=colors.HexColor("#111827"), spaceBefore=6, spaceAfter=3))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.0, leading=8.4, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=6))
    return styles


def p(text, styles, style="TopicBody"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=92)


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
        title="C++ Build Systems, STL Algorithms, and Shared Ownership Study Pack",
    )

    story = [
        p("C++ Build Systems, STL Algorithms, and Shared Ownership", styles, "TopicTitle"),
        p(
            "Grounded in ECM2433 cppIntro, L10, L13, and L16: C++ compile/link flow, CMake as a large-project build tool, STL algorithms/function objects, and shared/weak smart pointers.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),
        p("1. C++ compile and link flow", styles, "DarkHeading"),
        p(
            "C++ uses the same broad compile/link model as C, but use the C++ compiler driver. Source files such as <font face=\"Courier\">main.cpp</font> and <font face=\"Courier\">sensor.cpp</font> compile to object files. The object files are then linked into an executable.",
            styles,
        ),
        code(
            """
g++ -std=c++17 -c main.cpp -o main.o
g++ -std=c++17 -c sensor.cpp -o sensor.o
g++ main.o sensor.o -o program
            """,
            styles,
        ),
        p(
            "The output executable is usually named without <font face=\"Courier\">.o</font>. The <font face=\"Courier\">.o</font> extension means object file, not finished program.",
            styles,
        ),
        p("2. CMake at a high level", styles, "DarkHeading"),
        p(
            "Lecture L10 mentions <font face=\"Courier\">cmake</font> as the large-project build tool for C++. CMake does not replace the compiler. It generates build files for tools such as Make or Ninja, then those tools run the compile and link commands.",
            styles,
        ),
        code(
            """
cmake -S . -B build
cmake --build build
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">-S .</font> says where the source project is.",
                "<font face=\"Courier\">-B build</font> says where generated build files and compiled output go.",
                "CMake is useful when a project has many files, libraries, include directories, and platform-specific build settings.",
            ],
            styles,
        ),
        p("3. STL algorithms and iterators", styles, "DarkHeading"),
        p(
            "STL algorithms work with iterator ranges. A common pattern is <font face=\"Courier\">container.begin()</font> and <font face=\"Courier\">container.end()</font>. <font face=\"Courier\">end()</font> is one past the last element.",
            styles,
        ),
        code(
            """
#include <algorithm>
#include <vector>

std::vector<int> values = {4, 1, 7, 1};

std::sort(values.begin(), values.end());
bool has_four = std::binary_search(values.begin(), values.end(), 4);
int ones = std::count(values.begin(), values.end(), 1);
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">sort</font> reorders the range.",
                "<font face=\"Courier\">binary_search</font> assumes the range is already sorted according to the same ordering.",
                "<font face=\"Courier\">count</font> returns how many elements compare equal to a value.",
            ],
            styles,
        ),
        p("4. Function objects and lambdas", styles, "DarkHeading"),
        p(
            "Algorithms can be customised by passing a comparator or predicate. That callable can be a function, a function object, or a lambda.",
            styles,
        ),
        code(
            """
std::sort(values.begin(), values.end(),
          [](int a, int b) {
              return a > b;   // descending
          });

int big = std::count_if(values.begin(), values.end(),
                        [](int value) {
                            return value > 10;
                        });
            """,
            styles,
        ),
        p(
            "A sort comparator should return true when the first argument should come before the second. A count/filter predicate returns true for values that should be counted or kept.",
            styles,
        ),
        p("5. shared_ptr and weak_ptr", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">std::unique_ptr&#60;T&#62;</font> has one owner and cannot be copied. <font face=\"Courier\">std::shared_ptr&#60;T&#62;</font> is for shared ownership: copies increase a reference count, and the object is destroyed when the last shared owner goes away.",
            styles,
        ),
        code(
            """
#include <memory>

auto p = std::make_shared<int>(42);
auto q = p;                 // both share ownership

std::cout << p.use_count(); // usually 2 here
            """,
            styles,
        ),
        p(
            "<font face=\"Courier\">std::weak_ptr&#60;T&#62;</font> observes an object owned by shared pointers without increasing the strong ownership count. To use the object, call <font face=\"Courier\">lock()</font>. If the object is already gone, <font face=\"Courier\">lock()</font> returns an empty shared pointer.",
            styles,
        ),
        code(
            """
std::weak_ptr<int> weak = p;

if (auto alive = weak.lock()) {
    std::cout << *alive << std::endl;
}
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        p("Question 1 - finish the C++ build:", styles),
        code(
            """
g++ -std=c++17 -c main.cpp -o main.o
g++ -std=c++17 -c sensor.cpp -o sensor.o
/* link command here */
            """,
            styles,
        ),
        numbered(["Write the command that creates an executable called <font face=\"Courier\">program</font>."], styles),
        p("Question 2 - explain the output file names:", styles),
        code(
            """
g++ main.o sensor.o -o program
            """,
            styles,
        ),
        numbered(["Why is the output called <font face=\"Courier\">program</font> rather than <font face=\"Courier\">program.o</font>?"], styles, start=2),
        p("Question 3 - CMake role:", styles),
        code(
            """
cmake -S . -B build
cmake --build build
            """,
            styles,
        ),
        numbered(["Explain what CMake is doing at a high level and whether it replaces <font face=\"Courier\">g++</font>."], styles, start=3),
        p("Question 4 - binary search bug:", styles),
        code(
            """
std::vector<int> values = {8, 2, 5, 1};
bool found = std::binary_search(values.begin(), values.end(), 5);
            """,
            styles,
        ),
        numbered(["Explain the bug and fix the code."], styles, start=4),
        p("Question 5 - complete descending sort:", styles),
        code(
            """
std::vector<int> scores = {4, 10, 7};
std::sort(scores.begin(), scores.end(),
          /* comparator here */);
            """,
            styles,
        ),
        numbered(["Complete the comparator so the largest score comes first."], styles, start=5),
        p("Question 6 - choose the algorithm:", styles),
        code(
            """
std::vector<int> xs = {1, 4, 4, 8};
/* count how many values are 4 */
            """,
            styles,
        ),
        numbered(["Write the STL algorithm call that gives the count."], styles, start=6),
        p("Question 7 - complete count_if:", styles),
        code(
            """
std::vector<int> xs = {3, 12, 5, 20};
int n = std::count_if(xs.begin(), xs.end(),
                      /* predicate here */);
            """,
            styles,
        ),
        numbered(["Complete the predicate so <font face=\"Courier\">n</font> counts values greater than 10."], styles, start=7),
        p("Question 8 - shared ownership trace:", styles),
        code(
            """
auto a = std::make_shared<int>(5);
auto b = a;
auto c = b;
            """,
            styles,
        ),
        numbered(["After these lines, explain how many shared owners there are and when the int can be destroyed."], styles, start=8),
        p("Question 9 - weak_ptr access:", styles),
        code(
            """
std::weak_ptr<int> observer = a;
/* safely print the int if it still exists */
            """,
            styles,
        ),
        numbered(["Write the safe access pattern using <font face=\"Courier\">lock()</font>."], styles, start=9),
        p("Question 10 - choose the pointer type:", styles),
        code(
            """
// A tree node has one owning parent pointer to each child.
// A cache entry may be referenced by several systems.
// A back pointer observes an object owned elsewhere.
            """,
            styles,
        ),
        numbered(["For each situation, choose <font face=\"Courier\">unique_ptr</font>, <font face=\"Courier\">shared_ptr</font>, or <font face=\"Courier\">weak_ptr</font> and explain the ownership reason."], styles, start=10),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "<font face=\"Courier\">g++ main.o sensor.o -o program</font>.",
                "<font face=\"Courier\">program.o</font> would mean another object file. The link step produces the final executable, so it is normally named <font face=\"Courier\">program</font>.",
                "CMake configures/generates build files and drives a build tool. It does not replace the compiler; the generated build still runs compiler/linker commands such as <font face=\"Courier\">g++</font>.",
                "<font face=\"Courier\">binary_search</font> requires a sorted range. Fix: <font face=\"Courier\">std::sort(values.begin(), values.end());</font> before the search.",
                "Expected: <font face=\"Courier\">[](int a, int b) { return a &#62; b; }</font>.",
                "<font face=\"Courier\">int n = std::count(xs.begin(), xs.end(), 4);</font>.",
                "Expected: <font face=\"Courier\">[](int value) { return value &#62; 10; }</font>.",
                "There are three shared owners. The managed <font face=\"Courier\">int</font> is destroyed after the last shared pointer owning it is destroyed or reset.",
                "Expected: <font face=\"Courier\">if (auto p = observer.lock()) { std::cout &#60;&#60; *p; }</font>. <font face=\"Courier\">lock()</font> checks whether the object still exists.",
                "Tree child ownership: <font face=\"Courier\">unique_ptr</font>. Shared cache entry: <font face=\"Courier\">shared_ptr</font>. Non-owning back pointer: <font face=\"Courier\">weak_ptr</font> to avoid extending lifetime or creating ownership cycles.",
            ],
            styles,
        ),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
