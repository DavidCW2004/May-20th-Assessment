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


OUT = Path(__file__).with_name("c-structures-dynamic-data-study-pack.pdf")


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
        title="C Structures and Dynamic Data Structures Study Pack",
    )

    story = [
        p("C Structures and Dynamic Data Structures", styles, "TopicTitle"),
        p(
            "Focused revision sheet based on ECM2433 L07 Structures and Pointers plus worksheet 4 stack practice, chosen from a red C topic not yet covered in the revision RAG tracker.",
            styles,
            "SourceText",
        ),
        p("Description: What You Need To Know", styles, "BlueHeading"),
        p("1. What a struct is", styles, "DarkHeading"),
        p(
            "A <font face=\"Courier\">struct</font> groups related fields into one compound type. It is the closest thing basic C has to a simple class-style record.",
            styles,
        ),
        code(
            """
struct Book {
    char title[181];
    char author[51];
    float price;
    int pages;
};

struct Book book = {
    "The Joy of Programming in C",
    "A. Programmer",
    12.99f,
    384
};
            """,
            styles,
        ),
        p(
            "The fields live inside the same object. Use dot notation when you have the struct object itself.",
            styles,
        ),
        code(
            """
book.price = 10.99f;
printf("%d\\n", book.pages);
            """,
            styles,
        ),
        p("2. <font face=\"Courier\">typedef</font> with structs", styles, "DarkHeading"),
        p(
            "<font face=\"Courier\">typedef</font> creates a shorter type name. It lets you write <font face=\"Courier\">Book</font> instead of <font face=\"Courier\">struct Book</font>.",
            styles,
        ),
        code(
            """
typedef struct Book {
    char title[181];
    char author[51];
    float price;
    int pages;
} Book;

Book first;
Book library[20];
            """,
            styles,
        ),
        p(
            "The name after <font face=\"Courier\">struct</font> is the tag. The final name before the semicolon is the typedef alias.",
            styles,
        ),
        p("3. Struct assignment, arrays, and function parameters", styles, "DarkHeading"),
        p(
            "Structs can be assigned, passed to functions, returned from functions, and stored in arrays. Assignment copies the fields.",
            styles,
        ),
        code(
            """
Book copy = first;

int page_count(Book b) {
    return b.pages;
}

Book make_book(void) {
    Book b = {"Title", "Author", 9.99f, 200};
    return b;
}
            """,
            styles,
        ),
        p(
            "Passing a struct by value copies it. For a large struct, use a pointer if the function needs to modify it, or a pointer to const if it only needs to read it.",
            styles,
        ),
        code(
            """
void discount(Book *b) {
    b->price *= 0.9f;
}

int pages_of(const Book *b) {
    return b->pages;
}
            """,
            styles,
        ),
        p("4. Dot vs arrow", styles, "DarkHeading"),
        p(
            "Use dot when you have a struct object. Use arrow when you have a pointer to a struct. The arrow form is shorthand for dereference then dot.",
            styles,
        ),
        code(
            """
Book first;
Book *second = malloc(sizeof *second);

first.price = 8.99f;
second->price = 8.99f;      /* same as (*second).price */

free(second);
            """,
            styles,
        ),
        bullets(
            [
                "<font face=\"Courier\">book.price</font> means the field of a struct object.",
                "<font face=\"Courier\">book_pointer-&#62;price</font> means the field of the struct being pointed at.",
                "After <font face=\"Courier\">malloc</font>, check for <font face=\"Courier\">NULL</font> before using the pointer.",
            ],
            styles,
        ),
        p("5. Linked-list nodes", styles, "DarkHeading"),
        p(
            "A linked list is made from nodes. Each node stores data plus a pointer to the next node. The nodes do not need to be next to each other in memory.",
            styles,
        ),
        code(
            """
typedef struct Node {
    char data;
    struct Node *next;
} Node;

Node *root = NULL;  /* empty list */
            """,
            styles,
        ),
        p(
            "The self-reference must be a pointer. A node cannot directly contain a full node of the same type, because that would require infinite size.",
            styles,
        ),
        p("6. Creating and freeing nodes", styles, "DarkHeading"),
        p(
            "A dynamic node is usually created with <font face=\"Courier\">malloc</font>, initialised, linked into a list, and later freed exactly once.",
            styles,
        ),
        code(
            """
Node *new_node(char data) {
    Node *node = malloc(sizeof *node);
    if (node == NULL) {
        return NULL;
    }

    node->data = data;
    node->next = NULL;
    return node;
}
            """,
            styles,
        ),
        p(
            "Use <font face=\"Courier\">sizeof *node</font> so the allocation stays correct if the pointer's target type changes.",
            styles,
        ),
        p("7. Inserting at the front", styles, "DarkHeading"),
        p(
            "To add a node at the front, point the new node at the old root first, then update the root.",
            styles,
        ),
        code(
            """
Node *push_front(Node *root, char data) {
    Node *node = new_node(data);
    if (node == NULL) {
        return root;
    }

    node->next = root;
    return node;
}

root = push_front(root, 'Q');
root = push_front(root, 'C');
            """,
            styles,
        ),
        p(
            "The order matters. If you overwrite <font face=\"Courier\">root</font> before saving the old root in <font face=\"Courier\">node-&#62;next</font>, you lose the rest of the list.",
            styles,
        ),
        p("8. Inserting after a node", styles, "DarkHeading"),
        p(
            "When inserting in the middle, first link the new node to the tail, then link the previous node to the new node.",
            styles,
        ),
        code(
            """
void insert_after(Node *previous, Node *node) {
    node->next = previous->next;
    previous->next = node;
}
            """,
            styles,
        ),
        p(
            "Doing those assignments in the opposite order can lose the tail of the list because the only pointer to it has been overwritten.",
            styles,
        ),
        p("9. Stack with a linked list", styles, "DarkHeading"),
        p(
            "A stack is last in, first out. With a linked list, pushing adds a new node at the front. Popping removes the front node, returns its data, updates the root, and frees the removed node.",
            styles,
        ),
        code(
            """
char pop(Node **root) {
    if (*root == NULL) {
        return '\\0';
    }

    Node *old = *root;
    char data = old->data;
    *root = old->next;
    free(old);
    return data;
}
            """,
            styles,
        ),
        p(
            "The parameter is a pointer to the root pointer because <font face=\"Courier\">pop</font> must change the caller's root.",
            styles,
        ),
        p("10. Arrays vs linked lists", styles, "DarkHeading"),
        bullets(
            [
                "Arrays are contiguous, so indexing is fast: <font face=\"Courier\">array[i]</font> can jump straight to element <font face=\"Courier\">i</font>.",
                "Arrays are awkward for insertion and deletion in the middle because elements may need to move.",
                "Linked lists can grow one node at a time and insert/delete by changing pointers.",
                "Linked lists are slower for lookup by position because you must start at the root and follow links.",
            ],
            styles,
        ),
        p("Practice Questions", styles, "BlueHeading"),
        numbered(
            [
                "Define a <font face=\"Courier\">Book</font> struct with title, author, price, and page-count fields, then initialise one value.",
                "Rewrite a <font face=\"Courier\">struct Book</font> definition so the type can be used as <font face=\"Courier\">Book b;</font>.",
                "Given <font face=\"Courier\">Book book;</font> and <font face=\"Courier\">Book *ptr;</font>, write one assignment to <font face=\"Courier\">price</font> using dot and one using arrow.",
                "Write a function header for a function that reads a <font face=\"Courier\">Book</font> without copying or modifying it.",
                "Define a linked-list node that stores one character and a pointer to the next node.",
                "Complete <font face=\"Courier\">new_node</font> so it allocates a node, handles allocation failure, stores the character, and sets the next pointer to empty.",
                "Starting with <font face=\"Courier\">root</font> pointing at a list, write the two pointer assignments that insert <font face=\"Courier\">new_node</font> at the front.",
                "For insertion after <font face=\"Courier\">previous</font>, choose the safe order for updating <font face=\"Courier\">new_node-&#62;next</font> and <font face=\"Courier\">previous-&#62;next</font>.",
                "Complete a <font face=\"Courier\">pop</font> function for a linked-list stack so it updates the caller's root pointer and frees the removed node.",
                "For a workload that often inserts items in the middle but rarely indexes by number, choose between an array and a linked list and justify the choice.",
            ],
            styles,
        ),
        PageBreak(),
        p("Mark Scheme", styles, "TopicTitle"),
        p(
            "Use this after attempting the questions. Good answers should show the pointer update order, not just name the data structure.",
            styles,
            "SourceText",
        ),
        numbered(
            [
                "A valid answer defines fields such as <font face=\"Courier\">char title[181]</font>, <font face=\"Courier\">char author[51]</font>, <font face=\"Courier\">float price</font>, and <font face=\"Courier\">int pages</font>, then initialises them in order.",
                "Expected pattern: <font face=\"Courier\">typedef struct Book { ... } Book;</font>. The final <font face=\"Courier\">Book</font> is the alias.",
                "Use <font face=\"Courier\">book.price = ...;</font> for the object and <font face=\"Courier\">ptr-&#62;price = ...;</font> for the pointer.",
                "Use a pointer to const, for example <font face=\"Courier\">int pages_of(const Book *book)</font>. This avoids copying and promises not to modify the book.",
                "Expected pattern: <font face=\"Courier\">typedef struct Node { char data; struct Node *next; } Node;</font>.",
                "Allocate with <font face=\"Courier\">malloc(sizeof *node)</font>, check for <font face=\"Courier\">NULL</font>, store <font face=\"Courier\">data</font>, set <font face=\"Courier\">next</font> to <font face=\"Courier\">NULL</font>, and return the node.",
                "Use <font face=\"Courier\">new_node-&#62;next = root;</font> before <font face=\"Courier\">root = new_node;</font>.",
                "Use <font face=\"Courier\">new_node-&#62;next = previous-&#62;next;</font> before <font face=\"Courier\">previous-&#62;next = new_node;</font>.",
                "Use a pointer to the root pointer, save the old root, move the root to <font face=\"Courier\">old-&#62;next</font>, save the data, free the old node, and return the data.",
                "A linked list is better for frequent middle insertions because insertion only changes pointers. An array is better for direct indexing by position.",
            ],
            styles,
        ),
        p("Useful Code Patterns", styles, "BlueHeading"),
        code(
            """
#include <stdlib.h>

typedef struct Node {
    char data;
    struct Node *next;
} Node;

Node *new_node(char data) {
    Node *node = malloc(sizeof *node);
    if (node == NULL) {
        return NULL;
    }

    node->data = data;
    node->next = NULL;
    return node;
}

Node *push_front(Node *root, char data) {
    Node *node = new_node(data);
    if (node == NULL) {
        return root;
    }

    node->next = root;
    return node;
}

char pop(Node **root) {
    if (*root == NULL) {
        return '\\0';
    }

    Node *old = *root;
    char data = old->data;
    *root = old->next;
    free(old);
    return data;
}
            """,
            styles,
        ),
    ]

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUT)
