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


OUT = Path(__file__).with_name("rust-collections-data-modelling-study-pack.pdf")


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
        title="Rust Collections and Data Modelling Study Pack",
    )

    story = [
        p("Rust Collections and Data Modelling", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 Rust Lecture 04, chosen from a red Rust topic in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. <font face=\"Courier\">String</font> and <font face=\"Courier\">&#38;str</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">String</font> is owned, heap-allocated, and growable. <font face=\"Courier\">&#38;str</font> is a borrowed string slice: a view into text owned somewhere else. For read-only function parameters, prefer <font face=\"Courier\">&#38;str</font> because it accepts both string literals and borrowed <font face=\"Courier\">String</font> values.",
            styles,
        ),
        code(
            """
fn count_letters(text: &str) -> usize {
    text.chars().count()
}

let literal = "hello";
let owned = String::from("world");

println!("{}", count_letters(literal));
println!("{}", count_letters(&owned));
            """,
            styles,
        ),
        p("Use <font face=\"Courier\">push</font> for one character and <font face=\"Courier\">push_str</font> for a string slice:", styles),
        code(
            """
let mut text = String::from("Hi");
text.push('!');
text.push_str(" there");
            """,
            styles,
        ),
        p("2. <font face=\"Courier\">Vec&lt;T&gt;</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">Vec&lt;T&gt;</font> is Rust's growable array. All elements have the same type. Use <font face=\"Courier\">Vec::new()</font> for an empty vector, <font face=\"Courier\">vec![]</font> for initial values, <font face=\"Courier\">push</font> to add to the end, and <font face=\"Courier\">pop</font> to remove from the end.",
            styles,
        ),
        code(
            """
let mut scores = Vec::new();
scores.push(10);
scores.push(20);

let mut names = vec!["Ada", "Grace", "Linus"];
names.push("Ken");
            """,
            styles,
        ),
        p("Indexing with square brackets can panic if the index is out of range. <font face=\"Courier\">get</font> returns <font face=\"Courier\">Option&lt;&#38;T&gt;</font>, which forces you to handle missing values.", styles),
        code(
            """
let values = vec![4, 8, 15];

println!("{}", values[1]);       // 8

match values.get(10) {
    Some(value) => println!("{value}"),
    None => println!("no value at that index"),
}
            """,
            styles,
        ),
        p("Iterate by reference when you want to read without taking ownership:", styles),
        code(
            """
for value in &values {
    println!("{value}");
}
            """,
            styles,
        ),
        p("3. Structs", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">struct</font> groups related fields into one named type. Fields have names and types. The whole binding must be <font face=\"Courier\">mut</font> if you want to change any field.",
            styles,
        ),
        code(
            """
struct Student {
    name: String,
    mark: u32,
}

let mut student = Student {
    name: String::from("Amina"),
    mark: 72,
};

student.mark = 75;
            """,
            styles,
        ),
        p("Field init shorthand is used when a variable has the same name as the field. Update syntax copies or moves the remaining fields from another value and must come last.", styles),
        code(
            """
fn make_student(name: String, mark: u32) -> Student {
    Student { name, mark }
}

let first = make_student(String::from("Sam"), 64);
let second = Student {
    mark: 70,
    ..first
};
            """,
            styles,
        ),
        p("4. Methods and associated functions", styles, "DarkHeading"),
        p(
            "Methods live in an <font face=\"Courier\">impl</font> block. A method with <font face=\"Courier\">&#38;self</font> reads the value, <font face=\"Courier\">&#38;mut self</font> changes it, and <font face=\"Courier\">self</font> takes ownership. Associated functions do not take <font face=\"Courier\">self</font>; they are often used as constructors such as <font face=\"Courier\">new</font>.",
            styles,
        ),
        code(
            """
struct Counter {
    value: u32,
}

impl Counter {
    fn new() -> Self {
        Self { value: 0 }
    }

    fn get(&self) -> u32 {
        self.value
    }

    fn increment(&mut self) {
        self.value += 1;
    }
}
            """,
            styles,
        ),
        p("5. Enums", styles, "DarkHeading"),
        p(
            "An <font face=\"Courier\">enum</font> defines a type with a fixed set of variants. Variants can be simple names or can carry data. Use <font face=\"Courier\">::</font> to name a variant.",
            styles,
        ),
        code(
            """
enum Direction {
    North,
    South,
    East,
    West,
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}
            """,
            styles,
        ),
        p("6. <font face=\"Courier\">Option&lt;T&gt;</font>, <font face=\"Courier\">match</font>, and <font face=\"Courier\">if let</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">Option&lt;T&gt;</font> represents a value that might be missing. It has two variants: <font face=\"Courier\">Some(value)</font> and <font face=\"Courier\">None</font>. This is Rust's standard null-free pattern.",
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">match</font> is exhaustive, so all possible variants must be handled.",
                "<font face=\"Courier\">Some(value)</font> in a pattern extracts the inner value.",
                "<font face=\"Courier\">_</font> is a catch-all pattern, like a default case.",
                "<font face=\"Courier\">if let</font> is shorter when you only care about one pattern.",
            ],
            styles,
        ),
        code(
            """
fn describe(score: Option<u32>) {
    match score {
        Some(value) => println!("score = {value}"),
        None => println!("missing score"),
    }
}

let last = vec![10, 20, 30].pop();
if let Some(value) = last {
    println!("removed {value}");
}
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Choose a parameter type for a function that only reads text and should accept both <font face=\"Courier\">String</font> values and string literals. Show both calls.",
                "Starting from <font face=\"Courier\">let mut text = String::from(\"Hi\");</font>, write the two lines that produce <font face=\"Courier\">Hi! there</font>.",
                "Create a mutable <font face=\"Courier\">Vec&lt;i32&gt;</font>, push <font face=\"Courier\">3</font> and <font face=\"Courier\">7</font>, then remove the last value.",
                "Explain the difference between <font face=\"Courier\">v[10]</font> and <font face=\"Courier\">v.get(10)</font> when the vector is too short.",
                "Write a loop that prints every value in <font face=\"Courier\">Vec&lt;i32&gt;</font> without taking ownership of the vector.",
                "Define a <font face=\"Courier\">Book</font> struct with <font face=\"Courier\">title: String</font> and <font face=\"Courier\">pages: u32</font>, then instantiate one value.",
                "Write a constructor-style associated function <font face=\"Courier\">Book::new</font> that returns <font face=\"Courier\">Self</font>.",
                "Explain the difference between a method taking <font face=\"Courier\">&#38;self</font> and one taking <font face=\"Courier\">&#38;mut self</font>.",
                "Define an enum <font face=\"Courier\">TrafficLight</font> with three variants, then write a <font face=\"Courier\">match</font> that prints a message for each.",
                "Use <font face=\"Courier\">match</font> to handle <font face=\"Courier\">Option&lt;i32&gt;</font>, printing the number for <font face=\"Courier\">Some</font> and <font face=\"Courier\">missing</font> for <font face=\"Courier\">None</font>.",
                "Rewrite the previous answer with <font face=\"Courier\">if let</font> for the <font face=\"Courier\">Some</font> case and <font face=\"Courier\">else</font> for everything else.",
                "Why is <font face=\"Courier\">Option&lt;T&gt;</font> safer than using null pointers for missing values?",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Good answers should show ownership-aware collection use and exhaustive pattern handling.", styles, "SourceText"),
        numbered(
            [
                "Use <font face=\"Courier\">&#38;str</font>. A string literal passes directly, and a <font face=\"Courier\">String</font> is passed as a borrow, for example <font face=\"Courier\">f(\"hi\")</font> and <font face=\"Courier\">f(&#38;name)</font>.",
                "Use <font face=\"Courier\">text.push('!');</font> and <font face=\"Courier\">text.push_str(\" there\");</font>.",
                "Expected pattern: <font face=\"Courier\">let mut v = Vec::new(); v.push(3); v.push(7); let last = v.pop();</font>. The removed value has type <font face=\"Courier\">Option&lt;i32&gt;</font>.",
                "<font face=\"Courier\">v[10]</font> panics if index 10 does not exist. <font face=\"Courier\">v.get(10)</font> returns <font face=\"Courier\">None</font>, so the missing case can be handled.",
                "Expected pattern: <font face=\"Courier\">for value in &#38;v { println!(\"{value}\"); }</font>. Borrowing keeps the vector usable after the loop.",
                "A valid answer defines <font face=\"Courier\">struct Book { title: String, pages: u32 }</font> and creates <font face=\"Courier\">Book { title: String::from(\"...\"), pages: ... }</font>.",
                "Expected pattern: <font face=\"Courier\">impl Book { fn new(title: String, pages: u32) -&gt; Self { Self { title, pages } } }</font>.",
                "<font face=\"Courier\">&#38;self</font> borrows immutably and can read fields. <font face=\"Courier\">&#38;mut self</font> borrows mutably and can change fields.",
                "A valid enum has variants such as <font face=\"Courier\">Red</font>, <font face=\"Courier\">Amber</font>, and <font face=\"Courier\">Green</font>. A correct <font face=\"Courier\">match</font> handles all three variants.",
                "Expected pattern: <font face=\"Courier\">match x { Some(n) =&gt; println!(\"{n}\"), None =&gt; println!(\"missing\") }</font>.",
                "Expected pattern: <font face=\"Courier\">if let Some(n) = x { println!(\"{n}\"); } else { println!(\"missing\"); }</font>.",
                "<font face=\"Courier\">Option&lt;T&gt;</font> makes absence explicit in the type system. Code must handle <font face=\"Courier\">Some</font> and <font face=\"Courier\">None</font> instead of accidentally dereferencing a missing value.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
struct Book {
    title: String,
    pages: u32,
}

impl Book {
    fn new(title: String, pages: u32) -> Self {
        Self { title, pages }
    }

    fn is_long(&self) -> bool {
        self.pages > 300
    }
}

fn print_first(values: &[i32]) {
    match values.get(0) {
        Some(value) => println!("first = {value}"),
        None => println!("empty"),
    }
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
