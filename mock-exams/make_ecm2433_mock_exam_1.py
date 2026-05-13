from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer


OUT = Path(__file__).with_name("ECM2433-mock-paper-1.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("PaperTitle", parent=styles["Title"], fontSize=22, leading=27, textColor=colors.HexColor("#111827"), spaceAfter=10))
    styles.add(ParagraphStyle("PaperSubTitle", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#111827"), spaceAfter=7))
    styles.add(ParagraphStyle("QuestionTitle", parent=styles["Heading1"], fontSize=16, leading=19, textColor=colors.HexColor("#111827"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle("Part", parent=styles["Normal"], fontSize=9.3, leading=12, textColor=colors.HexColor("#111827"), spaceBefore=4, spaceAfter=4))
    styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=8.2, leading=10.4, textColor=colors.HexColor("#374151"), spaceAfter=4))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=7.1, leading=8.6, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=7))
    return styles


def p(text, styles, style="Part"):
    return Paragraph(escape(text), styles[style])


def raw_p(text, styles, style="Part"):
    return Paragraph(text, styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=92)


def part(label, text, marks, styles):
    return p(f"({label}) {text} ({marks} marks)", styles)


def answer_part(label, question, marks, answer, styles):
    return [
        p(f"({label}) Question ({marks} marks): {question}", styles),
        p(f"Answer: {answer}", styles),
    ]


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=17 * mm,
        rightMargin=17 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="ECM2433 Mock Paper 1",
    )

    story = [
        p("ECM2433", styles, "PaperTitle"),
        p("Mock Paper 1", styles, "PaperTitle"),
        p("The C Family", styles, "PaperSubTitle"),
        p("Closed Book", styles, "PaperSubTitle"),
        Spacer(1, 5 * mm),
        p("Additional Materials: None", styles),
        p("Permitted Materials: No calculators permitted", styles),
        Spacer(1, 5 * mm),
        p("Guidelines:", styles, "PaperSubTitle"),
        p("The duration of this paper is 2hr 00.", styles),
        p("Answer ALL questions.", styles),
        p("Write all answers in the answer booklet provided.", styles),
        p("Use only black pen or pencil.", styles),
        p("Mobile and electronic devices are not allowed.", styles),
        Spacer(1, 5 * mm),
        p(
            "This is a mock paper in the style of the May paper. Possible answers are skeleton answers.",
            styles,
            "Small",
        ),
        p("Answers and marking notes are at the end of this document.", styles, "Small"),
        PageBreak(),
    ]

    # Question 1
    story += [
        p("Question 1", styles, "QuestionTitle"),
        part("a", "Consider the following fragment. Explain what fflush(stdout) changes, and state one situation where the output before the newline might otherwise not appear immediately.", 4, styles),
        code(
            """
#include <stdio.h>

int main(void) {
    printf("loading");
    fflush(stdout);
    printf(" done\\n");
    return 0;
}
            """,
            styles,
        ),
        part("b", "A project contains main.c, stats.c, and stats.h. Write a Makefile fragment with variables CC and CFLAGS that builds an executable named report. Include rules for report, main.o, stats.o, and clean.", 6, styles),
        part("c", "Complete the function so it returns a newly allocated copy of src. The caller will free the returned pointer. Handle allocation failure.", 5, styles),
        code(
            """
#include <stdlib.h>
#include <string.h>

char *copy_label(const char *src) {
    char *copy = /* allocate enough space */;
    if (copy == NULL) {
        return NULL;
    }
    /* copy the string */
    return copy;
}
            """,
            styles,
        ),
        part("d", "Complete the comparator and call qsort so the array is sorted by score descending. If two scores are equal, sort by name ascending.", 6, styles),
        code(
            """
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[16];
    int score;
} Entry;

int compare_entries(const void *left, const void *right) {
    /* complete this comparator */
}

void sort_entries(Entry entries[], size_t len) {
    /* call qsort */
}
            """,
            styles,
        ),
        part("e", "Explain the bug in the final printf, and name the kind of behaviour C gives for that access.", 4, styles),
        code(
            """
int *p = malloc(sizeof *p);
*p = 10;
free(p);
printf("%d\\n", *p);
            """,
            styles,
        ),
        p("(Total 25 marks)", styles, "Small"),
        PageBreak(),
    ]

    # Question 2
    story += [
        p("Question 2", styles, "QuestionTitle"),
        part("a", "Write battery.hpp and battery.cpp for a class Battery with a private int percent, a constructor taking an int, set_percent, and get_percent. The setter should ignore values outside 0 to 100. Use an include guard and member function definitions in the source file.", 7, styles),
        part("b", "The following class owns a raw heap array. Identify two resource-management problems and give a safer correction using either the rule of three idea or a standard RAII object.", 5, styles),
        code(
            """
class Buffer {
    char *data;
public:
    Buffer(int size) {
        data = new char[size];
    }

    ~Buffer() = default;
};
            """,
            styles,
        ),
        part("c", "Fix the binary search bug, then write a separate sort call that orders the same values descending.", 5, styles),
        code(
            """
#include <algorithm>
#include <vector>

std::vector<int> values = {9, 1, 4, 7};
bool found = std::binary_search(values.begin(), values.end(), 4);
            """,
            styles,
        ),
        part("d", "Trace the shared ownership and explain whether the weak pointer can still be locked at the marked line.", 4, styles),
        code(
            """
#include <memory>
#include <iostream>

auto a = std::make_shared<int>(42);
std::weak_ptr<int> watch = a;
auto b = a;
a.reset();

if (auto p = watch.lock()) {
    std::cout << *p << "\\n";
}
            """,
            styles,
        ),
        part("e", "In the catch line below, explain why the exception is caught by const reference and what error.what() provides.", 4, styles),
        code(
            """
try {
    throw std::invalid_argument("negative age");
} catch (const std::invalid_argument& error) {
    std::cerr << error.what() << "\\n";
}
            """,
            styles,
        ),
        p("(Total 25 marks)", styles, "Small"),
        PageBreak(),
    ]

    # Question 3
    story += [
        p("Question 3", styles, "QuestionTitle"),
        part("a", "The function below fails to compile. Explain the role of the semicolon and fix the function.", 4, styles),
        code(
            """
fn double(n: i32) -> i32 {
    n * 2;
}
            """,
            styles,
        ),
        part("b", "Complete classify as a single if expression. Explain why the expression needs an else branch.", 4, styles),
        code(
            """
fn classify(score: u32) -> &'static str {
    let result = /* pass if score >= 40, otherwise fail */;
    result
}
            """,
            styles,
        ),
        part("c", "This program tries to use a moved String. Explain the error and show two fixes: one using borrowing, and one using clone.", 5, styles),
        code(
            """
fn print_name(name: String) {
    println!("{name}");
}

fn main() {
    let user = String::from("Ada");
    print_name(user);
    println!("{user}");
}
            """,
            styles,
        ),
        part("d", "Write the sort_by call that sorts readings by the floating-point value ascending and then by id descending. Explain why partial_cmp is used.", 6, styles),
        code(
            """
let mut readings = vec![(0.5, 2), (0.1, 9), (0.5, 1)];
/* sort here */
            """,
            styles,
        ),
        part("e", "Complete parse_count so it trims the input, parses an i32, and returns parse errors to the caller without unwrap.", 6, styles),
        code(
            """
fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = /* parse with ? */;
    Ok(n)
}
            """,
            styles,
        ),
        p("(Total 25 marks)", styles, "Small"),
        PageBreak(),
    ]

    # Question 4
    story += [
        p("Question 4", styles, "QuestionTitle"),
        part("a", "Complete the loop so four worker threads all send one value through the same channel. Explain why drop(tx) is needed before the receiving loop can finish.", 7, styles),
        code(
            """
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    for id in 0..4 {
        /* spawn a worker that sends id * 10 */
    }

    drop(tx);

    for value in rx {
        println!("{value}");
    }
}
            """,
            styles,
        ),
        part("b", "Complete the shared counter update using Arc<Mutex<i32>>. Explain what lock returns and why each update is exclusive.", 6, styles),
        code(
            """
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = Vec::new();

for _ in 0..4 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        /* increment the shared counter */
    }));
}

for handle in handles {
    handle.join().unwrap();
}
            """,
            styles,
        ),
        part("c", "Fix the generic function signature so it can compare two values and print the larger one using normal display formatting.", 4, styles),
        code(
            """
fn show_larger<T>(a: T, b: T) {
    let winner = if a > b { a } else { b };
    println!("{winner}");
}
            """,
            styles,
        ),
        part("d", "Fix the recursive enum so Rust knows its size, then explain why the indirection is needed.", 4, styles),
        code(
            """
enum List {
    Cons(i32, List),
    Nil,
}
            """,
            styles,
        ),
        part("e", "For the custom Team key below, add the derives needed for insertion and lookup in a HashMap. State why those traits are needed.", 4, styles),
        code(
            """
use std::collections::HashMap;

struct Team {
    name: String,
    division: u8,
}

let mut scores = HashMap::new();
scores.insert(Team { name: String::from("red"), division: 1 }, 12);
            """,
            styles,
        ),
        p("(Total 25 marks)", styles, "Small"),
        PageBreak(),
    ]

    story += [
        p("Answers and marking notes", styles, "PaperTitle"),
        p("These are skeleton answers. Equivalent correct code and reasoning should receive credit.", styles, "Small"),
        p("Question 1", styles, "QuestionTitle"),
        *answer_part("a", "Consider the following fragment. Explain what fflush(stdout) changes, and state one situation where the output before the newline might otherwise not appear immediately.", 4, "fflush(stdout) forces pending buffered output on stdout to be written immediately. Without it, the text may remain in the buffer until newline, a full buffer, or normal program exit.", styles),
        *answer_part("b", "A project contains main.c, stats.c, and stats.h. Write a Makefile fragment with variables CC and CFLAGS that builds an executable named report. Include rules for report, main.o, stats.o, and clean.", 6, "One suitable Makefile:", styles),
        code(
            """
CC = gcc
CFLAGS = -std=c99 -Wall -Wextra

report: main.o stats.o
<TAB>$(CC) $(CFLAGS) main.o stats.o -o report

main.o: main.c stats.h
<TAB>$(CC) $(CFLAGS) -c main.c -o main.o

stats.o: stats.c stats.h
<TAB>$(CC) $(CFLAGS) -c stats.c -o stats.o

clean:
<TAB>rm -f *.o report
            """,
            styles,
        ),
        *answer_part("c", "Complete the function so it returns a newly allocated copy of src. The caller will free the returned pointer. Handle allocation failure.", 5, "Allocate strlen(src) + 1 bytes, check NULL, then copy the string.", styles),
        code(
            """
char *copy_label(const char *src) {
    char *copy = malloc(strlen(src) + 1);
    if (copy == NULL) {
        return NULL;
    }
    strcpy(copy, src);
    return copy;
}
            """,
            styles,
        ),
        *answer_part("d", "Complete the comparator and call qsort so the array is sorted by score descending. If two scores are equal, sort by name ascending.", 6, "Comparator and qsort call:", styles),
        code(
            """
int compare_entries(const void *left, const void *right) {
    const Entry *a = left;
    const Entry *b = right;

    if (a->score < b->score) {
        return 1;
    }
    if (a->score > b->score) {
        return -1;
    }
    return strcmp(a->name, b->name);
}

void sort_entries(Entry entries[], size_t len) {
    qsort(entries, len, sizeof entries[0], compare_entries);
}
            """,
            styles,
        ),
        *answer_part("e", "Explain the bug in the final printf, and name the kind of behaviour C gives for that access.", 4, "After free(p), p is dangling. Dereferencing it is use-after-free and gives undefined behaviour.", styles),
        p("Question 2", styles, "QuestionTitle"),
        *answer_part("a", "Write battery.hpp and battery.cpp for a class Battery with a private int percent, a constructor taking an int, set_percent, and get_percent. The setter should ignore values outside 0 to 100. Use an include guard and member function definitions in the source file.", 7, "One correct split:", styles),
        code(
            """
/* battery.hpp */
#ifndef BATTERY_HPP
#define BATTERY_HPP

class Battery {
    int percent;
public:
    Battery(int percent);
    void set_percent(int percent);
    int get_percent() const;
};

#endif

/* battery.cpp */
#include "battery.hpp"

Battery::Battery(int percent) : percent(0) {
    set_percent(percent);
}

void Battery::set_percent(int percent) {
    if (percent < 0 || percent > 100) {
        return;
    }
    this->percent = percent;
}

int Battery::get_percent() const {
    return percent;
}
            """,
            styles,
        ),
        *answer_part("b", "The following class owns a raw heap array. Identify two resource-management problems and give a safer correction using either the rule of three idea or a standard RAII object.", 5, "The default destructor does not delete the owned array, so it leaks. The default copy behaviour would also copy only the pointer, risking double delete if a destructor were added. Safer fixes include using std::vector<char> or std::string, or writing destructor, copy constructor, and copy assignment correctly.", styles),
        code(
            """
#include <vector>

class Buffer {
    std::vector<char> data;
public:
    explicit Buffer(int size) : data(size) {}
};
            """,
            styles,
        ),
        *answer_part("c", "Fix the binary search bug, then write a separate sort call that orders the same values descending.", 5, "binary_search requires a sorted range. Then descending sort uses a comparator.", styles),
        code(
            """
std::sort(values.begin(), values.end());
bool found = std::binary_search(values.begin(), values.end(), 4);

std::sort(values.begin(), values.end(), [](int a, int b) {
    return a > b;
});
            """,
            styles,
        ),
        *answer_part("d", "Trace the shared ownership and explain whether the weak pointer can still be locked at the marked line.", 4, "After auto b = a, there are two shared owners. a.reset() removes one owner, but b still owns the int. watch.lock() succeeds and prints 42. The object is destroyed when the last shared_ptr owner is gone.", styles),
        *answer_part("e", "In the catch line below, explain why the exception is caught by const reference and what error.what() provides.", 4, "Catching by const reference avoids copying and preserves the dynamic exception object. error.what() returns a C string describing the exception, here negative age.", styles),
        p("Question 3", styles, "QuestionTitle"),
        *answer_part("a", "The function below fails to compile. Explain the role of the semicolon and fix the function.", 4, "The semicolon makes n * 2 a statement, so the block evaluates to unit (). Remove the semicolon:", styles),
        code(
            """
fn double(n: i32) -> i32 {
    n * 2
}
            """,
            styles,
        ),
        *answer_part("b", "Complete classify as a single if expression. Explain why the expression needs an else branch.", 4, "if is being used as an expression, so both branches must produce a value:", styles),
        code(
            """
fn classify(score: u32) -> &'static str {
    let result = if score >= 40 {
        "pass"
    } else {
        "fail"
    };
    result
}
            """,
            styles,
        ),
        *answer_part("c", "This program tries to use a moved String. Explain the error and show two fixes: one using borrowing, and one using clone.", 5, "print_name takes ownership of the String, so user cannot be used afterwards. Borrowing fix:", styles),
        code(
            """
fn print_name(name: &str) {
    println!("{name}");
}

let user = String::from("Ada");
print_name(&user);
println!("{user}");
            """,
            styles,
        ),
        p("Keeping the original print_name(String), clone fix:", styles),
        code(
            """
let user = String::from("Ada");
print_name(user.clone());
println!("{user}");
            """,
            styles,
        ),
        *answer_part("d", "Write the sort_by call that sorts readings by the floating-point value ascending and then by id descending. Explain why partial_cmp is used.", 6, "Float sorting uses partial_cmp because NaN means floats may not have a total ordering.", styles),
        code(
            """
readings.sort_by(|a, b| {
    a.0.partial_cmp(&b.0)
        .unwrap()
        .then_with(|| b.1.cmp(&a.1))
});
            """,
            styles,
        ),
        *answer_part("e", "Complete parse_count so it trims the input, parses an i32, and returns parse errors to the caller without unwrap.", 6, "Use parse with an explicit target type and ?. The function must return Result.", styles),
        code(
            """
fn parse_count(text: &str) -> Result<i32, std::num::ParseIntError> {
    let n = text.trim().parse::<i32>()?;
    Ok(n)
}
            """,
            styles,
        ),
        p("Question 4", styles, "QuestionTitle"),
        *answer_part("a", "Complete the loop so four worker threads all send one value through the same channel. Explain why drop(tx) is needed before the receiving loop can finish.", 7, "Clone the transmitter for each worker and move that clone into the closure. drop(tx) removes the original sender so the receiver loop can end once worker senders are gone.", styles),
        code(
            """
for id in 0..4 {
    let tx = tx.clone();
    thread::spawn(move || {
        tx.send(id * 10).unwrap();
    });
}
            """,
            styles,
        ),
        *answer_part("b", "Complete the shared counter update using Arc<Mutex<i32>>. Explain what lock returns and why each update is exclusive.", 6, "Arc gives shared ownership; Mutex gives exclusive mutable access. lock returns a Result containing a guard. The guard dereferences to the protected value and unlocks when dropped.", styles),
        code(
            """
handles.push(thread::spawn(move || {
    let mut value = counter.lock().unwrap();
    *value += 1;
}));
            """,
            styles,
        ),
        *answer_part("c", "Fix the generic function signature so it can compare two values and print the larger one using normal display formatting.", 4, "PartialOrd is needed for > and Display is needed for normal braces formatting.", styles),
        code(
            """
use std::fmt::Display;

fn show_larger<T>(a: T, b: T)
where
    T: PartialOrd + Display,
{
    let winner = if a > b { a } else { b };
    println!("{winner}");
}
            """,
            styles,
        ),
        *answer_part("d", "Fix the recursive enum so Rust knows its size, then explain why the indirection is needed.", 4, "Box gives a fixed-size pointer to the rest of the list. Without indirection, List would contain another full List recursively and have no known size.", styles),
        code(
            """
enum List {
    Cons(i32, Box<List>),
    Nil,
}
            """,
            styles,
        ),
        *answer_part("e", "For the custom Team key below, add the derives needed for insertion and lookup in a HashMap. State why those traits are needed.", 4, "HashMap keys need equality and hashing. Debug is often useful for tests but not required for HashMap itself.", styles),
        code(
            """
#[derive(PartialEq, Eq, Hash)]
struct Team {
    name: String,
    division: u8,
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
