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

OUT = Path(__file__).with_name("rust-expressions-statements-study-pack.pdf")


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
        bulletType="bullet", leftIndent=6 * mm, bulletFontName="Helvetica", bulletFontSize=7,
    )


def numbered(items, styles, start=1):
    return ListFlowable(
        [ListItem(p(item, styles), leftIndent=5 * mm) for item in items],
        bulletType="1", leftIndent=7 * mm, bulletFontName="Helvetica-Bold", bulletFontSize=8, start=start,
    )


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm,
        title="Rust Expressions and Statements Study Pack",
    )

    story = [
        p("Rust: Expressions vs Statements", styles, "TopicTitle"),
        p(
            "Based on ECM2433 rust_02_crash_course slides and Worksheet 1. "
            "Covers the expression/statement distinction, how semicolons affect return values, "
            "blocks as expressions, if as an expression, functions with implicit returns, "
            "the unit type, and loop returning a value.",
            styles, "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),

        p("1. Statements and expressions", styles, "DarkHeading"),
        p(
            "<b>Statements</b> perform an action and do not produce a value. "
            "<b>Expressions</b> evaluate to a value. "
            "In Rust, adding a semicolon to the end of an expression turns it into a statement "
            "— it discards the value and produces the unit type "
            "<font face=\"Courier\">()</font> instead.",
            styles,
        ),
        code(
            """
let x = 5;        // statement: let binding, no value produced
x + 1             // expression: evaluates to 6
x + 1;            // now a statement: value discarded, produces ()
            """,
            styles,
        ),

        p("2. Blocks are expressions", styles, "DarkHeading"),
        p(
            "A block <font face=\"Courier\">{ ... }</font> is itself an expression. "
            "Its value is the final expression inside it. "
            "If the last line ends with a semicolon, the block evaluates to "
            "<font face=\"Courier\">()</font>.",
            styles,
        ),
        code(
            """
let y = {
    let x = 3;
    x + 1          // no semicolon: block evaluates to 4
};                 // y is 4

let z = {
    let x = 3;
    x + 1;         // semicolon: block evaluates to ()
};                 // z is ()
            """,
            styles,
        ),

        p("3. Functions return their final expression", styles, "DarkHeading"),
        p(
            "A function's return value is the value of its final expression. "
            "No <font face=\"Courier\">return</font> keyword is needed. "
            "Adding a semicolon to the last line changes the return type to "
            "<font face=\"Courier\">()</font>, which causes a compile error if the "
            "function declares a non-unit return type.",
            styles,
        ),
        code(
            """
fn add(x: i32, y: i32) -> i32 {
    x + y          /* implicit return: no semicolon */
}

fn broken(x: i32) -> i32 {
    x + 10;        /* semicolon: returns () — compile error! */
}
            """,
            styles,
        ),
        p(
            "This is the exact error shown in Worksheet 1, section 1.3: "
            "<font face=\"Courier\">fn add_ten(x: i32) -> i32 { x + 10; }</font> "
            "reports \"mismatched types: expected i32, found ()\".",
            styles,
        ),

        p("4. if is an expression", styles, "DarkHeading"),
        p(
            "An <font face=\"Courier\">if</font> block evaluates to a value. "
            "All branches must return the same type. "
            "This lets you write conditional assignments as a single "
            "<font face=\"Courier\">let</font> binding.",
            styles,
        ),
        code(
            """
let number = 5;

/* if used as an expression */
let description = if number > 0 {
    "positive"
} else if number < 0 {
    "negative"
} else {
    "zero"
};

/* all branches must return the same type */
let bad = if number > 0 { 1 } else { "oops" }; /* compile error */
            """,
            styles,
        ),

        p("5. loop can return a value", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">loop</font> block is also an expression. "
            "Use <font face=\"Courier\">break value;</font> to exit the loop "
            "and produce a value.",
            styles,
        ),
        code(
            """
let mut counter = 0;
let result = loop {
    counter += 1;
    if counter == 10 {
        break counter * 2;   /* loop evaluates to 20 */
    }
};                           /* result is 20 */
            """,
            styles,
        ),

        p("6. The unit type ()", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">()</font> is the unit type. "
            "Functions with no <font face=\"Courier\">-&#62;</font> annotation return "
            "<font face=\"Courier\">()</font> implicitly. "
            "Writing <font face=\"Courier\">-&#62; ()</font> is valid but rarely needed.",
            styles,
        ),
        code(
            """
fn greet() {                /* implicitly returns () */
    println!("hello");
}

fn explicit_unit() -> () {  /* same thing, explicit */
    println!("hello");
}
            """,
            styles,
        ),

        p("Practice Questions", styles, "BlueHeading"),
        p("Question 1 — this function fails to compile:", styles),
        code(
            """
fn add_ten(x: i32) -> i32 {
    x + 10;
}
            """,
            styles,
        ),
        numbered(
            [
                "Identify the error and write the corrected function.",
                "What type does <font face=\"Courier\">z</font> have? "
                "<font face=\"Courier\">let z = { let x = 3; x + 1; };</font>",
            ],
            styles,
        ),
        p("Question 3 — state what this prints:", styles),
        code(
            """
let x = {
    let a = 5;
    let b = 3;
    a + b
};
println!("{}", x);
            """,
            styles,
        ),
        numbered(
            [
                "State what the code above prints.",
                "Write <font face=\"Courier\">fn larger(a: i32, b: i32) -&#62; i32</font> "
                "that returns the larger value. Use "
                "<font face=\"Courier\">if</font> as an expression with no explicit "
                "<font face=\"Courier\">return</font> keyword.",
            ],
            styles, start=3,
        ),
        p("Question 5 — this function does not compile:", styles),
        code(
            """
fn classify(score: i32) -> &'static str {
    if score >= 70 {
        "distinction"
    } else if score >= 50 {
        "pass"
    } else {
        0   /* wrong type */
    }
}
            """,
            styles,
        ),
        numbered(
            [
                "Explain why it does not compile and write a corrected version that "
                "returns <font face=\"Courier\">\"fail\"</font> for scores below 50.",
            ],
            styles, start=5,
        ),
        p("Question 6 — state what this prints:", styles),
        code(
            """
fn double(x: i32) -> i32 { x * 2 }

fn main() {
    let a = double(4);
    let b = {
        let n = double(3);
        n + 1
    };
    println!("{} {}", a, b);
}
            """,
            styles,
        ),
        numbered(
            [
                "State what the program above prints.",
                "What is the return type of a function declared as "
                "<font face=\"Courier\">fn greet(name: &#38;str)</font> with no "
                "<font face=\"Courier\">-&#62;</font> annotation? "
                "What would happen if you wrote "
                "<font face=\"Courier\">let x: i32 = greet(\"Alice\");</font>?",
            ],
            styles, start=6,
        ),
        p("Question 8 — state the value of result:", styles),
        code(
            """
let mut n = 1;
let result = loop {
    n *= 2;
    if n > 1000 {
        break n;
    }
};
            """,
            styles,
        ),
        numbered(
            [
                "State the value of <font face=\"Courier\">result</font>.",
            ],
            styles, start=8,
        ),
        p("Question 9 — rewrite this using if as an expression:", styles),
        code(
            """
let label;
if temperature > 100.0 {
    label = "hot";
} else {
    label = "cool";
}
            """,
            styles,
        ),
        numbered(
            [
                "Rewrite the code above as a single "
                "<font face=\"Courier\">let</font> binding.",
                "Write <font face=\"Courier\">fn sign(n: i32) -&#62; &#38;'static str</font> "
                "that returns <font face=\"Courier\">\"positive\"</font>, "
                "<font face=\"Courier\">\"negative\"</font>, or "
                "<font face=\"Courier\">\"zero\"</font> using "
                "<font face=\"Courier\">if/else if/else</font> as a single expression "
                "with no <font face=\"Courier\">return</font> keyword.",
            ],
            styles, start=9,
        ),

        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "The semicolon on <font face=\"Courier\">x + 10;</font> turns the expression "
                "into a statement returning <font face=\"Courier\">()</font>, but the function "
                "declares <font face=\"Courier\">-&#62; i32</font>. "
                "Fix: remove the semicolon: <font face=\"Courier\">fn add_ten(x: i32) -&#62; i32 { x + 10 }</font>",

                "<font face=\"Courier\">()</font> — the semicolon discards the value of "
                "<font face=\"Courier\">x + 1</font>.",

                "Prints <font face=\"Courier\">8</font> — the block evaluates to "
                "<font face=\"Courier\">5 + 3 = 8</font> (no semicolon on last line).",

                "<font face=\"Courier\">fn larger(a: i32, b: i32) -&#62; i32 { if a &gt; b { a } else { b } }</font>",

                "The final branch returns <font face=\"Courier\">0</font> (integer) while "
                "the other branches return <font face=\"Courier\">&amp;str</font> — all "
                "branches of an if expression must return the same type. "
                "Fix the last branch to return "
                "<font face=\"Courier\">\"fail\"</font>.",

                "Prints <font face=\"Courier\">8 7</font>. "
                "<font face=\"Courier\">double(4)</font> = 8. "
                "Block: <font face=\"Courier\">n = double(3) = 6</font>, then "
                "<font face=\"Courier\">n + 1 = 7</font>.",

                "Return type is <font face=\"Courier\">()</font>. "
                "<font face=\"Courier\">let x: i32 = greet(\"Alice\");</font> would not "
                "compile because the function returns <font face=\"Courier\">()</font>, "
                "not <font face=\"Courier\">i32</font>.",

                "1024 — the loop doubles n each iteration (2, 4, 8, …, 512, 1024) and "
                "breaks when n exceeds 1000.",

                "<font face=\"Courier\">let label = if temperature &gt; 100.0 { \"hot\" } else { \"cool\" };</font>",

                "<font face=\"Courier\">fn sign(n: i32) -&#62; &amp;'static str { if n &gt; 0 { \"positive\" } else if n &lt; 0 { \"negative\" } else { \"zero\" } }</font>",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
