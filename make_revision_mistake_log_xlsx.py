from __future__ import annotations

import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "revision-mistake-log.xlsx"

TRACKER_COLUMNS = ["Topic sheet", "Question number", "Topic", "Redo prompt", "Completed"]
TRACKER_ROWS = [
    ["C Pointers and Memory", "1", "Pointer basics", "For `int x = 4; int *p = &x;`, state only what `x` is.", ""],
    ["C Pointers and Memory", "5", "`sizeof` vs `strlen`", "For `char s[20] = \"Hello\";`, explain only why `strlen(s)` is 5.", "Yes"],
    ["C Pointers and Memory", "6", "Out-of-bounds access", "List three possible results of writing past the end of an array in C.", "Yes"],
    ["C Pointers and Memory", "7", "`malloc` safety check", "Write only the allocation and `NULL` check for an `int *a` array of size `n`.", "Yes"],
    ["C Pointers and Memory", "8", "`strcpy` into `char *`", "Explain why `char *p; strcpy(p, \"Hello\");` is unsafe, then give one safe fix.", ""],
    ["C Pointers and Memory", "9", "Dynamic 2D array", "Write the declaration, allocation pattern, and free order for `int **X` with `R` rows and `C` columns.", ""],
    ["Rust Ownership and Borrowing", "1", "Ownership rules", "Write only the Rust ownership rule about how many owners a value can have.", "Yes"],
    ["Rust Ownership and Borrowing", "2", "Move semantics", "State what Rust prevents after a `String` has been moved.", "Yes"],
    ["Rust Ownership and Borrowing", "5", "`&str` parameters and iteration", "Write the loop header for iterating over characters in `text`, then say why `&str` is a good read-only parameter type.", "Yes"],
    ["Rust Ownership and Borrowing", "7", "Modifying a `String`", "Write the single line that appends the character `!` to a `String` called `text`.", "Yes"],
    ["Rust Ownership and Borrowing", "8", "`String` vs `&str`", "State who owns the text in `String` and who owns the text in `&str`.", "Yes"],
    ["C Files and Streams", "1", "Text vs binary streams", "State that text streams may have character translation, and binary streams do not.", ""],
    ["C Files and Streams", "3", "`scanf` basics", "State that `scanf` returns the number of items successfully assigned, and explain why it needs `&k`.", ""],
    ["C Files and Streams", "5", "Buffering and flushing", "State that output may be held in memory before it is written.", ""],
    ["C Files and Streams", "7", "`ferror` vs `feof`", "State what kind of problem `ferror(fp)` reports.", ""],
    ["C Files and Streams", "8", "`rewind` and `fseek`", "Write the code to reset the file to the start before moving 20 bytes from the beginning.", ""],
    ["C Files and Streams", "10", "Open / write / flush / close", "Write the fragment with the `if (fp == NULL)` check included.", ""],
]

RULES_COLUMNS = ["Topic sheet", "Question number", "Topic", "Correct rule"]
RULES_ROWS = [
    ["C Pointers and Memory", "1", "Pointer basics", "In `int x = 4; int *p = &x;`, `x` is the stored integer value."],
    ["C Pointers and Memory", "5", "`sizeof` vs `strlen`", "`strlen(s)` is 5 because it counts characters only up to the null terminator `\\0`, not including it."],
    ["C Pointers and Memory", "6", "Out-of-bounds access", "Three valid results are: corrupting nearby memory, changing another variable, and crashing with a segmentation fault."],
    ["C Pointers and Memory", "7", "`malloc` safety check", "Use `int *a = malloc(n * sizeof *a);` and then check `if (a == NULL)` before writing through `a`."],
    ["C Pointers and Memory", "8", "`strcpy` into `char *`", "`char *p;` is uninitialised, so it does not point to valid writable memory. A safe fix is `char p[6]; strcpy(p, \"Hello\");` or allocating with `malloc(6)` and then freeing it later."],
    ["C Pointers and Memory", "9", "Dynamic 2D array", "Declare `int **X`; allocate `X = malloc(R * sizeof *X);`, allocate each row with `X[r] = malloc(C * sizeof *X[r]);`, then `free(X[r])` for each row before `free(X)`."],
    ["Rust Ownership and Borrowing", "1", "Ownership rules", "A value can only have one owner at a time."],
    ["Rust Ownership and Borrowing", "2", "Move semantics", "After a `String` is moved, Rust prevents use-after-move by rejecting any later use of the old variable."],
    ["Rust Ownership and Borrowing", "5", "`&str` parameters and iteration", "Iterate with `for c in text.chars() { ... }`. `&str` is a good read-only parameter type because it borrows text and accepts both `String` references and string literals."],
    ["Rust Ownership and Borrowing", "7", "Modifying a `String`", "To add one `char` to a `String`, use `text.push('!')`. `+=` expects a string slice such as `\"!\"`, not a `char`."],
    ["Rust Ownership and Borrowing", "8", "`String` vs `&str`", "`String` owns the text it stores on the heap. `&str` does not own the text; it is a borrowed string slice."],
    ["C Files and Streams", "1", "Text vs binary streams", "Text streams may have character translation. Binary streams do not have character translation."],
    ["C Files and Streams", "3", "`scanf` basics", "`scanf` returns the number of items successfully assigned. It needs `&k` because it writes into the caller's variable, so it needs its address."],
    ["C Files and Streams", "5", "Buffering and flushing", "Output may be held in memory in a buffer before it is actually written to the file or device."],
    ["C Files and Streams", "7", "`ferror` vs `feof`", "`ferror(fp)` reports general file-operation errors on the stream. `feof(fp)` reports end-of-file."],
    ["C Files and Streams", "8", "`rewind` and `fseek`", "Use `rewind(fp);` first, then `fseek(fp, 20, SEEK_SET);`."],
    ["C Files and Streams", "10", "Open / write / flush / close", "Open with `fopen`, immediately check `if (fp == NULL)`, then write with `fprintf`, flush if needed, and close with `fclose`."],
]


