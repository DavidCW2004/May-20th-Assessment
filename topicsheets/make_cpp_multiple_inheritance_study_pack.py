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


OUT = Path(__file__).with_name("cpp-multiple-inheritance-study-pack.pdf")


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
        title="C++ Multiple Inheritance Study Pack",
    )

    story = [
        p("C++ Multiple Inheritance", styles, "TopicTitle"),
        p(
            "Grounded in ECM2433 inheritance material. Focuses on inherited access, "
            "multiple inheritance syntax, the diamond problem, virtual base classes, "
            "virtual member functions, and runtime dispatch through base-class pointers.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),

        p("1. Inherited access depends on the inheritance specifier", styles, "DarkHeading"),
        p(
            "The access specifier in the class head changes how inherited public and protected "
            "members appear inside the derived class. Private members of the base are still "
            "private to the base and cannot be accessed directly by derived code.",
            styles,
        ),
        bullets(
            [
                "<b>Public inheritance</b>: inherited public stays public; inherited protected "
                "stays protected.",
                "<b>Protected inheritance</b>: inherited public and protected become protected.",
                "<b>Private inheritance</b>: inherited public and protected become private.",
                "A <font face=\"Courier\">class</font> inherits privately by default. "
                "A <font face=\"Courier\">struct</font> inherits publicly by default.",
            ],
            styles,
        ),
        code(
            r"""
class Base {
    int private_value;
protected:
    int protected_value;
public:
    void set(int a, int b) { private_value = a; protected_value = b; }
};

class Derived : protected Base {
public:
    void reset() {
        protected_value = 0;  /* OK: protected member */
        set(1, 2);            /* OK inside Derived */
        /* private_value = 3;  ERROR: private to Base */
    }
};

int main() {
    Derived d;
    d.reset();      /* OK */
    d.set(1, 2);    /* ERROR: set became protected in Derived */
}
            """,
            styles,
        ),

        p("2. Multiple inheritance lists more than one base", styles, "DarkHeading"),
        p(
            "A derived class can inherit from several base classes by separating them with "
            "commas. The derived object then contains base-class subobjects for each base.",
            styles,
        ),
        code(
            r"""
class HasX {
protected:
    int x;
public:
    void show_x() const { std::cout << x << "\n"; }
};

class HasY {
protected:
    int y;
public:
    void show_y() const { std::cout << y << "\n"; }
};

class Point : public HasX, public HasY {
public:
    void set(int new_x, int new_y) { x = new_x; y = new_y; }
};
            """,
            styles,
        ),

        p("3. The diamond problem creates duplicate base subobjects", styles, "DarkHeading"),
        p(
            "If two intermediate bases both inherit from the same base, the final derived "
            "class can receive two separate copies of that shared base. Unqualified access to "
            "a member of the shared base then becomes ambiguous.",
            styles,
        ),
        code(
            r"""
class Base { public: int value; };
class Left : public Base {};
class Right : public Base {};
class Bottom : public Left, public Right {};

int main() {
    Bottom b;
    b.value = 10;        /* ERROR: Left::Base::value or Right::Base::value? */
    b.Left::value = 10;  /* OK: explicitly selects one copy */
}
            """,
            styles,
        ),

        p("4. Virtual base classes share one base subobject", styles, "DarkHeading"),
        p(
            "Use virtual inheritance on the intermediate classes when the final class should "
            "contain only one shared copy of the common base. The most-derived class is then "
            "responsible for constructing that virtual base.",
            styles,
        ),
        code(
            r"""
class Base { public: int value; };
class Left : virtual public Base {};
class Right : virtual public Base {};
class Bottom : public Left, public Right {};

int main() {
    Bottom b;
    b.value = 10;        /* OK: only one Base subobject */
}
            """,
            styles,
        ),

        p("5. Virtual functions choose the override at runtime", styles, "DarkHeading"),
        p(
            "A virtual member function allows derived classes to override behaviour. When the "
            "function is called through a base pointer or reference, C++ uses the actual object "
            "type at runtime to choose the correct override.",
            styles,
        ),
        code(
            r"""
class Animal {
protected:
    std::string name;
public:
    Animal(std::string n) : name(n) {}
    virtual void speak() const { std::cout << name << "\n"; }
};

class Dog : public Animal {
public:
    Dog(std::string n) : Animal(n) {}
    void speak() const override { std::cout << "Bark " << name << "\n"; }
};

Dog pet("Fido");
Animal *a = &pet;
a->speak();     /* Bark Fido */
            """,
            styles,
        ),

        p("6. Constructor order and virtual bases", styles, "DarkHeading"),
        p(
            "Base constructors run before the derived constructor body. With virtual bases, the "
            "most-derived class constructs the virtual base directly, even if intermediate "
            "classes also mention it in their initializer lists. Destructors run in the reverse "
            "order.",
            styles,
        ),
        code(
            r"""
class Animal {
public:
    Animal(std::string name) {}
    virtual void speak() const = 0;
    virtual ~Animal() = default;
};

class Wolf : virtual public Animal {
public:
    Wolf(std::string name) : Animal(name) {}
};

class Poodle : virtual public Animal {
public:
    Poodle(std::string name) : Animal(name) {}
};

class Dog : public Wolf, public Poodle {
public:
    Dog(std::string name) : Animal(name), Wolf(name), Poodle(name) {}
    void speak() const override {}
};
            """,
            styles,
        ),

        p("Practice Questions", styles, "BlueHeading"),
        p("Questions 1 to 3 use this code:", styles),
        code(
            r"""
class Base {
    int i;
protected:
    int j;
public:
    void set(int a, int b) { i = a; j = b; }
    void show() const { std::cout << i << " " << j << "\n"; }
};

class Derived : public Base {
public:
    void reset() { j = 0; }
    void show_all() const { show(); }
};

int main() {
    Derived obj;
    obj.set(1, 2);      /* line A */
    obj.show();         /* line B */
    obj.show_all();     /* line C */
    obj.i = 5;          /* line D */
}
            """,
            styles,
        ),
        numbered(
            [
                "For lines A to D, identify which compile and which do not.",
                "Change the inheritance line to <font face=\"Courier\">class Derived : protected Base</font>. "
                "Now identify which of lines A to D compile.",
                "In <font face=\"Courier\">reset</font>, explain why <font face=\"Courier\">j = 0</font> "
                "is allowed but <font face=\"Courier\">i = 0</font> would not compile.",
            ],
            styles,
        ),

        p("Questions 4 to 6 use this code:", styles),
        code(
            r"""
class Base { public: int value; };
class Left : public Base {};
class Right : public Base {};
class Bottom : public Left, public Right {};

int main() {
    Bottom b;
    b.value = 10;       /* line E */
}
            """,
            styles,
        ),
        numbered(
            [
                "Explain why line E fails to compile.",
                "Rewrite line E so it selects the value inherited through Left.",
                "Change the class definitions so <font face=\"Courier\">b.value = 10;</font> "
                "compiles without needing scope resolution.",
            ],
            styles,
            start=4,
        ),

        p("Questions 7 to 10 use this code:", styles),
        code(
            r"""
class Animal {
protected:
    std::string name;
public:
    Animal(std::string n) : name(n) {}
    virtual void speak() const { std::cout << name << "\n"; }
};

class Dog : public Animal {
public:
    Dog(std::string n) : Animal(n) {}
    void speak() const override { std::cout << "Bark " << name << "\n"; }
};

int main() {
    Dog pet("Fido");
    pet.speak();        /* line F */
    Animal *a = &pet;
    a->speak();         /* line G */
}
            """,
            styles,
        ),
        numbered(
            [
                "Trace lines F and G. What does each line print?",
                "Remove <font face=\"Courier\">virtual</font> from "
                "<font face=\"Courier\">Animal::speak</font>. What does line G print now?",
                "Make <font face=\"Courier\">Animal::speak</font> pure virtual. What happens if "
                "someone writes <font face=\"Courier\">Animal a(\"Rex\");</font>?",
                "Add the destructor declaration Animal should usually have when it is used "
                "through base-class pointers.",
            ],
            styles,
            start=7,
        ),

        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Attempt the questions before checking. Equivalent wording is fine if it correctly "
            "uses inherited access, virtual bases, and virtual dispatch.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "A, B, and C compile. D does not compile because i is private in Base.",
                "With protected inheritance, A and B no longer compile from main because "
                "set and show become protected in Derived. C still compiles because show_all "
                "is public in Derived. D still does not compile.",
                "j is protected, so Derived member functions can access it. i is private, so "
                "only Base member functions can access it directly.",
                "Bottom contains two Base subobjects: one through Left and one through Right. "
                "The expression b.value is ambiguous.",
                "Use <font face=\"Courier\">b.Left::value = 10;</font>.",
                "Make the intermediate inheritance virtual: "
                "<font face=\"Courier\">class Left : virtual public Base {};</font> and "
                "<font face=\"Courier\">class Right : virtual public Base {};</font>.",
                "Line F prints <font face=\"Courier\">Bark Fido</font>. Line G also prints "
                "<font face=\"Courier\">Bark Fido</font> because speak is virtual.",
                "Without virtual, line G uses the base-pointer type and prints "
                "<font face=\"Courier\">Fido</font>.",
                "Animal becomes abstract, so <font face=\"Courier\">Animal a(\"Rex\");</font> "
                "does not compile.",
                "Use <font face=\"Courier\">virtual ~Animal() = default;</font>.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            r"""
/* Multiple inheritance */
class Derived : public Base1, public Base2 {};

/* Diamond fix */
class Left : virtual public Base {};
class Right : virtual public Base {};
class Bottom : public Left, public Right {};

/* Virtual dispatch */
class Base {
public:
    virtual void f() const = 0;
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void f() const override {}
};

Base *ptr = &derived_object;
ptr->f();       /* calls Derived::f at runtime */
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
