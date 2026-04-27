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


OUT = Path(__file__).with_name("cpp-operator-overloading-study-pack.pdf")


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
        title="C++ Operator Overloading Study Pack",
    )

    story = [
        p("C++ Operator Overloading", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 L15 Operator Overloading, chosen from a red C++ topic not yet covered in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Why overload operators", styles, "DarkHeading"),
        p(
            "Operator overloading gives an existing C++ operator a class-specific meaning. The aim is to make code easier for users of the class to read, not to save effort for the class developer.",
            styles,
        ),
        code(
            """
MyDate dt1(29, 6, 2015);
MyDate dt2(1, 3, 2021);

int diff = dt2 - dt1;    // nicer than dt2.difference(dt1)
MyDate dt3 = dt2 + 43;   // nicer than dt2.addDays(43)
            """,
            styles,
        ),
        p(
            "Only overload an operator when the result matches what a reader would naturally expect. This is the law of least surprise.",
            styles,
        ),
        p("2. Basic syntax", styles, "DarkHeading"),
        p(
            "An overloaded operator is a function whose name starts with <font face=\"Courier\">operator</font> followed by the symbol. As a member function, the left-hand operand is the object before the operator.",
            styles,
        ),
        code(
            """
class MyInteger {
    int i;
public:
    MyInteger(int value) : i(value) {}

    int operator+(MyInteger other) {
        return i + other.i;
    }

    int operator+(int value) {
        return i + value;
    }
};

MyInteger a(4);
MyInteger b(3);
int total = a + b;  // calls a.operator+(b)
int next = a + 6;   // calls a.operator+(6)
            """,
            styles,
        ),
        p("3. Member vs non-member overloads", styles, "DarkHeading"),
        p(
            "A member operator works when the left-hand operand is the class object. If the left-hand operand is not your class, you normally need a non-member operator.",
            styles,
        ),
        code(
            """
MyInteger c(4);

int x = c + 8;  // can use member: c.operator+(8)
int y = 8 + c;  // needs non-member operator+(int, MyInteger)
            """,
            styles,
        ),
        p(
            "If the non-member operator needs private fields, declare it as a <font face=\"Courier\">friend</font>. A friend function is not a member of the class, but it can access private and protected fields of that class.",
            styles,
        ),
        code(
            """
class MyInteger {
    int i;
public:
    MyInteger(int value) : i(value) {}
    friend int operator+(int value, MyInteger m);
};

int operator+(int value, MyInteger m) {
    return value + m.i;
}
            """,
            styles,
        ),
        p("4. Rules and limits", styles, "DarkHeading"),
        bullets(
            [
                "At least one operand must be a user-defined type, such as a class.",
                "Some operators cannot be overloaded: <font face=\"Courier\">.</font>, <font face=\"Courier\">sizeof</font>, <font face=\"Courier\">?:</font>, <font face=\"Courier\">::</font>, and <font face=\"Courier\">.*</font>.",
                "You cannot change precedence or associativity. Overloaded operators are still parsed using the normal operator rules.",
                "Overloaded <font face=\"Courier\">&#38;&#38;</font> and <font face=\"Courier\">||</font> do not preserve normal short-circuit behaviour.",
                "Just because an operator can be overloaded does not mean it should be.",
            ],
            styles,
        ),
        p("5. Subscript and call operators", styles, "DarkHeading"),
        p(
            "Overloading <font face=\"Courier\">[]</font> is useful for array-like classes. Return a reference if callers should be able to assign through the subscript.",
            styles,
        ),
        code(
            """
class MyArray {
    int data[100];
public:
    int &operator[](unsigned int index) {
        if (index >= 100) {
            throw std::out_of_range("index");
        }
        return data[index];
    }
};

MyArray a;
a[10] = 42;
            """,
            styles,
        ),
        p(
            "The <font face=\"Courier\">[]</font> operator takes one index. For a matrix-style object needing row and column, overload <font face=\"Courier\">()</font> instead.",
            styles,
        ),
        code(
            """
class Matrix {
public:
    int &operator()(unsigned int row, unsigned int col);
};

m(5, 1) = 99;
            """,
            styles,
        ),
        p("6. Stream insertion", styles, "DarkHeading"),
        p(
            "Overload stream insertion when you want <font face=\"Courier\">std::cout</font> to print your object naturally. It is usually a non-member function because the left-hand operand is the stream.",
            styles,
        ),
        code(
            """
#include <iostream>

class MyDate {
    unsigned int day;
    unsigned int month;
    int year;
public:
    MyDate(unsigned int d, unsigned int m, int y)
        : day(d), month(m), year(y) {}

    friend std::ostream &operator<<(std::ostream &os,
                                    const MyDate &dt);
};

std::ostream &operator<<(std::ostream &os, const MyDate &dt) {
    os << dt.day << '/' << dt.month << '/' << dt.year;
    return os;
}
            """,
            styles,
        ),
        p(
            "Returning the same stream reference enables chaining, such as <font face=\"Courier\">std::cout &lt;&lt; \"Date: \" &lt;&lt; dt &lt;&lt; std::endl</font>.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Complete the missing body for <font face=\"Courier\">int MyInteger::operator+(MyInteger other)</font> so <font face=\"Courier\">MyInteger a(4), b(3); int x = a + b;</font> gives <font face=\"Courier\">7</font>.",
                "Add a member overload so <font face=\"Courier\">MyInteger a(4); int x = a + 6;</font> gives <font face=\"Courier\">10</font>.",
                "The expression <font face=\"Courier\">8 + a</font> fails even though <font face=\"Courier\">a + 8</font> works. Write the non-member operator header that fixes it.",
                "A non-member <font face=\"Courier\">operator+</font> needs to read private field <font face=\"Courier\">i</font>. Change the class declaration so that operator can legally read it.",
                "For a class <font face=\"Courier\">Point</font>, decide whether overloading <font face=\"Courier\">+</font>, <font face=\"Courier\">sizeof</font>, and <font face=\"Courier\">.</font> is possible. For possible ones, say whether it would be a sensible design.",
                "Complete <font face=\"Courier\">operator[]</font> for a small array class so <font face=\"Courier\">arr[2] = 99;</font> modifies the stored element rather than a copy.",
                "A matrix class needs two indices. Choose between <font face=\"Courier\">[]</font> and <font face=\"Courier\">()</font>, then write the operator header.",
                "Write a stream insertion overload header for <font face=\"Courier\">MyDate</font> so <font face=\"Courier\">std::cout &lt;&lt; dt;</font> compiles.",
                "Fill in the body of the <font face=\"Courier\">MyDate</font> stream insertion function so it prints <font face=\"Courier\">day/month/year</font> and still supports chained output.",
                "A developer wants <font face=\"Courier\">account1 + account2</font> to transfer money from one bank account to another. Decide whether this is good operator design and give a better interface.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should produce legal overloads and justify whether the operator meaning is natural.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "Return the sum of the two stored integer values, for example <font face=\"Courier\">return i + other.i;</font> inside the member function.",
                "Add a member such as <font face=\"Courier\">int operator+(int value) { return i + value; }</font>.",
                "Use a non-member with the built-in type on the left, for example <font face=\"Courier\">int operator+(int value, MyInteger m)</font>.",
                "Declare the non-member as a friend inside the class, for example <font face=\"Courier\">friend int operator+(int value, MyInteger m);</font>.",
                "<font face=\"Courier\">+</font> can be overloaded if at least one operand is a class type, but it should only be used if point addition is meaningful. <font face=\"Courier\">sizeof</font> and <font face=\"Courier\">.</font> cannot be overloaded.",
                "Return <font face=\"Courier\">int&amp;</font>, not plain <font face=\"Courier\">int</font>. A reference lets assignment through the subscript update the stored array element.",
                "Use <font face=\"Courier\">operator()</font> for two indices, for example <font face=\"Courier\">int&amp; operator()(unsigned int row, unsigned int col)</font>.",
                "Use a non-member returning a stream reference, for example <font face=\"Courier\">std::ostream&amp; operator&lt;&lt;(std::ostream&amp; os, const MyDate&amp; dt)</font>.",
                "Write to the stream, then return it: <font face=\"Courier\">os &lt;&lt; dt.day &lt;&lt; '/' &lt;&lt; dt.month &lt;&lt; '/' &lt;&lt; dt.year; return os;</font>.",
                "That is poor design because <font face=\"Courier\">+</font> usually suggests producing a combined value, not mutating accounts. A clearer interface is a named function such as <font face=\"Courier\">transfer_to</font> or <font face=\"Courier\">transfer</font>.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
class MyInteger {
    int i;
public:
    MyInteger(int value) : i(value) {}

    int operator+(MyInteger other) {
        return i + other.i;
    }

    int operator+(int value) {
        return i + value;
    }

    friend int operator+(int value, MyInteger m);
};

int operator+(int value, MyInteger m) {
    return value + m.i;
}

std::ostream &operator<<(std::ostream &os, const MyDate &dt) {
    os << dt.day << '/' << dt.month << '/' << dt.year;
    return os;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
