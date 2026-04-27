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


OUT = Path(__file__).with_name("cpp-virtual-functions-dynamic-binding-study-pack.pdf")


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
        title="C++ Virtual Functions and Dynamic Binding Study Pack",
    )

    story = [
        p("C++ Virtual Functions and Dynamic Binding", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 L14 Inheritance and the C++ temperature sensor exercise, chosen from a red C++ topic not yet covered in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Base and derived classes", styles, "DarkHeading"),
        p(
            "Inheritance lets a derived class reuse and specialise a base class. With public inheritance, a derived object can be used where a base object reference or pointer is expected.",
            styles,
        ),
        code(
            """
class Sensor {
protected:
    std::string name;

public:
    Sensor(const std::string &name) : name(name) {}
    double read() const { return 0.0; }
};

class TemperatureSensor : public Sensor {
    double celsius;

public:
    TemperatureSensor(const std::string &name, double celsius)
        : Sensor(name), celsius(celsius) {}

    double read() const { return celsius; }
};
            """,
            styles,
        ),
        p(
            "Without <font face=\"Courier\">virtual</font>, a call through a base pointer uses the base class version. That is static binding: the compiler chooses the function from the pointer type.",
            styles,
        ),
        p("2. Virtual functions", styles, "DarkHeading"),
        p(
            "A virtual function allows runtime dispatch. If a base pointer points at a derived object, a virtual call uses the derived implementation.",
            styles,
        ),
        code(
            """
class Sensor {
public:
    virtual double read() const {
        return 0.0;
    }
};

class TemperatureSensor : public Sensor {
    double celsius;

public:
    double read() const override {
        return celsius;
    }
};

TemperatureSensor temp("Server Room", 18.0);
Sensor *sensor = &temp;
double value = sensor->read();  // calls TemperatureSensor::read
            """,
            styles,
        ),
        p(
            "This is dynamic binding: the actual object type matters at runtime. The pointer type is <font face=\"Courier\">Sensor *</font>, but the object is a <font face=\"Courier\">TemperatureSensor</font>.",
            styles,
        ),
        p("3. <font face=\"Courier\">override</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">override</font> asks the compiler to check that the derived function really overrides a virtual base function. It catches spelling mistakes, missing <font face=\"Courier\">const</font>, and wrong parameter lists.",
            styles,
        ),
        code(
            """
class Sensor {
public:
    virtual double read() const;
};

class TemperatureSensor : public Sensor {
public:
    double read() const override;  // checked by compiler
};
            """,
            styles,
        ),
        p(
            "If the base has <font face=\"Courier\">virtual double read() const</font> but the derived class writes <font face=\"Courier\">double read()</font>, that is not the same signature. <font face=\"Courier\">override</font> makes the compiler reject the mistake.",
            styles,
        ),
        p("4. Pure virtual functions", styles, "DarkHeading"),
        p(
            "A pure virtual function has no base implementation and makes the class abstract. You cannot directly create an object of an abstract class, but you can use references and pointers to it.",
            styles,
        ),
        code(
            """
class Sensor {
public:
    virtual double read() const = 0;
};

class TemperatureSensor : public Sensor {
public:
    double read() const override {
        return 21.5;
    }
};
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">Sensor</font> defines the interface.",
                "<font face=\"Courier\">TemperatureSensor</font> provides the concrete behaviour.",
                "A class with an unimplemented pure virtual function cannot be instantiated.",
            ],
            styles,
        ),
        p("5. Base pointers, references, and slicing", styles, "DarkHeading"),
        p(
            "Runtime polymorphism works through pointers and references. If you copy a derived object into a base object by value, the derived part is sliced away.",
            styles,
        ),
        code(
            """
void print_reading(const Sensor &sensor) {
    std::cout << sensor.read() << std::endl;
}

TemperatureSensor temp("Lab", 21.5);
print_reading(temp);  // dynamic dispatch through reference

Sensor *ptr = &temp;
std::cout << ptr->read() << std::endl;
            """,
            styles,
        ),
        p(
            "Prefer a base reference when the object is owned elsewhere. Prefer a smart pointer such as <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt;</font> when the base pointer owns the object.",
            styles,
        ),
        p("6. Virtual destructors", styles, "DarkHeading"),
        p(
            "If a class is intended to be used polymorphically through a base pointer, give the base class a virtual destructor. This allows deletion through the base pointer to clean up the derived object properly.",
            styles,
        ),
        code(
            """
class Sensor {
public:
    virtual ~Sensor() = default;
    virtual double read() const = 0;
};

std::unique_ptr<Sensor> sensor =
    std::make_unique<TemperatureSensor>("Server Room", 18.0);
            """,
            styles,
        ),
        p("7. Constructors and base initialisation", styles, "DarkHeading"),
        p(
            "Base constructors run before derived constructors. If the base needs parameters, the derived constructor passes them using a member initializer list.",
            styles,
        ),
        code(
            """
class Sensor {
    int id;

protected:
    std::string name;

public:
    Sensor(int id, const std::string &name)
        : id(id), name(name) {}
};

class TemperatureSensor : public Sensor {
    double celsius;

public:
    TemperatureSensor(int id, const std::string &name, double celsius)
        : Sensor(id, name), celsius(celsius) {}
};
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Fix the base and derived declarations so <font face=\"Courier\">Sensor *s = &#38;temp; s-&gt;read();</font> calls <font face=\"Courier\">TemperatureSensor::read</font>.",
                "Given a base method <font face=\"Courier\">virtual double read() const;</font>, repair the derived declaration <font face=\"Courier\">double read();</font> so the compiler checks it is a real override.",
                "Trace the call result for <font face=\"Courier\">TemperatureSensor temp(\"Lab\", 21.5); Sensor *s = &#38;temp; s-&gt;read();</font> when <font face=\"Courier\">read</font> is virtual.",
                "Change <font face=\"Courier\">Sensor</font> so it cannot be instantiated directly and every concrete sensor must provide <font face=\"Courier\">read</font>.",
                "Write a function <font face=\"Courier\">print_reading</font> that borrows any <font face=\"Courier\">Sensor</font> object and prints the result of its virtual <font face=\"Courier\">read</font> method.",
                "A function takes <font face=\"Courier\">Sensor sensor</font> by value. Replace the parameter type so dynamic dispatch is preserved for derived sensor objects.",
                "Add the destructor line a polymorphic base class should have when objects may be destroyed through a base pointer.",
                "Complete the <font face=\"Courier\">TemperatureSensor</font> constructor initializer list so it passes <font face=\"Courier\">id</font> and <font face=\"Courier\">name</font> to <font face=\"Courier\">Sensor</font> and stores <font face=\"Courier\">celsius</font>.",
                "Fill in the smart-pointer declaration that owns a <font face=\"Courier\">TemperatureSensor</font> through a <font face=\"Courier\">Sensor</font> pointer type.",
                "In a short code fragment, show the difference between a non-virtual base call and a virtual base call through <font face=\"Courier\">Sensor *</font>.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should produce legal C++ and identify whether the call is chosen from the pointer type or actual object type.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "Make the base method virtual and make the derived method match the signature, for example <font face=\"Courier\">virtual double read() const;</font> in <font face=\"Courier\">Sensor</font> and <font face=\"Courier\">double read() const override;</font> in <font face=\"Courier\">TemperatureSensor</font>.",
                "The derived declaration should keep the same signature and add <font face=\"Courier\">override</font>: <font face=\"Courier\">double read() const override;</font>.",
                "The result is <font face=\"Courier\">21.5</font>. Because <font face=\"Courier\">read</font> is virtual, the call through <font face=\"Courier\">Sensor *</font> dispatches to the actual <font face=\"Courier\">TemperatureSensor</font> object.",
                "Use a pure virtual function: <font face=\"Courier\">virtual double read() const = 0;</font>. That makes <font face=\"Courier\">Sensor</font> abstract.",
                "Expected pattern: <font face=\"Courier\">void print_reading(const Sensor &#38;sensor) { std::cout &lt;&lt; sensor.read(); }</font>.",
                "Use a reference or pointer, for example <font face=\"Courier\">const Sensor &#38;sensor</font> or <font face=\"Courier\">Sensor *sensor</font>. Passing by value slices derived objects.",
                "Use <font face=\"Courier\">virtual ~Sensor() = default;</font> in the base class.",
                "Expected pattern: <font face=\"Courier\">TemperatureSensor(int id, const std::string &#38;name, double celsius) : Sensor(id, name), celsius(celsius) {}</font>.",
                "Expected pattern: <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; sensor = std::make_unique&lt;TemperatureSensor&gt;(id, name, value);</font>.",
                "Without <font face=\"Courier\">virtual</font>, <font face=\"Courier\">s-&gt;read()</font> uses the base version. With <font face=\"Courier\">virtual</font>, it uses the derived version for a derived object.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
class Sensor {
protected:
    std::string name;

public:
    Sensor(const std::string &name) : name(name) {}
    virtual ~Sensor() = default;
    virtual double read() const = 0;
};

class TemperatureSensor : public Sensor {
    double celsius;

public:
    TemperatureSensor(const std::string &name, double celsius)
        : Sensor(name), celsius(celsius) {}

    double read() const override {
        return celsius;
    }
};

void print_reading(const Sensor &sensor) {
    std::cout << sensor.read() << std::endl;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
