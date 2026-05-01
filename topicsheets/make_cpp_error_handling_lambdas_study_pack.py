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


OUT = Path(__file__).with_name("cpp-error-handling-lambdas-study-pack.pdf")


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
        title="C++ Error Handling and Lambdas Study Pack",
    )

    story = [
        p("C++ Error Handling and Lambdas", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: try, catch, throw, standard exceptions, good exception practice, lambda syntax, and lambda capture.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Throwing exceptions", styles, "DarkHeading"),
        p(
            "An exception is a way to report an error that the current function cannot sensibly handle. Use <font face=\"Courier\">throw</font> to leave the current flow and search for a matching handler.",
            styles,
        ),
        code(
            """
#include <stdexcept>

double divide(double a, double b) {
    if (b == 0.0) {
        throw std::invalid_argument("division by zero");
    }
    return a / b;
}
            """,
            styles,
        ),
        p(
            "After <font face=\"Courier\">throw</font>, normal execution of that function stops. The program jumps to the nearest matching <font face=\"Courier\">catch</font> block.",
            styles,
        ),
        p("2. Catching exceptions", styles, "DarkHeading"),
        p(
            "Put code that may throw inside a <font face=\"Courier\">try</font> block. Put recovery or reporting code in one or more <font face=\"Courier\">catch</font> blocks.",
            styles,
        ),
        code(
            """
#include <iostream>
#include <stdexcept>

try {
    std::cout << divide(10.0, 0.0) << "\\n";
} catch (const std::invalid_argument& error) {
    std::cerr << "bad argument: " << error.what() << "\\n";
}
            """,
            styles,
        ),
        p(
            "Catch exception objects by <font face=\"Courier\">const</font> reference. This avoids copying and preserves the real dynamic exception type.",
            styles,
        ),
        p("3. Standard exception types", styles, "DarkHeading"),
        bullets(
            [
                "<font face=\"Courier\">std::invalid_argument</font>: argument value is not acceptable.",
                "<font face=\"Courier\">std::out_of_range</font>: index or value is outside the valid range.",
                "<font face=\"Courier\">std::runtime_error</font>: runtime failure that does not fit a more specific category.",
                "<font face=\"Courier\">std::exception</font>: common base class for standard exceptions.",
            ],
            styles,
        ),
        code(
            """
#include <stdexcept>
#include <vector>

int at_checked(const std::vector<int>& values, std::size_t index) {
    if (index >= values.size()) {
        throw std::out_of_range("index");
    }
    return values[index];
}
            """,
            styles,
        ),
        p("4. Catch order matters", styles, "DarkHeading"),
        p(
            "Catch more specific exception types before more general ones. If <font face=\"Courier\">std::exception</font> comes first, it catches standard derived exceptions before their specific handlers can run.",
            styles,
        ),
        code(
            """
try {
    value = at_checked(values, index);
} catch (const std::out_of_range& error) {
    std::cerr << "bad index: " << error.what() << "\\n";
} catch (const std::exception& error) {
    std::cerr << "other error: " << error.what() << "\\n";
}
            """,
            styles,
        ),
        p("5. Good exception practice", styles, "DarkHeading"),
        bullets(
            [
                "Throw exceptions for exceptional error cases, not for ordinary loop control.",
                "Catch only when this level can recover or add useful context.",
                "Prefer RAII-managed objects so cleanup still happens during stack unwinding.",
                "Do not throw raw strings if a standard exception type fits.",
                "Avoid swallowing an exception silently; the caller then loses the error signal.",
            ],
            styles,
        ),
        p(
            "Stack unwinding means C++ destroys local objects as it leaves scopes looking for a handler. This is why classes with destructors and smart pointers are important for exception-safe code.",
            styles,
        ),
        p("6. Lambda syntax", styles, "DarkHeading"),
        p(
            "A lambda is an unnamed function object written inline. The general shape is capture list, parameter list, optional return type, then body.",
            styles,
        ),
        code(
            """
auto square = [](int x) {
    return x * x;
};

int result = square(6);  // 36
            """,
            styles,
        ),
        p(
            "The empty capture list <font face=\"Courier\">[]</font> means the lambda does not use local variables from the surrounding scope.",
            styles,
        ),
        p("7. Capture by value and by reference", styles, "DarkHeading"),
        p(
            "A lambda can capture variables from the surrounding scope. Capture by value copies the variable into the lambda. Capture by reference lets the lambda access the original variable.",
            styles,
        ),
        code(
            """
int factor = 10;

auto by_value = [factor](int x) {
    return x * factor;
};

auto by_reference = [&factor](int x) {
    factor += 1;
    return x * factor;
};
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">[factor]</font> captures only <font face=\"Courier\">factor</font> by value.",
                "<font face=\"Courier\">[&amp;factor]</font> captures only <font face=\"Courier\">factor</font> by reference.",
                "<font face=\"Courier\">[=]</font> captures used locals by value.",
                "<font face=\"Courier\">[&amp;]</font> captures used locals by reference.",
            ],
            styles,
        ),
        p("8. Mutable lambdas", styles, "DarkHeading"),
        p(
            "A value capture is normally read-only inside the lambda body. Use <font face=\"Courier\">mutable</font> if the lambda should modify its own captured copy.",
            styles,
        ),
        code(
            """
int count = 0;

auto next = [count]() mutable {
    count += 1;
    return count;
};

next();  // 1
next();  // 2
// outer count is still 0
            """,
            styles,
        ),
        p(
            "The outer variable is unchanged because the lambda is modifying its private copy.",
            styles,
        ),
        p("9. Lambdas with algorithms", styles, "DarkHeading"),
        p(
            "Lambdas are often passed to standard algorithms to express small operations without writing a separate named function.",
            styles,
        ),
        code(
            """
#include <algorithm>
#include <vector>

std::vector<int> values = {1, 7, 3, 9, 2};
int threshold = 5;

int count = std::count_if(values.begin(), values.end(),
    [threshold](int value) {
        return value > threshold;
    });
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write a function that throws <font face=\"Courier\">std::invalid_argument</font> when a denominator is zero.",
                "Wrap a call to that function in <font face=\"Courier\">try</font> and catch the error by <font face=\"Courier\">const</font> reference.",
                "Choose a standard exception type for an invalid vector index and explain the choice.",
                "Explain why <font face=\"Courier\">catch (const std::exception&amp; e)</font> should usually come after more specific catches.",
                "Explain what stack unwinding does to local objects when an exception leaves a scope.",
                "Write a lambda that takes an <font face=\"Courier\">int</font> and returns its square.",
                "Given <font face=\"Courier\">int limit = 10;</font>, write a lambda that captures it by value and tests whether a number is greater than it.",
                "Write a lambda that captures a counter by reference and increments the original counter.",
                "Explain the difference between <font face=\"Courier\">[x]</font> and <font face=\"Courier\">[&amp;x]</font>.",
                "Use <font face=\"Courier\">std::count_if</font> with a lambda to count values greater than 5 in a vector.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Good answers should explain both syntax and the control-flow effect.", styles, "SourceText"),
        numbered(
            [
                "Expected pattern: check <font face=\"Courier\">b == 0</font> and <font face=\"Courier\">throw std::invalid_argument(\"...\")</font> before dividing.",
                "Expected: <font face=\"Courier\">try { ... } catch (const std::invalid_argument&amp; e) { ... e.what() ... }</font>.",
                "<font face=\"Courier\">std::out_of_range</font> fits an invalid index because the requested position is outside the valid range.",
                "A base-class catch can catch derived exceptions first, preventing specific handlers from running.",
                "C++ destroys local objects as it leaves scopes while searching for a handler; RAII uses this to clean up resources.",
                "Expected: <font face=\"Courier\">auto square = [](int x) { return x * x; };</font>.",
                "Expected: <font face=\"Courier\">auto above = [limit](int n) { return n &gt; limit; };</font>.",
                "Expected: <font face=\"Courier\">auto inc = [&amp;counter]() { counter += 1; };</font>.",
                "<font face=\"Courier\">[x]</font> copies <font face=\"Courier\">x</font> into the lambda; <font face=\"Courier\">[&amp;x]</font> lets the lambda access the original variable.",
                "Expected: <font face=\"Courier\">std::count_if(v.begin(), v.end(), [](int x) { return x &gt; 5; })</font>.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Catching exceptions by value and accidentally slicing derived exception types.",
                "Putting <font face=\"Courier\">catch (std::exception)</font> before a specific handler.",
                "Using exceptions for normal expected branches instead of errors.",
                "Forgetting that <font face=\"Courier\">[x]</font> captures a copy, not the original variable.",
                "Using reference capture when the lambda may outlive the referenced local variable.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
