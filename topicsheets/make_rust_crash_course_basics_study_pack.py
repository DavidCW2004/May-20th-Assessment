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


OUT = Path(__file__).with_name("rust-crash-course-basics-study-pack.pdf")


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
        title="Rust Crash-course Basics Study Pack",
    )

    story = [
        p("Rust Crash-course Basics", styles, "TopicTitle"),
        p(
            "Focused revision sheet for the RAG item: let, mut, shadowing, const, integer types, tuples, arrays, runtime bounds checks, and printing.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. <font face=\"Courier\">main</font> and printing", styles, "DarkHeading"),
        p(
            "A Rust executable starts in <font face=\"Courier\">fn main()</font>. Use <font face=\"Courier\">println!</font> for formatted output. The exclamation mark means it is a macro.",
            styles,
        ),
        code(
            """
fn main() {
    println!("hello");
    let name = "Ada";
    println!("name = {name}");
    println!("2 + 3 = {}", 2 + 3);
}
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">{name}</font> prints a variable by name.",
                "<font face=\"Courier\">{}</font> prints the next argument.",
                "<font face=\"Courier\">{:?}</font> uses debug formatting.",
            ],
            styles,
        ),
        p("2. <font face=\"Courier\">let</font> and immutability", styles, "DarkHeading"),
        p(
            "Variables are immutable by default. That means you cannot assign a new value to them unless you use <font face=\"Courier\">mut</font>.",
            styles,
        ),
        code(
            """
let score = 10;
// score = 11;  // error: score is immutable

let mut count = 0;
count += 1;
            """,
            styles,
        ),
        p(
            "Use immutability as the default. Add <font face=\"Courier\">mut</font> only when the variable really changes.",
            styles,
        ),
        p("3. Shadowing is not mutation", styles, "DarkHeading"),
        p(
            "Shadowing creates a new variable with the same name. This is different from changing an existing variable.",
            styles,
        ),
        code(
            """
let text = "42";
let text = text.parse::<i32>().unwrap();
let text = text + 1;

println!("{text}");  // 43
            """,
            styles,
        ),
        p(
            "Shadowing can also change the type. Mutation cannot change a variable's type after it has been inferred.",
            styles,
        ),
        code(
            """
let mut value = 10;
// value = "hello";  // error: value is already an integer
            """,
            styles,
        ),
        p("4. <font face=\"Courier\">const</font>", styles, "DarkHeading"),
        p(
            "Constants are always immutable, must have an explicit type annotation, and are usually named in capitals.",
            styles,
        ),
        code(
            """
const MAX_STUDENTS: usize = 200;

fn main() {
    println!("{MAX_STUDENTS}");
}
            """,
            styles,
        ),
        p(
            "Use <font face=\"Courier\">const</font> for values that are fixed for the whole program, not for ordinary local variables.",
            styles,
        ),
        p("5. Integer and floating-point types", styles, "DarkHeading"),
        p(
            "Rust has explicit numeric types. Common integer types include <font face=\"Courier\">i32</font>, <font face=\"Courier\">u32</font>, <font face=\"Courier\">usize</font>, and <font face=\"Courier\">i64</font>. Common floating-point types are <font face=\"Courier\">f32</font> and <font face=\"Courier\">f64</font>.",
            styles,
        ),
        code(
            """
let a: i32 = -10;
let b: u32 = 10;
let index: usize = 3;
let average: f64 = 12.5;
            """,
            styles,
        ),
        bullets(
            [
                "Signed integers such as <font face=\"Courier\">i32</font> can be negative.",
                "Unsigned integers such as <font face=\"Courier\">u32</font> cannot be negative.",
                "<font face=\"Courier\">usize</font> is commonly used for indexes and lengths.",
                "Rust does not silently mix all numeric types; conversions often need to be explicit.",
            ],
            styles,
        ),
        p("6. Tuples", styles, "DarkHeading"),
        p(
            "A tuple groups a fixed number of values, and the values can have different types.",
            styles,
        ),
        code(
            """
let item = ("apple", 3, 0.75);

let name = item.0;
let quantity = item.1;
let price = item.2;

let (name, quantity, price) = item;
            """,
            styles,
        ),
        p(
            "Use dot indexes such as <font face=\"Courier\">.0</font> and <font face=\"Courier\">.1</font>, or destructure the tuple into named variables.",
            styles,
        ),
        p("7. Arrays", styles, "DarkHeading"),
        p(
            "An array has a fixed length and every element has the same type. The length is part of the array type.",
            styles,
        ),
        code(
            """
let values = [10, 20, 30];
let first = values[0];

let zeros: [i32; 5] = [0; 5];

println!("{first}");
println!("{:?}", zeros);
            """,
            styles,
        ),
        p(
            "Use arrays for fixed-size data. Use <font face=\"Courier\">Vec&lt;T&gt;</font> when the length needs to grow or change at runtime.",
            styles,
        ),
        p("8. Runtime bounds checks", styles, "DarkHeading"),
        p(
            "Rust checks array and vector indexing at runtime. If an index is out of bounds, the program panics instead of reading invalid memory.",
            styles,
        ),
        code(
            """
let values = [10, 20, 30];

println!("{}", values[2]);  // ok
// println!("{}", values[3]);  // panic: index out of bounds
            """,
            styles,
        ),
        p(
            "When an index may be missing, use <font face=\"Courier\">get</font>, which returns <font face=\"Courier\">Option</font>.",
            styles,
        ),
        code(
            """
match values.get(3) {
    Some(value) => println!("{value}"),
    None => println!("missing index"),
}
            """,
            styles,
        ),
        p("9. Expressions and semicolons", styles, "DarkHeading"),
        p(
            "Many Rust blocks are expressions. A final expression without a semicolon becomes the value of the block or function.",
            styles,
        ),
        code(
            """
fn add_one(x: i32) -> i32 {
    x + 1
}

let size = if add_one(2) > 3 {
    "large"
} else {
    "small"
};
            """,
            styles,
        ),
        p(
            "Adding a semicolon to <font face=\"Courier\">x + 1</font> would turn it into a statement, so the function would no longer return the expected <font face=\"Courier\">i32</font>.",
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Write a minimal Rust <font face=\"Courier\">main</font> that prints a variable using named formatting.",
                "Given <font face=\"Courier\">let x = 5; x += 1;</font>, explain the error and fix it.",
                "Show shadowing that converts the string <font face=\"Courier\">\"12\"</font> into an <font face=\"Courier\">i32</font> and then adds one.",
                "Write a constant called <font face=\"Courier\">MAX_USERS</font> with type <font face=\"Courier\">usize</font> and value <font face=\"Courier\">100</font>.",
                "Choose suitable types for a negative temperature, an array index, and a decimal average.",
                "Create a tuple holding a name, age, and height, then read the age using tuple indexing.",
                "Create an array of three integers and print it with debug formatting.",
                "Explain what happens when code indexes an array outside its length.",
                "Rewrite an unsafe direct index as a <font face=\"Courier\">get</font> plus <font face=\"Courier\">match</font>.",
                "Explain why <font face=\"Courier\">fn f() -&gt; i32 { 5 }</font> works but <font face=\"Courier\">fn f() -&gt; i32 { 5; }</font> does not.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Strong answers should mention Rust's default immutability and runtime bounds checks.", styles, "SourceText"),
        numbered(
            [
                "Expected pattern: <font face=\"Courier\">fn main() { let name = \"Ada\"; println!(\"{name}\"); }</font>.",
                "<font face=\"Courier\">x</font> is immutable. Fix with <font face=\"Courier\">let mut x = 5;</font> before <font face=\"Courier\">x += 1</font>.",
                "Expected: <font face=\"Courier\">let value = \"12\"; let value = value.parse::&lt;i32&gt;().unwrap(); let value = value + 1;</font>.",
                "Expected: <font face=\"Courier\">const MAX_USERS: usize = 100;</font>.",
                "Example: <font face=\"Courier\">i32</font> for negative temperature, <font face=\"Courier\">usize</font> for index, <font face=\"Courier\">f64</font> for decimal average.",
                "Expected: create something like <font face=\"Courier\">let person = (\"Ada\", 20, 1.70);</font> and read <font face=\"Courier\">person.1</font>.",
                "Expected: <font face=\"Courier\">let values = [1, 2, 3]; println!(\"{:?}\", values);</font>.",
                "Rust panics at runtime rather than reading outside the array.",
                "Expected: <font face=\"Courier\">match values.get(i) { Some(v) =&gt; ..., None =&gt; ... }</font>.",
                "The first has final expression <font face=\"Courier\">5</font>. The second has statement <font face=\"Courier\">5;</font>, which returns unit <font face=\"Courier\">()</font>, not <font face=\"Courier\">i32</font>.",
            ],
            styles,
        ),
        p("Common Mistakes", styles, "BlueHeading"),
        bullets(
            [
                "Forgetting <font face=\"Courier\">mut</font> before assigning to a variable again.",
                "Calling shadowing the same thing as mutation.",
                "Using array indexing when <font face=\"Courier\">get</font> would be safer for a possibly missing index.",
                "Forgetting that <font face=\"Courier\">println!</font> is a macro, not a normal function.",
                "Adding a semicolon to the final value of a function that is meant to return that value.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
