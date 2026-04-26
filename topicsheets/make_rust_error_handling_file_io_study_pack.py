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


OUT = Path(__file__).with_name("rust-error-handling-file-io-study-pack.pdf")


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
        title="Rust Error Handling and File I/O Study Pack",
    )

    story = [
        p("Rust Error Handling and File I/O", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 Rust Lecture 05 and worksheet 2, chosen from red Rust topics in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. Recoverable vs unrecoverable errors", styles, "DarkHeading"),
        p(
            "Rust separates errors into two broad categories. Unrecoverable errors usually indicate a bug or broken assumption and stop the program with <font face=\"Courier\">panic!</font>. Recoverable errors are represented with <font face=\"Courier\">Result&lt;T, E&gt;</font>, so the caller must decide how to handle failure.",
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">panic!</font>: stop immediately for unrecoverable situations.",
                "<font face=\"Courier\">Result&lt;T, E&gt;</font>: explicit recoverable success/failure.",
                "<font face=\"Courier\">Option&lt;T&gt;</font>: value may be present or absent, but there is no error information.",
            ],
            styles,
        ),
        p("2. <font face=\"Courier\">Result&lt;T, E&gt;</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">Result&lt;T, E&gt;</font> is an enum with two variants: <font face=\"Courier\">Ok(T)</font> for success and <font face=\"Courier\">Err(E)</font> for failure. Unlike <font face=\"Courier\">Option</font>, the failure case carries error information.",
            styles,
        ),
        code(
            """
let number: Result<i32, _> = "42".parse();

match number {
    Ok(n) => println!("number = {n}"),
    Err(e) => println!("parse failed: {e}"),
}
            """,
            styles,
        ),
        p("3. Handling locally with <font face=\"Courier\">match</font>", styles, "DarkHeading"),
        p(
            "Use <font face=\"Courier\">match</font> when the current function should decide what to do with both success and failure. This is useful when you want to print a friendly message, choose a default, or recover locally.",
            styles,
        ),
        code(
            """
fn parse_age(text: &str) -> i32 {
    match text.parse::<i32>() {
        Ok(age) => age,
        Err(_) => 0,
    }
}
            """,
            styles,
        ),
        p("4. Propagating errors with <font face=\"Courier\">?</font>", styles, "DarkHeading"),
        p(
            "The <font face=\"Courier\">?</font> operator is for propagation. If the result is <font face=\"Courier\">Ok(value)</font>, it unwraps the value. If it is <font face=\"Courier\">Err(error)</font>, it returns that error early from the current function. The function using <font face=\"Courier\">?</font> must itself return a compatible <font face=\"Courier\">Result</font>.",
            styles,
        ),
        code(
            """
fn read_name(path: &str) -> Result<String, std::io::Error> {
    let text = std::fs::read_to_string(path)?;
    Ok(text)
}
            """,
            styles,
        ),
        p("5. Reading files", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">std::fs::read_to_string</font> reads an entire file into a <font face=\"Courier\">String</font>. It returns <font face=\"Courier\">Result&lt;String, io::Error&gt;</font> because the file might not exist or might not be readable.",
            styles,
        ),
        code(
            """
use std::fs;

fn print_lines(path: &str) -> Result<(), std::io::Error> {
    let text = fs::read_to_string(path)?;
    for line in text.lines() {
        println!("{line}");
    }
    Ok(())
}
            """,
            styles,
        ),
        p("6. Parsing and custom errors", styles, "DarkHeading"),
        p(
            "Worksheet exercises use functions like <font face=\"Courier\">parse_item(line: &#38;str) -&gt; Result&lt;Item, String&gt;</font>. Return <font face=\"Courier\">Ok(value)</font> when parsing succeeds and <font face=\"Courier\">Err(message)</font> when the line has the wrong number of fields or a field cannot be parsed.",
            styles,
        ),
        code(
            """
struct Item {
    name: String,
    quantity: u32,
    unit_price: f64,
}

fn parse_item(line: &str) -> Result<Item, String> {
    let parts: Vec<&str> = line.split(',').collect();
    if parts.len() != 3 {
        return Err("expected three fields".to_string());
    }

    let quantity = parts[1].trim().parse::<u32>()
        .map_err(|_| "bad quantity".to_string())?;
    let unit_price = parts[2].trim().parse::<f64>()
        .map_err(|_| "bad price".to_string())?;

    Ok(Item {
        name: parts[0].trim().to_string(),
        quantity,
        unit_price,
    })
}
            """,
            styles,
        ),
        p("7. <font face=\"Courier\">unwrap</font>, <font face=\"Courier\">expect</font>, and <font face=\"Courier\">main</font>", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">unwrap()</font> extracts the success value but panics on error. <font face=\"Courier\">expect()</font> does the same but lets you provide a message. They are convenient for quick experiments but should usually be avoided in library code. Library functions should return <font face=\"Courier\">Result</font> so callers can handle errors.",
            styles,
        ),
        p(
            "A useful pattern is <font face=\"Courier\">fn main() -&gt; Result&lt;(), Box&lt;dyn std::error::Error&gt;&gt;</font>, which lets <font face=\"Courier\">main</font> use <font face=\"Courier\">?</font> with different error types.",
            styles,
        ),
        code(
            """
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let text = std::fs::read_to_string("input.txt")?;
    let n: i32 = text.trim().parse()?;
    println!("{n}");
    Ok(())
}
            """,
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Given an out-of-bounds vector index and a missing input file, choose which one should usually be <font face=\"Courier\">panic!</font> and which should usually be <font face=\"Courier\">Result</font>. Explain why.",
                "For <font face=\"Courier\">let x = \"abc\".parse::&lt;i32&gt;();</font>, what kind of value is returned, and which variant do you expect?",
                "Rewrite a parse operation using <font face=\"Courier\">match</font> so invalid input prints <font face=\"Courier\">invalid number</font> instead of panicking.",
                "In a function returning <font face=\"Courier\">Result&lt;i32, ParseIntError&gt;</font>, use <font face=\"Courier\">?</font> to parse a string into an integer and return it doubled.",
                "Write a function signature and body that reads an entire file into a <font face=\"Courier\">String</font> using <font face=\"Courier\">fs::read_to_string</font> and propagates I/O errors.",
                "Why can a function using <font face=\"Courier\">?</font> not return plain <font face=\"Courier\">i32</font>?",
                "Write the first error check in <font face=\"Courier\">parse_item</font>: split a CSV line by commas and return <font face=\"Courier\">Err</font> if there are not exactly three fields.",
                "Use <font face=\"Courier\">map_err</font> or <font face=\"Courier\">match</font> to turn a failed <font face=\"Courier\">u32</font> parse into <font face=\"Courier\">Err(\"bad quantity\".to_string())</font>.",
                "Explain why <font face=\"Courier\">unwrap</font> is usually a bad choice inside reusable library functions.",
                "Write a <font face=\"Courier\">main</font> signature that allows <font face=\"Courier\">?</font> with multiple error types, then show the final success return value.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p("Use this after attempting the questions. Good answers should distinguish handling locally from propagating errors.", styles, "SourceText"),
        numbered(
            [
                "Out-of-bounds indexing is usually a programming bug and can panic. A missing input file is an expected recoverable failure and should usually be represented with <font face=\"Courier\">Result</font>.",
                "It returns a <font face=\"Courier\">Result&lt;i32, _&gt;</font>. For <font face=\"Courier\">\"abc\"</font>, parsing as <font face=\"Courier\">i32</font> fails, so the result is <font face=\"Courier\">Err</font>.",
                "A correct answer matches <font face=\"Courier\">Ok(n)</font> and <font face=\"Courier\">Err(_)</font>, printing <font face=\"Courier\">invalid number</font> in the error arm.",
                "Expected pattern: <font face=\"Courier\">let n = text.parse::&lt;i32&gt;()?; Ok(n * 2)</font> inside a function returning <font face=\"Courier\">Result&lt;i32, ParseIntError&gt;</font>.",
                "Expected pattern: <font face=\"Courier\">fn read_file(path: &#38;str) -&gt; Result&lt;String, std::io::Error&gt; { let text = std::fs::read_to_string(path)?; Ok(text) }</font>.",
                "Because <font face=\"Courier\">?</font> may need to return an error early. A plain <font face=\"Courier\">i32</font> return type has nowhere to put the error.",
                "Expected: split with <font face=\"Courier\">line.split(',')</font>, collect or count fields, and return <font face=\"Courier\">Err(...)</font> unless there are exactly three fields.",
                "Valid answers include <font face=\"Courier\">parts[1].trim().parse::&lt;u32&gt;().map_err(|_| \"bad quantity\".to_string())?</font> or an equivalent <font face=\"Courier\">match</font>.",
                "<font face=\"Courier\">unwrap</font> panics on error, so callers cannot recover. Reusable code should return <font face=\"Courier\">Result</font> and let the caller decide.",
                "Expected: <font face=\"Courier\">fn main() -&gt; Result&lt;(), Box&lt;dyn std::error::Error&gt;&gt;</font> and final success value <font face=\"Courier\">Ok(())</font>.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
fn double_number(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = text.parse::<i32>()?;
    Ok(n * 2)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let text = std::fs::read_to_string("input.txt")?;
    let n = double_number(text.trim())?;
    println!("{n}");
    Ok(())
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
