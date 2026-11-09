"""Helpers for generating APA-7 student-paper .docx files with python-docx."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, RGBColor

FONT = "Times New Roman"
CODE_FONT = "Consolas"


def _set_font(run, size=12, bold=False, italic=False, name=FONT):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)


def _add_page_number_field(paragraph):
    run = paragraph.add_run()
    for tag, attrs, text in (("w:fldChar", {"w:fldCharType": "begin"}, None),
                             ("w:instrText", {"xml:space": "preserve"}, "PAGE"),
                             ("w:fldChar", {"w:fldCharType": "end"}, None)):
        el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(qn(k), v)
        if text:
            el.text = text
        run._element.append(el)
    _set_font(run)


def new_document():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(12)
    header_p = doc.sections[0].header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _add_page_number_field(header_p)
    return doc


def _double_space(paragraph, first_line_indent=None, space_after=0):
    pf = paragraph.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
    if first_line_indent is not None:
        pf.first_line_indent = Inches(first_line_indent)


def title_page(doc, title, author, affiliation, course, instructor, date):
    for _ in range(6):
        p = doc.add_paragraph()
        _double_space(p)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _double_space(p)
    _set_font(p.add_run(title), bold=True)
    p = doc.add_paragraph()
    _double_space(p)
    for line in (author, affiliation, course, instructor, date):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _double_space(p)
        _set_font(p.add_run(line))
    doc.add_page_break()


def heading1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _double_space(p)
    p.paragraph_format.keep_with_next = True  # never strand a heading at a page bottom
    _set_font(p.add_run(text), bold=True)
    return p


def heading2(doc, text):
    p = doc.add_paragraph()
    _double_space(p)
    p.paragraph_format.keep_with_next = True
    _set_font(p.add_run(text), bold=True)
    return p


def body(doc, text):
    """A normal APA body paragraph. Text in *...* is italicized."""
    p = doc.add_paragraph()
    _double_space(p, first_line_indent=0.5)
    for i, part in enumerate(text.split("*")):
        if part:
            _set_font(p.add_run(part), italic=(i % 2 == 1))
    return p


def code_block(doc, code, caption=None):
    if caption:
        p = doc.add_paragraph()
        _double_space(p)
        _set_font(p.add_run(caption), italic=True)
    for line in code.rstrip("\n").split("\n"):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        pf.left_indent = Inches(0.4)
        _set_font(p.add_run(line if line else " "), size=10, name=CODE_FONT)
    doc.add_paragraph()


def figure(doc, image_path, caption, number, width=6.0):
    # Keep the image, its label and its title on one page.
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(image_path, width=Inches(width))
    p = doc.add_paragraph()
    _double_space(p)
    p.paragraph_format.keep_with_next = True
    _set_font(p.add_run(f"Figure {number}"), bold=True)
    p = doc.add_paragraph()
    _double_space(p)
    _set_font(p.add_run(caption), italic=True)


def references(doc, entries, page_break_before=True, sort=True):
    # Set the break on the heading itself rather than emitting a standalone
    # page-break paragraph, which leaves a blank page when the preceding text
    # happens to end at a page boundary.
    heading = heading1(doc, "References")
    if page_break_before:
        heading.paragraph_format.page_break_before = True
    for entry in (sorted(entries) if sort else entries):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        pf.space_after = Pt(0)
        pf.left_indent = Inches(0.5)
        pf.first_line_indent = Inches(-0.5)
        for i, part in enumerate(entry.split("*")):
            if part:
                _set_font(p.add_run(part), italic=(i % 2 == 1))


def table(doc, number, caption, header, rows, widths=None):
    """An APA-style table: bold 'Table N', italic caption, then a grid."""
    p = doc.add_paragraph()
    _double_space(p)
    p.paragraph_format.keep_with_next = True
    _set_font(p.add_run(f"Table {number}"), bold=True)
    p = doc.add_paragraph()
    _double_space(p)
    p.paragraph_format.keep_with_next = True
    _set_font(p.add_run(caption), italic=True)

    t = doc.add_table(rows=len(rows) + 1, cols=len(header))
    t.style = "Table Grid"
    for j, text in enumerate(header):
        cell = t.rows[0].cells[j]
        cell.text = ""
        _set_font(cell.paragraphs[0].add_run(text), size=11, bold=True)
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            cell = t.rows[i + 1].cells[j]
            cell.text = ""
            _set_font(cell.paragraphs[0].add_run(str(text)), size=11)
    last = len(t.rows) - 1
    for i, row in enumerate(t.rows):
        tr_pr = row._tr.get_or_add_trPr()
        tr_pr.append(OxmlElement("w:cantSplit"))  # a row never breaks across pages
        for cell in row.cells:
            for par in cell.paragraphs:
                pf = par.paragraph_format
                pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
                pf.space_after = Pt(0)
                pf.space_before = Pt(0)
                pf.keep_with_next = i < last  # keep the whole table on one page
    if widths:
        for row in t.rows:
            for cell, w in zip(row.cells, widths):
                cell.width = Inches(w)
    doc.add_paragraph()
    return t
