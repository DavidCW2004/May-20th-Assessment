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


OUT = Path(__file__).with_name("cpp-templates-stl-study-pack.pdf")


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
        title="C++ Templates and STL Study Pack",
    )

    story = [
        p("C++ Templates and STL", styles, "TopicTitle"),
        p("Focused revision sheet based on ECM2433 L16 Templates and STL, chosen from a red item in the revision RAG tracker.", styles, "SourceText"),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Why templates exist", styles, "DarkHeading"),
        p("Templates let you write one piece of generic C++ code and let the compiler generate type-specific versions when needed. They avoid writing almost identical functions or classes for <font face=\"Courier\">int</font>, <font face=\"Courier\">float</font>, <font face=\"Courier\">string</font>, and other types.", styles),
        code(
            """
void myswap(int &x, int &y) {
    int temp = x;
    x = y;
    y = temp;
}

void myswap(float &x, float &y) {
    float temp = x;
    x = y;
    y = temp;
}
            """,
            styles,
        ),
        p("A function template keeps the logic once and leaves the type as a parameter:", styles),
        code(
            """
template<typename T>
void myswap(T &x, T &y) {
    T temp = x;
    x = y;
    y = temp;
}
            """,
            styles,
        ),
        p("2. Templates vs macros", styles, "DarkHeading"),
        p("Macros run before compilation and perform text substitution. Templates are checked by the compiler, so they are usually safer, more modular, and better for type-correct generic code.", styles),
        bullets(
            [
                "Macros can cause linker problems if they generate repeated definitions in multiple source files.",
                "Macros do not give normal C++ type checking.",
                "Templates are instantiated by the compiler for the types you actually use.",
                "A template is not itself a type; <font face=\"Courier\">Stack&lt;int&gt;</font> is a type produced from the template.",
            ],
            styles,
        ),
        p("3. Function templates", styles, "DarkHeading"),
        p("A function template starts with <font face=\"Courier\">template&lt;typename T&gt;</font>. The compiler deduces <font face=\"Courier\">T</font> from the arguments when the function is called.", styles),
        code(
            """
int a = 1, b = 2;
myswap(a, b);        // T is int

std::string c = "cat";
std::string d = "dog";
myswap(c, d);        // T is std::string
            """,
            styles,
        ),
        p("If the argument types do not match the template, the compiler rejects the call. For example, <font face=\"Courier\">myswap(a, f)</font> with an <font face=\"Courier\">int</font> and a <font face=\"Courier\">float</font> is not a match for <font face=\"Courier\">T &#38;x, T &#38;y</font>.", styles),
        p("4. Class templates", styles, "DarkHeading"),
        p("A class template builds a family of similar classes. A stack of integers and a stack of strings can share one template definition.", styles),
        code(
            """
template<typename T>
class Stack {
    T stck[100];
    int index;
public:
    void push(T value);
    T pop();
};

Stack<int> numbers;
Stack<std::string> words;
            """,
            styles,
        ),
        p("When defining member functions outside the class body, remember that <font face=\"Courier\">Stack</font> alone is not a concrete type; use <font face=\"Courier\">Stack&lt;T&gt;</font>.", styles),
        code(
            """
template<typename T>
T Stack<T>::pop() {
    /* implementation */
}
            """,
            styles,
        ),
        p("General practice is to keep both the template interface and implementation in a header file, because the compiler needs the full template definition when it instantiates it.", styles),
        p("5. STL containers", styles, "DarkHeading"),
        p("The Standard Template Library provides common generic data structures and algorithms. Containers store collections of elements.", styles),
        bullets(
            [
                "Sequence containers store linear sequences, such as <font face=\"Courier\">array</font>, <font face=\"Courier\">vector</font>, <font face=\"Courier\">deque</font>, and <font face=\"Courier\">list</font>.",
                "Associative containers organize elements by keys, such as <font face=\"Courier\">set</font>, <font face=\"Courier\">map</font>, and their unordered versions.",
                "Container adapters provide restricted interfaces, such as <font face=\"Courier\">stack</font>, <font face=\"Courier\">queue</font>, and <font face=\"Courier\">priority_queue</font>.",
            ],
            styles,
        ),
        code(
            """
#include <stack>

std::stack<int> si;
si.push(43);
si.push(99);
std::cout << si.top() << std::endl; // 99
si.pop();
std::cout << si.top() << std::endl; // 43
            """,
            styles,
        ),
        p("6. <font face=\"Courier\">std::vector</font> and iterators", styles, "DarkHeading"),
        p("<font face=\"Courier\">std::vector</font> is a growable sequence container. It supports <font face=\"Courier\">push_back</font>, <font face=\"Courier\">size</font>, and indexed access with <font face=\"Courier\">operator[]</font>.", styles),
        code(
            """
#include <vector>

std::vector<int> v;
v.push_back(43);
v.push_back(99);
std::cout << v.size() << std::endl;
std::cout << v[1] << std::endl;
            """,
            styles,
        ),
        p("Iterators are objects used to traverse containers. <font face=\"Courier\">begin()</font> points at the first element and <font face=\"Courier\">end()</font> points one-past-the-last element.", styles),
        code(
            """
for (auto it = v.begin(); it != v.end(); it++) {
    std::cout << *it << std::endl;
}
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Explain why a template is better than writing separate <font face=\"Courier\">myswap</font> functions for <font face=\"Courier\">int</font>, <font face=\"Courier\">float</font>, and <font face=\"Courier\">string</font>.",
                "Explain one problem with using a macro to generate swap functions instead of using a template.",
                "Write a function template <font face=\"Courier\">myswap</font> that swaps two values of the same type by reference.",
                "Why would <font face=\"Courier\">myswap(a, b)</font> fail if <font face=\"Courier\">a</font> is an <font face=\"Courier\">int</font> and <font face=\"Courier\">b</font> is a <font face=\"Courier\">float</font>?",
                "Write the declaration of a class template <font face=\"Courier\">Box</font> that stores one value of type <font face=\"Courier\">T</font> and has a <font face=\"Courier\">get</font> method.",
                "When defining a class template member function outside the class body, why do you write <font face=\"Courier\">Stack&lt;T&gt;::pop</font> rather than <font face=\"Courier\">Stack::pop</font>?",
                "Explain why template implementations are often kept in header files.",
                "Write code using <font face=\"Courier\">std::stack&lt;int&gt;</font> to push <font face=\"Courier\">10</font> and <font face=\"Courier\">20</font>, print the top value, then pop once.",
                "Write code using <font face=\"Courier\">std::vector&lt;int&gt;</font> to store <font face=\"Courier\">1</font>, <font face=\"Courier\">2</font>, and <font face=\"Courier\">3</font>, then print the second value.",
                "Write a loop using <font face=\"Courier\">auto</font> and iterators to print every value in a <font face=\"Courier\">std::vector&lt;int&gt;</font>.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Good answers should show type-safety, instantiation, and correct STL operations.", styles, "SourceText"),
        numbered(
            [
                "A template avoids duplicated logic. The compiler generates type-specific versions when used, so one generic definition works for many types.",
                "Macros are text substitution before compilation. They can cause repeated definitions, poor type checking, and harder-to-trace errors.",
                "Expected pattern: <font face=\"Courier\">template&lt;typename T&gt; void myswap(T &#38;x, T &#38;y) { T temp = x; x = y; y = temp; }</font>.",
                "The template expects both parameters to have the same <font face=\"Courier\">T</font>. An <font face=\"Courier\">int</font> and a <font face=\"Courier\">float</font> cannot both bind to one same <font face=\"Courier\">T</font> in <font face=\"Courier\">myswap(T&#38;, T&#38;)</font>.",
                "A valid answer defines <font face=\"Courier\">template&lt;typename T&gt; class Box { T value; public: T get(); };</font> or equivalent.",
                "<font face=\"Courier\">Stack</font> is the template name, not a concrete type. <font face=\"Courier\">Stack&lt;T&gt;</font> is the templated class being defined for a particular type parameter.",
                "The compiler needs to see the full template definition when it instantiates the template for a specific type, so header-only template definitions are common.",
                "Expected use: <font face=\"Courier\">std::stack&lt;int&gt; s; s.push(10); s.push(20); std::cout &lt;&lt; s.top(); s.pop();</font>.",
                "Expected use: <font face=\"Courier\">std::vector&lt;int&gt; v; v.push_back(1); v.push_back(2); v.push_back(3); std::cout &lt;&lt; v[1];</font>.",
                "Expected pattern: <font face=\"Courier\">for (auto it = v.begin(); it != v.end(); it++) { std::cout &lt;&lt; *it; }</font>.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
template<typename T>
void myswap(T &x, T &y) {
    T temp = x;
    x = y;
    y = temp;
}

std::vector<int> v;
v.push_back(1);
v.push_back(2);

for (auto it = v.begin(); it != v.end(); it++) {
    std::cout << *it << std::endl;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
