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


OUT = Path(__file__).with_name("rust-generics-traits-study-pack.pdf")


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
        title="Rust Generics and Traits Study Pack",
    )

    story = [
        p("Rust Generics and Traits", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 Rust Lecture 07 Generics and Traits, chosen from a red Rust topic not yet covered in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Why generics exist", styles, "DarkHeading"),
        p(
            "Generics let you write one piece of logic and leave one or more types as parameters. Rust then checks and specialises the code for the concrete types you actually use.",
            styles,
        ),
        code(
            """
fn first_i32(values: &[i32]) -> Option<&i32> {
    values.get(0)
}

fn first_char(values: &[char]) -> Option<&char> {
    values.get(0)
}

fn first<T>(values: &[T]) -> Option<&T> {
    values.get(0)
}
            """,
            styles,
        ),
        p(
            "The generic version avoids duplicated code, but Rust still type-checks it. You cannot call methods or operators on a generic type unless the function says that type supports them.",
            styles,
        ),
        p("2. Generic functions and trait bounds", styles, "DarkHeading"),
        p(
            "A trait bound says what a generic type must be able to do. If the body compares values, the type must support comparison. If the body prints with normal braces, the type must support display formatting.",
            styles,
        ),
        code(
            """
fn larger<T: PartialOrd>(a: T, b: T) -> T {
    if a > b {
        a
    } else {
        b
    }
}

fn show_larger<T: PartialOrd + std::fmt::Display>(a: T, b: T) {
    let result = larger(a, b);
    println!("larger = {result}");
}
            """,
            styles,
        ),
        p(
            "Here, <font face=\"Courier\">PartialOrd</font> allows comparison with <font face=\"Courier\">&gt;</font>, and <font face=\"Courier\">Display</font> allows formatting with normal braces.",
            styles,
        ),
        p("3. Generic structs and methods", styles, "DarkHeading"),
        p(
            "A generic struct can store values whose type is not fixed until use. One type parameter means the fields using that parameter must share the same concrete type. Use two parameters if the fields may have different types.",
            styles,
        ),
        code(
            """
struct Point<T> {
    x: T,
    y: T,
}

struct Pair<T, U> {
    left: T,
    right: U,
}

let same = Point { x: 3, y: 4 };
let mixed = Pair { left: 3, right: 4.5 };
            """,
            styles,
        ),
        p(
            "When implementing methods for a generic struct, the <font face=\"Courier\">impl</font> block must introduce the type parameter.",
            styles,
        ),
        code(
            """
impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}
            """,
            styles,
        ),
        p("4. Traits", styles, "DarkHeading"),
        p(
            "A trait defines shared behaviour. A type implements the trait by providing the required methods. This is how generic code can say it accepts any type with a particular capability.",
            styles,
        ),
        code(
            """
trait Area {
    fn area(&self) -> f64;
}

struct Rectangle {
    width: f64,
    height: f64,
}

impl Area for Rectangle {
    fn area(&self) -> f64 {
        self.width * self.height
    }
}
            """,
            styles,
        ),
        p(
            "A trait can also provide a default method body. Types use the default unless their implementation overrides it.",
            styles,
        ),
        code(
            """
trait Area {
    fn area(&self) -> f64;

    fn is_large(&self) -> bool {
        self.area() > 100.0
    }
}
            """,
            styles,
        ),
        p("5. Trait bounds in function parameters", styles, "DarkHeading"),
        p(
            "Trait bounds let a function accept many concrete types while still knowing what operations are valid inside the function body.",
            styles,
        ),
        code(
            """
fn print_area<T: Area>(shape: &T) {
    println!("{}", shape.area());
}

fn print_area_short(shape: &impl Area) {
    println!("{}", shape.area());
}
            """,
            styles,
        ),
        p(
            "Both versions accept any borrowed value whose type implements <font face=\"Courier\">Area</font>. The explicit generic form is more flexible when one type parameter must appear in multiple places.",
            styles,
        ),
        p("6. Where clauses", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">where</font> clause moves long trait bounds after the parameter list. It means the same thing, but is usually easier to read when there are several bounds.",
            styles,
        ),
        code(
            """
use std::fmt::Display;

fn compare_and_print<T, U>(left: T, right: U)
where
    T: Display + PartialOrd,
    U: Display,
{
    println!("left = {left}, right = {right}");
}
            """,
            styles,
        ),
        p("7. Derive macros", styles, "DarkHeading"),
        p(
            "Some common traits can be generated automatically with <font face=\"Courier\">derive</font>. This is common for debugging, testing, cloning, equality checks, and map keys.",
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">Debug</font>: allows debug printing with <font face=\"Courier\">{:?}</font>.",
                "<font face=\"Courier\">Clone</font>: allows explicit cloning with <font face=\"Courier\">.clone()</font>.",
                "<font face=\"Courier\">PartialEq</font>: allows equality checks with <font face=\"Courier\">==</font> and <font face=\"Courier\">!=</font>.",
                "<font face=\"Courier\">Eq</font> and <font face=\"Courier\">Hash</font>: commonly needed for custom <font face=\"Courier\">HashMap</font> keys.",
            ],
            styles,
        ),
        code(
            """
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Team {
    name: String,
}

let mut scores = HashMap::new();
scores.insert(Team { name: String::from("Exeter") }, 3);
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Turn the two functions <font face=\"Courier\">first_i32</font> and <font face=\"Courier\">first_char</font> into one generic <font face=\"Courier\">first</font> function that works on a borrowed slice.",
                "Fix a <font face=\"Courier\">Point</font> definition so <font face=\"Courier\">Point { x: 3, y: 4.5 }</font> compiles without changing the values.",
                "Complete an <font face=\"Courier\">impl</font> block for <font face=\"Courier\">Point</font> so method <font face=\"Courier\">x</font> returns a borrowed reference to the x field.",
                "Given a <font face=\"Courier\">Rectangle</font> with width and height, define an <font face=\"Courier\">Area</font> trait and implement it for <font face=\"Courier\">Rectangle</font>.",
                "Add a default method to the <font face=\"Courier\">Area</font> trait that returns true when the area is bigger than 100.",
                "Write a function that borrows any value implementing <font face=\"Courier\">Area</font> and prints its area.",
                "Fix the signature of a generic <font face=\"Courier\">show_larger</font> function whose body uses <font face=\"Courier\">a &gt; b</font> and then prints the winning value with normal braces.",
                "Rewrite a generic function signature with two long bounds into a <font face=\"Courier\">where</font> clause.",
                "A test uses <font face=\"Courier\">assert_eq!(a, b)</font> on a custom struct and also prints it with debug formatting. Add the needed derives.",
                "A custom <font face=\"Courier\">Team</font> struct is used as a <font face=\"Courier\">HashMap</font> key. Add the usual derives that make this work.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should compile and show the correct trait bounds rather than just naming the concept.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "Expected pattern: <font face=\"Courier\">fn first&lt;T&gt;(values: &#38;[T]) -&gt; Option&lt;&#38;T&gt; { values.get(0) }</font>.",
                "Use two type parameters, for example <font face=\"Courier\">struct Point&lt;T, U&gt; { x: T, y: U }</font>. A single <font face=\"Courier\">T</font> would force both fields to have the same type.",
                "Expected pattern: <font face=\"Courier\">impl&lt;T&gt; Point&lt;T&gt; { fn x(&#38;self) -&gt; &#38;T { &#38;self.x } }</font>.",
                "A valid answer defines <font face=\"Courier\">trait Area { fn area(&#38;self) -&gt; f64; }</font> and implements it for <font face=\"Courier\">Rectangle</font> by returning width times height.",
                "Add a method with a body inside the trait, for example <font face=\"Courier\">fn is_large(&#38;self) -&gt; bool { self.area() &gt; 100.0 }</font>.",
                "Expected pattern: <font face=\"Courier\">fn print_area&lt;T: Area&gt;(shape: &#38;T) { println!(\"{}\", shape.area()); }</font>. <font face=\"Courier\">&#38;impl Area</font> is also valid for this simple case.",
                "The type needs both comparison and display formatting bounds, for example <font face=\"Courier\">T: PartialOrd + std::fmt::Display</font>.",
                "Move the bounds after <font face=\"Courier\">where</font>, for example <font face=\"Courier\">fn f&lt;T, U&gt;(x: T, y: U) where T: Display + PartialOrd, U: Display { ... }</font>.",
                "Use <font face=\"Courier\">#[derive(Debug, PartialEq)]</font>. <font face=\"Courier\">assert_eq!</font> needs equality and debug output for failure messages.",
                "Use <font face=\"Courier\">#[derive(Debug, Clone, PartialEq, Eq, Hash)]</font> or at least <font face=\"Courier\">PartialEq</font>, <font face=\"Courier\">Eq</font>, and <font face=\"Courier\">Hash</font> for map-key behaviour.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
use std::fmt::Display;

fn larger<T: PartialOrd>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

trait Area {
    fn area(&self) -> f64;

    fn is_large(&self) -> bool {
        self.area() > 100.0
    }
}

fn print_area<T>(shape: &T)
where
    T: Area,
{
    println!("{}", shape.area());
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Team {
    name: String,
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
