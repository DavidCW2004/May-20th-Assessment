from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer


OUT = Path(__file__).with_name("ECM2433-mock-paper-2.pdf")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("PaperTitle", parent=styles["Title"], fontSize=22, leading=27, textColor=colors.HexColor("#111827"), spaceAfter=10))
    styles.add(ParagraphStyle("PaperSubTitle", parent=styles["Heading2"], fontSize=14, leading=17, textColor=colors.HexColor("#111827"), spaceAfter=7))
    styles.add(ParagraphStyle("QuestionTitle", parent=styles["Heading1"], fontSize=16, leading=19, textColor=colors.HexColor("#111827"), spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle("Part", parent=styles["Normal"], fontSize=9.1, leading=11.8, textColor=colors.HexColor("#111827"), spaceBefore=4, spaceAfter=4))
    styles.add(ParagraphStyle("Small", parent=styles["Normal"], fontSize=8.1, leading=10.2, textColor=colors.HexColor("#374151"), spaceAfter=4))
    styles.add(ParagraphStyle("CodeBlock", parent=styles["Code"], fontName="Courier", fontSize=6.9, leading=8.3, backColor=colors.HexColor("#f3f4f6"), borderColor=colors.HexColor("#d1d5db"), borderWidth=0.4, borderPadding=4, spaceAfter=7))
    return styles


def p(text, styles, style="Part"):
    return Paragraph(escape(text), styles[style])


def code(text, styles):
    return Preformatted(text.strip("\n"), styles["CodeBlock"], maxLineLength=94)


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
        title="ECM2433 Mock Paper 2",
    )

    story = [
        p("ECM2433", styles, "PaperTitle"),
        p("Mock Paper 2", styles, "PaperTitle"),
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
        p("This is a mock paper in the style of the May paper. Possible answers are skeleton answers.", styles, "Small"),
        p("Answers and marking notes are at the end of this document.", styles, "Small"),
        PageBreak(),
    ]

    q1a = "Complete parse_positive so it accepts only a whole positive decimal int from text. It must reject no digits, trailing junk, range errors, zero, and values too large for int."
    q1b = "Complete the file fragment so it opens the named file, reports an open failure using errno and strerror, reads one line safely, and closes the file on the successful path."
    q1c = "The helper make_node should be usable only inside stack.c, while push should be callable from other files. Fix the declarations and state which declaration belongs in the header."
    q1d = "Complete remove_first so it removes the first linked-list node with the given key, updates the caller's head pointer when needed, frees the removed node, and returns 1 on success or 0 if no node matched."
    q1e = "A loop reads characters with fgetc until EOF. Add the check that distinguishes a read error from a clean end-of-file, and explain why EOF alone is not enough."
    story += [
        p("Question 1", styles, "QuestionTitle"),
        part("a", q1a, 5, styles),
        code(
            """
#include <errno.h>
#include <limits.h>
#include <stdlib.h>

int parse_positive(const char *text, int *out) {
    char *end = NULL;
    errno = 0;
    long value = strtol(text, &end, 10);

    /* checks here */

    *out = (int)value;
    return 1;
}
            """,
            styles,
        ),
        part("b", q1b, 5, styles),
        code(
            """
#include <errno.h>
#include <stdio.h>
#include <string.h>

int print_first_line(const char *path) {
    FILE *fp = fopen(path, "r");
    char line[80];

    /* failure handling and read here */

    return 0;
}
            """,
            styles,
        ),
        part("c", q1c, 4, styles),
        code(
            """
/* stack.c */
Node *make_node(char value);
Stack push(Stack stack, char value);
            """,
            styles,
        ),
        part("d", q1d, 7, styles),
        code(
            """
#include <stdlib.h>

typedef struct Node {
    char key;
    struct Node *next;
} Node;

int remove_first(Node **head, char key) {
    /* complete this function */
}
            """,
            styles,
        ),
        part("e", q1e, 4, styles),
        code(
            """
int ch;
long count = 0;

while ((ch = fgetc(fp)) != EOF) {
    count++;
}

/* error check here */
            """,
            styles,
        ),
        p("(Total 25 marks)", styles, "Small"),
        PageBreak(),
    ]

    q2a = "Complete operator[] so assignment through grades[2] changes the stored element. Include a simple bounds check."
    q2b = "Complete the output operator for Date so std::cout << d prints day/month/year and can still be chained with another output."
    q2c = "Write the out-of-class definitions for the Box template constructor and get method. Use the correct template headers and qualified names, and state where template definitions should normally live."
    q2d = "Trace the construction and destruction output for the automatic object in main, then explain the order."
    q2e = "Write make_shape so it returns unique ownership of a Circle through the Shape interface. Explain why Shape's destructor must be virtual."
    story += [
        p("Question 2", styles, "QuestionTitle"),
        part("a", q2a, 5, styles),
        code(
            """
#include <stdexcept>

class Grades {
    int data[4] = {0, 0, 0, 0};

public:
    /* operator[] here */
};
            """,
            styles,
        ),
        part("b", q2b, 5, styles),
        code(
            """
#include <iostream>

class Date {
    int day;
    int month;
    int year;

public:
    Date(int d, int m, int y) : day(d), month(m), year(y) {}
    /* friend declaration here */
};

/* operator definition here */
            """,
            styles,
        ),
        part("c", q2c, 5, styles),
        code(
            """
template<typename T>
class Box {
    T value;

public:
    Box(T value);
    T get() const;
};

/* definitions here */
            """,
            styles,
        ),
        part("d", q2d, 5, styles),
        code(
            """
#include <iostream>

class Base {
public:
    Base() { std::cout << "B+"; }
    ~Base() { std::cout << "B-"; }
};

class Derived : public Base {
public:
    Derived() { std::cout << "D+"; }
    ~Derived() { std::cout << "D-"; }
};

int main() {
    Derived item;
}
            """,
            styles,
        ),
        part("e", q2e, 5, styles),
        code(
            """
#include <memory>

class Shape {
public:
    virtual double area() const = 0;
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double radius;

public:
    explicit Circle(double radius) : radius(radius) {}
    double area() const override { return 3.14159 * radius * radius; }
};

/* make_shape here */
            """,
            styles,
        ),
        p("(Total 25 marks)", styles, "Small"),
        PageBreak(),
    ]

    q3a = "Fix the lifetime error in choose_label. Explain what the lifetime annotation says and why it does not keep either input alive for longer."
    q3b = "Explain what the closure captures, why the closure variable must be mutable, and name the closure trait it needs in order to update seen."
    q3c = "Write an iterator pipeline that collects the index and value for every present positive reading into Vec<(usize, i32)> without using explicit indexing."
    q3d = "Complete total_file so it reads the file, parses each line as i32, adds the values, and propagates both I/O and parse errors with the question-mark operator."
    q3e = "Rewrite third_name so it does not panic when the slice is too short. It should return Option<&str> borrowed from the input."
    story += [
        p("Question 3", styles, "QuestionTitle"),
        part("a", q3a, 5, styles),
        code(
            """
fn choose_label(primary: &str, fallback: &str) -> &str {
    if primary.is_empty() {
        fallback
    } else {
        primary
    }
}
            """,
            styles,
        ),
        part("b", q3b, 4, styles),
        code(
            """
let mut seen = 0;

let record = |word: &str| {
    if word.starts_with('a') {
        seen += 1;
    }
};

record("apple");
record("pear");
            """,
            styles,
        ),
        part("c", q3c, 5, styles),
        code(
            """
let readings = vec![Some(3), None, Some(-2), Some(8)];
/* collect [(0, 3), (3, 8)] */
            """,
            styles,
        ),
        part("d", q3d, 6, styles),
        code(
            """
use std::error::Error;
use std::fs;

fn total_file(path: &str) -> Result<i32, Box<dyn Error>> {
    /* complete */
}
            """,
            styles,
        ),
        part("e", q3e, 5, styles),
        code(
            """
fn third_name(names: &[String]) -> &str {
    &names[2]
}
            """,
            styles,
        ),
        p("(Total 25 marks)", styles, "Small"),
        PageBreak(),
    ]

    q4a = "Complete copy_slot so it copies the array element at source index from into destination index to. Explain why the element width is needed."
    q4b = "Complete the lambda so it reads limit, updates hits, and can be called for every value in the vector."
    q4c = "Complete the loop so repeated product names accumulate totals in the HashMap instead of replacing earlier totals."
    q4d = "Implement Iterator for Countdown so it yields current, current - 1, down to 1, and then stops."
    q4e = "The function tries to calculate an array length using sizeof after the array is passed to a function. Explain the bug and rewrite the function signature and call so the length is handled correctly."
    story += [
        p("Question 4", styles, "QuestionTitle"),
        part("a", q4a, 6, styles),
        code(
            """
#include <stddef.h>
#include <string.h>

void copy_slot(void *array, size_t from, size_t to, size_t width) {
    /* complete */
}
            """,
            styles,
        ),
        part("b", q4b, 4, styles),
        code(
            """
#include <vector>

int limit = 10;
int hits = 0;
std::vector<int> values = {4, 12, 15, 7};

auto record = /* lambda here */;

for (int value : values) {
    record(value);
}
            """,
            styles,
        ),
        part("c", q4c, 5, styles),
        code(
            """
use std::collections::HashMap;

let rows = vec![
    (String::from("tea"), 2.00),
    (String::from("tea"), 1.50),
    (String::from("cake"), 3.25),
];

let mut totals: HashMap<String, f64> = HashMap::new();

for (name, price) in rows {
    /* update totals */
}
            """,
            styles,
        ),
        part("d", q4d, 5, styles),
        code(
            """
struct Countdown {
    current: i32,
}

impl Iterator for Countdown {
    type Item = i32;

    fn next(&mut self) -> Option<Self::Item> {
        /* complete */
    }
}
            """,
            styles,
        ),
        part("e", q4e, 5, styles),
        code(
            """
#include <stdio.h>

void print_count(int values[]) {
    size_t count = sizeof(values) / sizeof(values[0]);
    printf("%zu\\n", count);
}

int main(void) {
    int values[5] = {1, 2, 3, 4, 5};
    print_count(values);
}
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
        *answer_part("a", q1a, 5, "Use strtol, then check whether no digits were consumed, whether trailing characters remain, whether errno reports range trouble, and whether the value is within the accepted int range.", styles),
        code(
            """
if (end == text) {
    return 0;
}
if (*end != '\\0') {
    return 0;
}
if (errno == ERANGE || value <= 0 || value > INT_MAX) {
    return 0;
}
            """,
            styles,
        ),
        *answer_part("b", q1b, 5, "Check fopen before using the stream. Use strerror(errno) only after the failed call. fgets reads at most sizeof line - 1 characters and adds a terminator when it succeeds.", styles),
        code(
            """
if (fp == NULL) {
    fprintf(stderr, "cannot open %s: %s\\n", path, strerror(errno));
    return 1;
}

if (fgets(line, sizeof line, fp) == NULL) {
    if (ferror(fp)) {
        fprintf(stderr, "read error: %s\\n", strerror(errno));
    }
    fclose(fp);
    return 1;
}

printf("%s", line);
fclose(fp);
return 0;
            """,
            styles,
        ),
        *answer_part("c", q1c, 4, "The helper should be static in stack.c so it has internal linkage. The public function should have a prototype in the header; extern is optional on a function prototype but may be written for clarity.", styles),
        code(
            """
/* stack.c */
static Node *make_node(char value);
Stack push(Stack stack, char value);

/* stack.h */
Stack push(Stack stack, char value);
            """,
            styles,
        ),
        *answer_part("d", q1d, 7, "Use a pointer to the link that leads to the current node. This handles removal from the head and from the middle with the same assignment.", styles),
        code(
            """
int remove_first(Node **head, char key) {
    Node **link = head;

    while (*link != NULL) {
        Node *current = *link;

        if (current->key == key) {
            *link = current->next;
            free(current);
            return 1;
        }

        link = &current->next;
    }

    return 0;
}
            """,
            styles,
        ),
        *answer_part("e", q1e, 4, "fgetc returns EOF both at end-of-file and on read error. After the loop, ferror tells you whether the stream saw an error.", styles),
        code(
            """
if (ferror(fp)) {
    return -1;
}

return count;
            """,
            styles,
        ),
        p("Question 2", styles, "QuestionTitle"),
        *answer_part("a", q2a, 5, "The subscript operator must return a reference so the left-hand side assignment changes the stored element. A const overload could be added for read-only objects, but the assignment case needs int&.", styles),
        code(
            """
int& operator[](unsigned int i) {
    if (i >= 4) {
        throw std::out_of_range("grade index");
    }
    return data[i];
}
            """,
            styles,
        ),
        *answer_part("b", q2b, 5, "operator<< is normally a non-member because the left operand is the stream. Returning the same stream by reference allows chaining such as std::cout << d << '\\n'.", styles),
        code(
            """
class Date {
    int day;
    int month;
    int year;

public:
    Date(int d, int m, int y) : day(d), month(m), year(y) {}
    friend std::ostream& operator<<(std::ostream& os, const Date& d);
};

std::ostream& operator<<(std::ostream& os, const Date& d) {
    os << d.day << "/" << d.month << "/" << d.year;
    return os;
}
            """,
            styles,
        ),
        *answer_part("c", q2c, 5, "Each out-of-class template definition needs template<typename T>, and the class name must be Box<T>. Template definitions normally live in the header so the compiler can instantiate them for the used types.", styles),
        code(
            """
template<typename T>
Box<T>::Box(T value) : value(value) {}

template<typename T>
T Box<T>::get() const {
    return value;
}
            """,
            styles,
        ),
        *answer_part("d", q2d, 5, "The output is B+D+D-B-. Base subobjects are constructed before the derived part. Destruction happens in the reverse order: derived destructor first, then base destructor.", styles),
        *answer_part("e", q2e, 5, "Return a unique_ptr to the base type, constructed with a derived Circle. The virtual destructor ensures deleting through a Shape pointer runs the derived destructor correctly.", styles),
        code(
            """
std::unique_ptr<Shape> make_shape(double radius) {
    return std::make_unique<Circle>(radius);
}
            """,
            styles,
        ),
        p("Question 3", styles, "QuestionTitle"),
        *answer_part("a", q3a, 5, "The output may be either input, so one lifetime parameter ties the returned borrowed string slice to both input borrowed string slices. The annotation describes the relationship; it does not extend either string's real lifetime.", styles),
        code(
            """
fn choose_label<'a>(primary: &'a str, fallback: &'a str) -> &'a str {
    if primary.is_empty() {
        fallback
    } else {
        primary
    }
}
            """,
            styles,
        ),
        *answer_part("b", q3b, 4, "The closure mutably borrows seen because it increments it. Calling a closure that mutates captured state requires a mutable closure binding, and the closure implements FnMut.", styles),
        code(
            """
let mut seen = 0;

let mut record = |word: &str| {
    if word.starts_with('a') {
        seen += 1;
    }
};

record("apple");
record("pear");
            """,
            styles,
        ),
        *answer_part("c", q3c, 5, "enumerate supplies the index, and filter_map can discard None and non-positive values while producing the kept tuple.", styles),
        code(
            """
let positives: Vec<(usize, i32)> = readings
    .iter()
    .enumerate()
    .filter_map(|(index, reading)| match reading {
        Some(value) if *value > 0 => Some((index, *value)),
        _ => None,
    })
    .collect();
            """,
            styles,
        ),
        *answer_part("d", q3d, 6, "The function returns Result so the question-mark operator can propagate either the file-read error or the parse error. Box<dyn Error> can hold either error type.", styles),
        code(
            """
fn total_file(path: &str) -> Result<i32, Box<dyn Error>> {
    let text = fs::read_to_string(path)?;
    let mut total = 0;

    for line in text.lines() {
        total += line.trim().parse::<i32>()?;
    }

    Ok(total)
}
            """,
            styles,
        ),
        *answer_part("e", q3e, 5, "Indexing with names[2] panics if there is no third element. get returns Option, and map converts the borrowed String to a borrowed string slice.", styles),
        code(
            """
fn third_name(names: &[String]) -> Option<&str> {
    names.get(2).map(|name| name.as_str())
}
            """,
            styles,
        ),
        p("Question 4", styles, "QuestionTitle"),
        *answer_part("a", q4a, 6, "The function does not know the real element type, so it must use the supplied width to calculate byte offsets. Convert the base pointer to char * so pointer arithmetic moves one byte at a time.", styles),
        code(
            """
void copy_slot(void *array, size_t from, size_t to, size_t width) {
    char *bytes = array;

    memmove(bytes + to * width, bytes + from * width, width);
}
            """,
            styles,
        ),
        *answer_part("b", q4b, 4, "Capture limit by value because the lambda only reads it. Capture hits by reference because the lambda must update the original counter.", styles),
        code(
            """
auto record = [limit, &hits](int value) {
    if (value > limit) {
        hits++;
    }
};
            """,
            styles,
        ),
        *answer_part("c", q4c, 5, "entry finds the existing total or inserts 0.0. The returned mutable reference is dereferenced so the price is added to the stored total.", styles),
        code(
            """
for (name, price) in rows {
    let total = totals.entry(name).or_insert(0.0);
    *total += price;
}
            """,
            styles,
        ),
        *answer_part("d", q4d, 5, "next returns Some(item) while the iterator can yield another value, then None when iteration is finished. The struct stores the current state.", styles),
        code(
            """
fn next(&mut self) -> Option<Self::Item> {
    if self.current <= 0 {
        None
    } else {
        let value = self.current;
        self.current -= 1;
        Some(value)
    }
}
            """,
            styles,
        ),
        *answer_part("e", q4e, 5, "In a function parameter, int values[] is adjusted to int *values. sizeof(values) is therefore the size of a pointer, not the original array. Pass the length separately.", styles),
        code(
            """
void print_count(const int values[], size_t count) {
    printf("%zu\\n", count);
}

int main(void) {
    int values[5] = {1, 2, 3, 4, 5};
    print_count(values, sizeof values / sizeof values[0]);
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
