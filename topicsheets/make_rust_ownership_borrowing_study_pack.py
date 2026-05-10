from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, Preformatted, SimpleDocTemplate


OUT = Path(__file__).with_name("rust-ownership-borrowing-study-pack.pdf")


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
    return ListFlowable([ListItem(p(item, styles), leftIndent=4 * mm) for item in items], bulletType="bullet", leftIndent=6 * mm, bulletFontName="Helvetica", bulletFontSize=7)


def numbered(items, styles):
    return ListFlowable([ListItem(p(item, styles), leftIndent=5 * mm) for item in items], bulletType="1", leftIndent=7 * mm, bulletFontName="Helvetica-Bold", bulletFontSize=8)


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm, title="Rust Ownership and Borrowing Study Pack")
    story = [
        p("Rust Ownership and Borrowing", styles, "TopicTitle"),
        p("Based on ECM2433 Rust ownership, slices/strings, and lifetime slides.", styles, "SourceText"),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. The ownership rules", styles, "DarkHeading"),
        bullets([
            "Each value in Rust has an owner.",
            "There can only be one owner at a time.",
            "When the owner goes out of scope, the value is dropped.",
        ], styles),
        p("2. Stack, heap, and String", styles, "DarkHeading"),
        p("Fixed-size scalar values often live on the stack. A String owns heap text; its stack part stores a pointer, length, and capacity.", styles),
        p("3. Move, Copy, and clone", styles, "DarkHeading"),
        code("""
let s1 = String::from("hello");
let s2 = s1;       // move
// println!("{s1}"); // error: s1 was moved

let x = 5;
let y = x;         // Copy
println!("{x} {y}");
        """, styles),
        p("4. Borrowing with references", styles, "DarkHeading"),
        p("A reference borrows a value without taking ownership. For read-only text parameters, prefer <font face=\"Courier\">&#38;str</font> because it accepts string literals and borrowed String values.", styles),
        code("""
fn announce(message: &str) {
    println!("{message}");
}

let msg = String::from("hello");
announce(&msg);
println!("{msg}");
        """, styles),
        p("5. Mutable references and borrowing rules", styles, "DarkHeading"),
        p("A mutable reference allows modification through a borrow. Rust allows either one mutable reference or any number of immutable references, but not both at the same time.", styles),
        code("""
fn shout(text: &mut String) {
    text.push_str("!");
}

let mut msg = String::from("hello");
shout(&mut msg);
        """, styles),
        p("6. Slices and lifetimes", styles, "DarkHeading"),
        p("<font face=\"Courier\">&#38;[T]</font> is a borrowed slice of elements. <font face=\"Courier\">&#38;str</font> is a borrowed string slice. Rust rejects references that could outlive the data they point to.", styles),
        code("""
fn bad() -> &str {
    let s = String::from("hello");
    &s
}

fn good() -> String {
    String::from("hello")
}
        """, styles),
        p("Practice Questions", styles, "BlueHeading"),
        numbered([
            "Write the three ownership rules in your own words.",
            "Explain why <font face=\"Courier\">let s2 = s1; println!(\"{s1}\");</font> fails when <font face=\"Courier\">s1</font> is a String.",
            "Explain why copying an <font face=\"Courier\">i32</font> leaves both variables usable.",
            "Fix a function parameter so it can print read-only text without taking ownership from the caller.",
            "Write a <font face=\"Courier\">count_vowels</font> signature using <font face=\"Courier\">&#38;str</font> and explain why that parameter type is useful.",
            "Explain why two active mutable references to the same String are not allowed.",
            "Write a function that appends <font face=\"Courier\">!</font> to a String through a mutable reference.",
            "Explain the difference between <font face=\"Courier\">String</font> and <font face=\"Courier\">&#38;str</font>.",
            "Explain why a function cannot return a reference to a String created inside that function.",
            "For <font face=\"Courier\">let nums = [10, 20, 30, 40];</font>, show how to pass the whole array to a function taking <font face=\"Courier\">&#38;[i32]</font>.",
        ], styles),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions.", styles, "SourceText"),
        numbered([
            "Each value has one owner; only one owner exists at a time; when the owner goes out of scope, the value is dropped.",
            "String owns heap data. Assignment moves ownership to <font face=\"Courier\">s2</font>, so <font face=\"Courier\">s1</font> is no longer valid.",
            "<font face=\"Courier\">i32</font> implements Copy, so assignment duplicates the value rather than moving ownership.",
            "Prefer <font face=\"Courier\">fn announce(message: &#38;str)</font>, then call it with a literal or a borrowed String.",
            "Expected shape: <font face=\"Courier\">fn count_vowels(text: &#38;str) -&#62; usize</font>. It only reads text and accepts literals and borrowed String values.",
            "Two active mutable references could both write to the same value. Rust enforces one writer or many readers.",
            "Expected shape: <font face=\"Courier\">fn shout(text: &#38;mut String) { text.push_str(\"!\"); }</font>, called with a mutable borrow.",
            "String owns growable heap text. <font face=\"Courier\">&#38;str</font> is a borrowed string slice: pointer plus length, no ownership.",
            "The local String is dropped when the function returns, so the reference would point to invalid data. Return an owned String instead.",
            "Expected: call a function like <font face=\"Courier\">use_all(&#38;nums)</font> when its parameter is <font face=\"Courier\">&#38;[i32]</font>.",
        ], styles),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
