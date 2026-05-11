from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, Preformatted, SimpleDocTemplate


OUT = Path(__file__).with_name("rust-ownership-closures-lifetimes-study-pack.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TopicTitle", parent=styles["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#111827"), spaceAfter=8))
    styles.add(ParagraphStyle("TopicBody", parent=styles["Normal"], fontSize=9.3, leading=12, textColor=colors.HexColor("#111827"), spaceAfter=6))
    styles.add(ParagraphStyle("SourceText", parent=styles["Normal"], fontSize=8, leading=10, textColor=colors.HexColor("#4b5563"), spaceAfter=6))
    styles.add(ParagraphStyle("BlueHeading", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#1d4ed8"), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle("DarkHeading", parent=styles["Heading3"], fontSize=11, leading=13, textColor=colors.HexColor("#111827"), spaceBefore=6, spaceAfter=3))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.25, leading=8.8, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=7))
    return styles


def p(text, styles, style="TopicBody"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=88)


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
        title="Rust Ownership, Closures, Lifetimes, and Smart Pointers Study Pack",
    )

    story = [
        p("Rust Ownership, Closures, Lifetimes, and Smart Pointers", styles, "TopicTitle"),
        p(
            "Merged sheet based on ECM2433 Rust ownership, closures/iterators, lifetimes, "
            "and smart-pointer revision topics. It keeps related borrowing and ownership "
            "rules together instead of splitting them into several small sheets.",
            styles,
            "SourceText",
        ),
        p("What You Need To Know", styles, "BlueHeading"),
        p("1. Closures capture their environment", styles, "DarkHeading"),
        p(
            "A closure is an inline function-like value. It can borrow, mutably borrow, "
            "or move variables from the surrounding scope. The capture style affects "
            "whether the closure implements <font face=\"Courier\">Fn</font>, "
            "<font face=\"Courier\">FnMut</font>, or <font face=\"Courier\">FnOnce</font>.",
            styles,
        ),
        code(
            """
let threshold = 10;
let bigger = |n: &i32| *n > threshold;  // borrows threshold

let mut count = 0;
let mut inc = || {
    count += 1;                         // mutable borrow
};
inc();
            """,
            styles,
        ),
        p("2. Iterators are lazy until consumed", styles, "DarkHeading"),
        p(
            "Adapters such as <font face=\"Courier\">map</font> and "
            "<font face=\"Courier\">filter</font> return another iterator. Nothing is "
            "fully produced until a consuming method such as "
            "<font face=\"Courier\">collect</font>, <font face=\"Courier\">sum</font>, "
            "or <font face=\"Courier\">count</font> runs.",
            styles,
        ),
        code(
            """
let values = vec![1, 2, 3, 4];
let squares = values
    .iter()
    .filter(|n| **n % 2 == 0)
    .map(|n| *n * *n)
    .collect::<Vec<_>>();
            """,
            styles,
        ),
        p("3. Lifetimes describe borrowed relationships", styles, "DarkHeading"),
        p(
            "Lifetime annotations do not extend how long data lives. They describe which "
            "borrowed output is tied to which borrowed input, so Rust can reject dangling "
            "references.",
            styles,
        ),
        code(
            """
fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() >= b.len() { a } else { b }
}
            """,
            styles,
        ),
        p("4. Box and Rc", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">Box&lt;T&gt;</font> stores one owned value on the heap. "
            "It is useful for large values and recursive types. "
            "<font face=\"Courier\">Rc&lt;T&gt;</font> gives shared ownership in one thread "
            "by keeping a reference count. Cloning an <font face=\"Courier\">Rc</font> "
            "clones the pointer and increments the count; it does not clone the inner data.",
            styles,
        ),
        code(
            """
use std::rc::Rc;

let shared = Rc::new(String::from("notes"));
let a = Rc::clone(&shared);
let b = Rc::clone(&shared);
println!("{}", Rc::strong_count(&shared));  // 3
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        p("Question 1 - explain the capture:", styles),
        code(
            """
let factor = 3;
let scale = |n: i32| n * factor;
println!("{}", scale(4));
            """,
            styles,
        ),
        numbered(["Does this closure borrow or move <font face=\"Courier\">factor</font>? Explain briefly."], styles),
        p("Question 2 - fix the mutable closure:", styles),
        code(
            """
let mut count = 0;
let inc = || {
    count += 1;
};
inc();
            """,
            styles,
        ),
        numbered(["Fix the binding so the closure can be called."], styles, start=2),
        p("Question 3 - complete the iterator:", styles),
        code(
            """
let values = vec![1, 2, 3, 4, 5, 6];
let squares = values
    .iter()
    .filter(|n| **n % 2 == 0)
    .map(|n| /* fill this */)
    .collect::<Vec<_>>();
            """,
            styles,
        ),
        numbered(["Fill the map step so the result is <font face=\"Courier\">[4, 16, 36]</font>."], styles, start=3),
        numbered(
            [
                "Why does <font face=\"Courier\">map</font> alone not build a vector?",
                "Write the signature for <font face=\"Courier\">longest</font>, which returns one of two borrowed string slices.",
            ],
            styles,
            start=4,
        ),
        p("Question 6 - identify the lifetime error:", styles),
        code(
            """
fn bad() -> &str {
    let text = String::from("hello");
    &text
}
            """,
            styles,
        ),
        numbered(["Explain why this cannot compile and give one normal fix."], styles, start=6),
        p("Question 7 - read from a Box:", styles),
        code(
            """
fn read_boxed(n: &Box<i32>) -> i32 {
    /* return the inner integer */
}
            """,
            styles,
        ),
        numbered(["Complete the function body."], styles, start=7),
        p("Question 8 - fix the recursive type:", styles),
        code(
            """
enum List {
    Cons(i32, List),
    Nil,
}
            """,
            styles,
        ),
        numbered(["Fix this enum so Rust knows its size."], styles, start=8),
        p("Question 9 - trace the count:", styles),
        code(
            """
use std::rc::Rc;

let value = Rc::new(String::from("x"));
let a = Rc::clone(&value);
{
    let b = Rc::clone(&value);
    println!("{}", Rc::strong_count(&value));
}
println!("{}", Rc::strong_count(&value));
            """,
            styles,
        ),
        numbered(["What two numbers are printed, and why?"], styles, start=9),
        numbered(["Why is <font face=\"Courier\">Rc&lt;T&gt;</font> not the right shared-ownership tool for multiple threads?"], styles, start=10),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Attempt all questions before checking.", styles, "SourceText"),
        numbered(
            [
                "It borrows <font face=\"Courier\">factor</font> immutably because <font face=\"Courier\">i32</font> can be copied and the closure only reads it. A <font face=\"Courier\">move</font> closure would capture its own copy.",
                "Use <font face=\"Courier\">let mut inc = || { count += 1; };</font>. Calling a closure that mutates captured state needs a mutable closure binding.",
                "Use <font face=\"Courier\">*n * *n</font>. In the map step, <font face=\"Courier\">n</font> is <font face=\"Courier\">&#38;i32</font>.",
                "<font face=\"Courier\">map</font> is lazy and returns another iterator. Use a consumer such as <font face=\"Courier\">collect::&lt;Vec&lt;_&gt;&gt;()</font> to build a vector.",
                "<font face=\"Courier\">fn longest&lt;'a&gt;(a: &#38;'a str, b: &#38;'a str) -&#62; &#38;'a str</font>",
                "It returns a reference to <font face=\"Courier\">text</font>, but <font face=\"Courier\">text</font> is dropped when the function ends. Return an owned <font face=\"Courier\">String</font> or return a reference to input data instead.",
                "<font face=\"Courier\">**n</font>. One dereference goes from <font face=\"Courier\">&#38;Box&lt;i32&gt;</font> to <font face=\"Courier\">Box&lt;i32&gt;</font>, the next reaches the <font face=\"Courier\">i32</font>.",
                "Use indirection: <font face=\"Courier\">enum List { Cons(i32, Box&lt;List&gt;), Nil }</font>.",
                "It prints <font face=\"Courier\">3</font> inside the block and <font face=\"Courier\">2</font> after the block. Dropping <font face=\"Courier\">b</font> decreases the strong count.",
                "<font face=\"Courier\">Rc&lt;T&gt;</font> updates its count non-atomically and is not thread-safe. Use <font face=\"Courier\">Arc&lt;T&gt;</font> for shared ownership across threads.",
            ],
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
