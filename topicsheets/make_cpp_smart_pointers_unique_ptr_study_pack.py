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


OUT = Path(__file__).with_name("cpp-smart-pointers-unique-ptr-study-pack.pdf")


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
        title="C++ Smart Pointer Practice with std::unique_ptr Study Pack",
    )

    story = [
        p("C++ Smart Pointer Practice with std::unique_ptr", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 memory and references material plus the C++ temperature sensor exercise, chosen from a red C++ topic not yet covered in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Why raw owning pointers are fragile", styles, "DarkHeading"),
        p(
            "A raw pointer can point to a heap object, but it does not automatically clean that object up. If the code forgets the matching <font face=\"Courier\">delete</font>, the object leaks. If an exception or early return happens before the delete, the cleanup is skipped.",
            styles,
        ),
        code(
            """
void broken() {
    Sensor *sensor = new TemperatureSensor(9, "Server Room", 18.0);

    if (sensor->read() < 20.0) {
        return;  // leak: delete never happens
    }

    delete sensor;
}
            """,
            styles,
        ),
        p(
            "Manual ownership works only if every control path frees the object exactly once. That is easy to get wrong, especially as functions grow.",
            styles,
        ),
        p("2. RAII and automatic cleanup", styles, "DarkHeading"),
        p(
            "RAII means a resource is tied to an object whose destructor performs cleanup. In practice, you create an owning object on the stack and let scope exit destroy it automatically.",
            styles,
        ),
        code(
            """
void safe() {
    std::unique_ptr<Sensor> sensor =
        std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);

    if (sensor->read() < 20.0) {
        return;  // fine: unique_ptr destructor runs here
    }
}
            """,
            styles,
        ),
        p(
            "When the <font face=\"Courier\">std::unique_ptr</font> variable goes out of scope, it deletes the object it owns. The cleanup is attached to scope, not to a hand-written <font face=\"Courier\">delete</font> line you might forget.",
            styles,
        ),
        p("3. What <font face=\"Courier\">std::unique_ptr</font> owns", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">std::unique_ptr&lt;T&gt;</font> stores a pointer to one heap object and has unique ownership of that object. Only one unique pointer may own a given object at a time.",
            styles,
        ),
        code(
            """
std::unique_ptr<TemperatureSensor> sensor =
    std::make_unique<TemperatureSensor>(7, "Lab", 21.5);

double x = sensor->read();
            """,
            styles,
        ),
        bullets(
            [
                "Use <font face=\"Courier\">-&gt;</font> to call methods through the owned pointer.",
                "The heap object still exists separately from the <font face=\"Courier\">unique_ptr</font> variable.",
                "Destroying the <font face=\"Courier\">unique_ptr</font> destroys the owned heap object.",
            ],
            styles,
        ),
        p("4. Why it cannot be copied", styles, "DarkHeading"),
        p(
            "If copying were allowed, two owners would believe they both had sole responsibility for the same object. That would break the ownership model and could cause double deletion.",
            styles,
        ),
        code(
            """
std::unique_ptr<Sensor> a =
    std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);

std::unique_ptr<Sensor> b = a;  // error: copy is not allowed
            """,
            styles,
        ),
        p(
            "Instead, ownership is transferred with a move. After the move, the old pointer becomes empty and the new pointer is the sole owner.",
            styles,
        ),
        code(
            """
std::unique_ptr<Sensor> a =
    std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);

std::unique_ptr<Sensor> b = std::move(a);

// now a is empty, b owns the TemperatureSensor
            """,
            styles,
        ),
        p("5. Returning and passing <font face=\"Courier\">unique_ptr</font>", styles, "DarkHeading"),
        p(
            "Returning a <font face=\"Courier\">std::unique_ptr</font> from a function is normal: ownership moves out to the caller. Passing by value also transfers ownership into the function. Passing by reference borrows it without transferring ownership.",
            styles,
        ),
        code(
            """
std::unique_ptr<Sensor> make_sensor() {
    return std::make_unique<TemperatureSensor>(5, "Office", 19.0);
}

void install(std::unique_ptr<Sensor> sensor) {
    // this function now owns the sensor
}
            """,
            styles,
        ),
        p("6. Polymorphic ownership", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt;</font> can own a derived object such as <font face=\"Courier\">TemperatureSensor</font>. This lets you use runtime polymorphism while keeping clear ownership.",
            styles,
        ),
        code(
            """
std::unique_ptr<Sensor> sensor =
    std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);

double reading = sensor->read();
            """,
            styles,
        ),
        p(
            "The pointer type is <font face=\"Courier\">Sensor</font>, so client code talks to the base interface. The actual heap object is still a <font face=\"Courier\">TemperatureSensor</font>.",
            styles,
        ),
        p("7. Why the base destructor should be virtual", styles, "DarkHeading"),
        p(
            "If a derived object is destroyed through a base-class pointer type, the base class needs a virtual destructor so the full derived object is cleaned up correctly.",
            styles,
        ),
        code(
            """
class Sensor {
public:
    virtual ~Sensor() = default;
    virtual double read() const = 0;
};
            """,
            styles,
        ),
        p(
            "This matters for both raw base pointers and <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt;</font>, because deletion still happens through the base pointer type.",
            styles,
        ),
        p("8. Prefer <font face=\"Courier\">make_unique</font>", styles, "DarkHeading"),
        p(
            "Prefer <font face=\"Courier\">std::make_unique&lt;T&gt;(...)</font> over writing <font face=\"Courier\">new T(...)</font> by hand. It is shorter, clearer, and keeps the construction and ownership in one expression.",
            styles,
        ),
        code(
            """
auto sensor = std::make_unique<TemperatureSensor>(7, "Lab", 21.5);
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "A function allocates <font face=\"Courier\">new TemperatureSensor(...)</font> and has an early <font face=\"Courier\">return</font> before <font face=\"Courier\">delete</font>. Explain what goes wrong and rewrite the local owner using <font face=\"Courier\">std::unique_ptr</font>.",
                "Complete the declaration so a base-type smart pointer owns a <font face=\"Courier\">TemperatureSensor</font> created with id <font face=\"Courier\">9</font>, name <font face=\"Courier\">\"Server Room\"</font>, and temperature <font face=\"Courier\">18.0</font>.",
                "This code does not compile: <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; b = a;</font>. Replace it with a correct transfer of ownership and state what is true about <font face=\"Courier\">a</font> afterwards.",
                "Write a function header for <font face=\"Courier\">make_sensor</font> that creates a sensor inside the function and gives ownership to the caller.",
                "A function should inspect a sensor without taking ownership of it. Choose a parameter type and write the function header.",
                "A class <font face=\"Courier\">Sensor</font> is used polymorphically and objects may be destroyed through <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt;</font>. Add the destructor line the base class should contain.",
                "Trace what object is actually called in <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; sensor = std::make_unique&lt;TemperatureSensor&gt;(...); sensor-&gt;read();</font> when <font face=\"Courier\">read</font> is virtual.",
                "Rewrite <font face=\"Courier\">Sensor *sensor = new TemperatureSensor(...); delete sensor;</font> into modern C++ using <font face=\"Courier\">make_unique</font>.",
                "A function <font face=\"Courier\">install(std::unique_ptr&lt;Sensor&gt; sensor)</font> is called with a local unique pointer named <font face=\"Courier\">p</font>. Write the call so ownership moves into <font face=\"Courier\">install</font>.",
                "Choose between <font face=\"Courier\">Sensor *</font>, <font face=\"Courier\">const Sensor &#38;</font>, and <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt;</font> for these three jobs: borrow for reading, own one heap sensor, and keep a non-owning optional link to an existing sensor.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should separate ownership from borrowing and show where destruction happens.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "The raw-pointer version leaks on the early return because the <font face=\"Courier\">delete</font> is skipped. A good rewrite is <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; sensor = std::make_unique&lt;TemperatureSensor&gt;(...);</font> so scope exit performs cleanup automatically.",
                "Expected pattern: <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; sensor = std::make_unique&lt;TemperatureSensor&gt;(9, \"Server Room\", 18.0);</font>.",
                "Use a move, for example <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; b = std::move(a);</font>. Afterwards <font face=\"Courier\">a</font> no longer owns the object and should be treated as empty.",
                "A correct header is <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; make_sensor()</font> or <font face=\"Courier\">std::unique_ptr&lt;TemperatureSensor&gt; make_sensor()</font>, depending on whether the interface should expose the base or derived type.",
                "Use a borrowed parameter such as <font face=\"Courier\">const Sensor &#38;sensor</font> if only read access is needed. That does not transfer ownership.",
                "Add <font face=\"Courier\">virtual ~Sensor() = default;</font> to the base class.",
                "The owned heap object is a <font face=\"Courier\">TemperatureSensor</font>, so a virtual call dispatches to <font face=\"Courier\">TemperatureSensor::read()</font> even though the pointer type is <font face=\"Courier\">Sensor</font>.",
                "Expected pattern: <font face=\"Courier\">auto sensor = std::make_unique&lt;TemperatureSensor&gt;(...);</font> or <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt; sensor = std::make_unique&lt;TemperatureSensor&gt;(...);</font>. No manual <font face=\"Courier\">delete</font> is needed.",
                "Call the function with <font face=\"Courier\">install(std::move(p));</font> so ownership transfers into the parameter.",
                "Borrow for reading: <font face=\"Courier\">const Sensor &#38;</font>. Own one heap sensor: <font face=\"Courier\">std::unique_ptr&lt;Sensor&gt;</font>. Non-owning optional link: a raw pointer such as <font face=\"Courier\">Sensor *</font> can express nullable borrowing if lifetime is managed elsewhere.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
class Sensor {
public:
    virtual ~Sensor() = default;
    virtual double read() const = 0;
};

class TemperatureSensor : public Sensor {
    double celsius;

public:
    TemperatureSensor(int id, const std::string &name, double celsius);
    double read() const override;
};

std::unique_ptr<Sensor> sensor =
    std::make_unique<TemperatureSensor>(9, "Server Room", 18.0);

double value = sensor->read();
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