def col_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def inline_cell(ref: str, value: str, style: int = 2) -> str:
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t>{escape(value)}</t></is></c>'


def sheet_xml(rows: list[list[str]], columns: list[str], table_range: str, rel_id: str, widths: list[float]) -> str:
    sheet_rows = [columns] + rows
    xml_rows = []
    for row_index, row in enumerate(sheet_rows, start=1):
        style = 1 if row_index == 1 else 2
        height = 24 if row_index == 1 else 54
        cells = []
        for column_index, value in enumerate(row, start=1):
            cells.append(inline_cell(f"{col_name(column_index)}{row_index}", value, style))
        xml_rows.append(f'<row r="{row_index}" ht="{height}" customHeight="1">{"".join(cells)}</row>')

    col_xml = "".join(
        f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>'
        for i, width in enumerate(widths, start=1)
    )

    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheetViews>
    <sheetView workbookViewId="0">
      <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
      <selection pane="bottomLeft"/>
    </sheetView>
  </sheetViews>
  <sheetFormatPr defaultRowHeight="15"/>
  <cols>{col_xml}</cols>
  <sheetData>{''.join(xml_rows)}</sheetData>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
  <tableParts count="1"><tablePart r:id="{rel_id}"/></tableParts>
</worksheet>'''


def table_xml(table_id: int, name: str, ref: str, columns: list[str]) -> str:
    table_cols = "".join(
        f'<tableColumn id="{i}" name="{escape(column)}"/>' for i, column in enumerate(columns, start=1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  id="{table_id}" name="{name}" displayName="{name}" ref="{ref}" totalsRowShown="0">
  <autoFilter ref="{ref}"/>
  <tableColumns count="{len(columns)}">{table_cols}</tableColumns>
  <tableStyleInfo name="TableStyleMedium2" showFirstColumn="0" showLastColumn="0" showRowStripes="1" showColumnStripes="0"/>
</table>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><color theme="1"/><name val="Calibri"/><family val="2"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1D4ED8"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border><left style="thin"><color rgb="FFD1D5DB"/></left><right style="thin"><color rgb="FFD1D5DB"/></right><top style="thin"><color rgb="FFD1D5DB"/></top><bottom style="thin"><color rgb="FFD1D5DB"/></bottom><diagonal/></border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment vertical="top" wrapText="1"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
  <dxfs count="0"/>
  <tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>
</styleSheet>'''


def build_xlsx() -> None:
    tracker_ref = f"A1:{col_name(len(TRACKER_COLUMNS))}{len(TRACKER_ROWS) + 1}"
    rules_ref = f"A1:{col_name(len(RULES_COLUMNS))}{len(RULES_ROWS) + 1}"
    now = datetime.now(timezone.utc).isoformat()

    files = {
        "[Content_Types].xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/tables/table1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>
  <Override PartName="/xl/tables/table2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>''',
        "_rels/.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>''',
        "xl/workbook.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Tracker" sheetId="1" r:id="rId1"/>
    <sheet name="Correct Rules" sheetId="2" r:id="rId2"/>
  </sheets>
</workbook>''',
        "xl/_rels/workbook.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''',
        "xl/worksheets/sheet1.xml": sheet_xml(TRACKER_ROWS, TRACKER_COLUMNS, tracker_ref, "rId1", [28, 10, 24, 52, 14]),
        "xl/worksheets/sheet2.xml": sheet_xml(RULES_ROWS, RULES_COLUMNS, rules_ref, "rId1", [28, 10, 24, 70]),
        "xl/worksheets/_rels/sheet1.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" Target="../tables/table1.xml"/></Relationships>''',
        "xl/worksheets/_rels/sheet2.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" Target="../tables/table2.xml"/></Relationships>''',
        "xl/tables/table1.xml": table_xml(1, "RevisionMistakeTracker", tracker_ref, TRACKER_COLUMNS),
        "xl/tables/table2.xml": table_xml(2, "RevisionCorrectRules", rules_ref, RULES_COLUMNS),
        "xl/styles.xml": styles_xml(),
        "docProps/app.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application></Properties>''',
        "docProps/core.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Revision Mistake Log</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>''',
    }

    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as xlsx:
        for name, content in files.items():
            xlsx.writestr(name, content)


if __name__ == "__main__":
    build_xlsx()
    print(OUTPUT)
