#!/usr/bin/env python3
"""
Builds the downloadable academic CV (assets/Abdulrazaq-Zubair-CV.docx and .pdf).

Publications, presentations and awards are read from data/*.js so the CV and
the website never drift apart. Everything else (profile, education,
appointments, ...) is defined in the CONTENT section below.

Run locally (Windows with Microsoft Word for the PDF export):
    pip install python-docx pywin32
    python scripts/build_cv.py
"""

import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
DOCX_OUT = ROOT / "assets" / "Abdulrazaq-Zubair-CV.docx"
PDF_OUT = ROOT / "assets" / "Abdulrazaq-Zubair-CV.pdf"

ACCENT = RGBColor(0x1F, 0x3A, 0x5F)
MUTED = RGBColor(0x55, 0x55, 0x55)
FONT = "Calibri"


def load_js_array(name: str, var: str) -> list[dict]:
    text = (ROOT / "data" / name).read_text(encoding="utf-8")
    m = re.search(re.escape(f"window.{var} = ") + r"(\[.*\]);", text, re.S)
    if not m:
        raise SystemExit(f"Could not find {var} array in data/{name}")
    return json.loads(m.group(1))


def by_year(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda e: -(e.get("year") or 0))


# ============================================================================
# CONTENT
# ============================================================================

NAME = "Abdulrazaq A. Zubair"
TAGLINE = "Lecturer  ·  MRI Specialist Radiographer  ·  Medical Imaging Researcher"
AFFILIATIONS = [
    "Federal University of Health Sciences, Azare (FUHSA), Nigeria",
    "African Institute for Research Advancement & Innovation (AIRA Africa)",
]
CONTACT_LINES = [
    [("aazubair01@gmail.com", "mailto:aazubair01@gmail.com"),
     ("abdulrazaq.zubair@fuhsa.edu.ng", "mailto:abdulrazaq.zubair@fuhsa.edu.ng"),
     ("aazubair@airaafrica.com", "mailto:aazubair@airaafrica.com")],
    [("+234 818 981 7182 (WhatsApp)", None), ("+234 806 050 2348", None)],
    [("aazubair01.github.io/Resume", "https://aazubair01.github.io/Resume/"),
     ("Google Scholar", "https://scholar.google.com/citations?user=JNqveLcAAAAJ"),
     ("GitHub: AAZubair01", "https://github.com/AAZubair01"),
     ("airaafrica.com", "https://www.airaafrica.com")],
]

PROFILE = (
    "Lecturer II at the Federal University of Health Sciences, Azare, and Executive Director of "
    "AIRA Africa. MRI specialist radiographer and medical imaging researcher with over nine years "
    "of clinical experience across MRI, CT, general radiography and ultrasound. My work sits at the "
    "intersection of clinical imaging, neuroimaging and artificial intelligence, with a focus on "
    "patient safety, quality assurance, workflow optimization and equitable access to diagnostic "
    "imaging in resource-limited settings. Author of 13 journal and conference/workshop papers, "
    "including MICCAI satellite-workshop and Springer LNCS contributions; recipient of MICCAI Health "
    "Equity, Open Data and Travel awards. Project Lead of the MICCAI 2026 Health Equity project for "
    "Africa, developing AI tools for pre-MRI safety screening, image quality optimization and digital "
    "data recording in Nigerian imaging centres. Currently pursuing a PhD in Medical Radiography at "
    "Bayero University Kano on AI-assisted workflow enhancement in MRI, with emphasis on safety and "
    "image quality optimization."
)

EDUCATION = [
    ("PhD, Medical Radiography (in progress)", "Bayero University Kano, Nigeria", "2023 – present"),
    ("Postgraduate Diploma, Magnetic Resonance Imaging", "Institute of Radiography, Abuja", "2023 – 2024"),
    ("Postgraduate Diploma, Medical Ultrasound", "Institute of Radiography, Kano", "2022 – 2023"),
    ("MSc, Nuclear Physics", "Bayero University Kano, Nigeria", "2017 – 2022"),
    ("Bachelor of Radiography (B.Rad.)", "Bayero University Kano, Nigeria", "2010 – 2016"),
]

ACADEMIC = [
    ("Executive Director", "African Institute for Research Advancement & Innovation (AIRA Africa)",
     "2026 – present", [
         "Coordinate the institute's research, mentorship and outreach programmes.",
         "Lead the institute's online instructional activities.",
     ]),
    ("Lecturer II", "Federal University of Health Sciences, Azare", "2025 – present", [
        "Deliver lectures and clinical tutorials in general radiography and magnetic resonance imaging.",
        "Supervise students and contribute to curriculum development.",
        "Support interdisciplinary research, professional mentorship and departmental outreach.",
    ]),
]

CLINICAL = [
    ("Team Lead Radiographer (part-time, alongside academic appointment)",
     "Medserve Kano Diagnostic Center / Aminu Kano Teaching Hospital, Kano", "2019 – present", [
         "Coordinate MRI, CT, X-ray and ultrasound services.",
         "Oversee QA/QC, radiation safety and RIS/PACS workflows.",
         "Mentor student and intern radiographers.",
     ]),
    ("Chief Radiographer", "Mercury Medical Diagnostic Center", "Dec 2018 – Jan 2024", [
        "Supervised radiography staff and coordinated departmental service delivery.",
        "Managed clinical scheduling, workflow and resource allocation.",
        "Developed and implemented standard operating procedures (SOPs) for radiographic services.",
    ]),
    ("Radiographer, National Youth Service Corps (NYSC)",
     "Federal Medical Centre, Birnin Kudu, Jigawa State", "2017 – 2018", []),
    ("Intern Radiographer", "Federal Medical Centre, Birnin Kudu, Jigawa State", "2016 – 2017", []),
]

INTERESTS = (
    "Medical radiography and imaging physics; MRI acquisition and optimization; diagnostic "
    "ultrasound; CT and radiation protection; quality assurance; neuroimaging; AI-assisted medical "
    "imaging; imaging informatics; equitable access to diagnostic services."
)

DEVELOPMENT = [
    ("SPARK Academy — Sprint AI Training for African Medical Imaging", "2025"),
    ("Neuroscience Workshop, African Brain Data Science Academy (ABDSA)", "2025"),
    ("SWIM Programme, Consortium for Advancement of MRI Research and Education in Africa", "2024, 2025"),
]

CERTIFICATIONS = [
    ("Radiation Safety Officer, Nigerian Nuclear Regulatory Authority (NNRA)", "2025"),
    ("Computed Tomography (CT) Certification", "2016"),
]

SKILLS = [
    ("Clinical imaging", "MRI and CT protocol optimization; ultrasound; general radiography"),
    ("Quality & safety", "QA/QC programmes; radiation protection; MRI safety screening"),
    ("Informatics", "RIS/PACS and LIS workflow management"),
    ("Data science", "Python, data processing and visualization; deep learning for medical imaging"),
    ("Research", "Study design, scientific writing, mentorship and teaching"),
]

LANGUAGES = "English (fluent)  ·  Hausa (native)  ·  Arabic (intermediate)"


# ============================================================================
# DOCX HELPERS
# ============================================================================

def bottom_border(paragraph, color="1F3A5F", size=8):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    p_pr.append(borders)


def add_hyperlink(paragraph, text, url, size=None, color=ACCENT, italic=False, bold=False):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                          is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    c = OxmlElement("w:color")
    c.set(qn("w:val"), str(color))
    r_pr.append(c)
    if size:
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(size * 2)))
        r_pr.append(sz)
    if italic:
        r_pr.append(OxmlElement("w:i"))
    if bold:
        r_pr.append(OxmlElement("w:b"))
    run.append(r_pr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def spacing(p, before=0, after=0, line=1.08):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line


def run(p, text, bold=False, italic=False, size=None, color=None):
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    if color is not None:
        r.font.color.rgb = color
    return r


class CV:
    def __init__(self):
        self.doc = Document()
        sec = self.doc.sections[0]
        sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
        sec.left_margin = sec.right_margin = Cm(2.0)
        sec.top_margin, sec.bottom_margin = Cm(1.7), Cm(1.7)
        self.text_width = sec.page_width - sec.left_margin - sec.right_margin

        normal = self.doc.styles["Normal"]
        normal.font.name = FONT
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        normal.font.size = Pt(10.5)
        self._footer()

    def _footer(self):
        p = self.doc.sections[0].footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(p, f"{NAME}  |  Academic Curriculum Vitae  |  Page ", size=8.5, color=MUTED)
        for code in ("PAGE", None, "NUMPAGES"):
            if code is None:
                run(p, " of ", size=8.5, color=MUTED)
                continue
            r = run(p, "", size=8.5, color=MUTED)
            for kind, val in (("begin", None), ("instr", code), ("end", None)):
                if kind == "instr":
                    el = OxmlElement("w:instrText")
                    el.set(qn("xml:space"), "preserve")
                    el.text = val
                else:
                    el = OxmlElement("w:fldChar")
                    el.set(qn("w:fldCharType"), kind)
                r._r.append(el)

    def header(self):
        p = self.doc.add_paragraph()
        spacing(p, after=1)
        run(p, NAME.upper(), bold=True, size=20, color=ACCENT)
        p = self.doc.add_paragraph()
        spacing(p, after=3)
        run(p, TAGLINE, size=10.5, color=MUTED)
        for aff in AFFILIATIONS:
            p = self.doc.add_paragraph()
            spacing(p)
            run(p, aff, size=10)
        for line in CONTACT_LINES:
            p = self.doc.add_paragraph()
            spacing(p, before=1)
            for i, (text, url) in enumerate(line):
                if i:
                    run(p, "  ·  ", size=9.5, color=MUTED)
                if url:
                    add_hyperlink(p, text, url, size=9.5)
                else:
                    run(p, text, size=9.5)

    def section(self, title):
        p = self.doc.add_paragraph()
        spacing(p, before=11, after=4)
        run(p, title.upper(), bold=True, size=11, color=ACCENT)
        bottom_border(p)
        p.paragraph_format.keep_with_next = True

    def dated(self, title, sub, dates, bullets=(), title_italic_suffix=None):
        p = self.doc.add_paragraph()
        spacing(p, before=3)
        p.paragraph_format.tab_stops.add_tab_stop(self.text_width, WD_TAB_ALIGNMENT.RIGHT)
        p.paragraph_format.keep_with_next = True
        run(p, title, bold=True)
        run(p, "\t" + dates, color=MUTED, size=10)
        if sub:
            p = self.doc.add_paragraph()
            spacing(p)
            p.paragraph_format.keep_with_next = bool(bullets)
            run(p, sub, italic=True, color=MUTED, size=10)
        for i, b in enumerate(bullets):
            p = self.doc.add_paragraph(style="List Bullet")
            spacing(p)
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.keep_with_next = i < len(bullets) - 1
            run(p, b, size=10)

    def simple_dated(self, text, date, url=None, detail=None):
        p = self.doc.add_paragraph()
        spacing(p, before=1)
        p.paragraph_format.tab_stops.add_tab_stop(self.text_width, WD_TAB_ALIGNMENT.RIGHT)
        p.paragraph_format.keep_with_next = bool(detail)
        if url:
            add_hyperlink(p, text, url, color="000000")
        else:
            run(p, text)
        run(p, "\t" + date, color=MUTED, size=10)
        if detail:
            p = self.doc.add_paragraph()
            spacing(p, after=2)
            p.paragraph_format.left_indent = Cm(0.4)
            p.paragraph_format.right_indent = Cm(1.5)
            run(p, detail, italic=True, size=9.5, color=MUTED)

    def para(self, text, size=10.5, after=0):
        p = self.doc.add_paragraph()
        spacing(p, after=after, line=1.12)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run(p, text, size=size)

    def note(self, text):
        p = self.doc.add_paragraph()
        spacing(p, after=3)
        run(p, text, italic=True, size=9, color=MUTED)

    def numbered(self, n, title, url, tail_parts):
        p = self.doc.add_paragraph()
        spacing(p, before=2, line=1.05)
        pf = p.paragraph_format
        pf.left_indent = Cm(0.75)
        pf.first_line_indent = Cm(-0.75)
        pf.tab_stops.add_tab_stop(Cm(0.75))
        run(p, f"{n}.\t", size=10)
        if url:
            add_hyperlink(p, title, url, size=10, color="000000")
        else:
            run(p, title, size=10)
        run(p, ". ", size=10)
        for text, italic in tail_parts:
            run(p, text, italic=italic, size=10, color=MUTED)

    def labelled(self, label, text):
        p = self.doc.add_paragraph()
        spacing(p, before=1)
        p.paragraph_format.left_indent = Cm(3.4)
        p.paragraph_format.first_line_indent = Cm(-3.4)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(3.4))
        run(p, label + "\t", bold=True, size=10)
        run(p, text, size=10)

    def save(self, path):
        self.doc.core_properties.author = NAME
        self.doc.core_properties.title = f"{NAME} — Academic Curriculum Vitae"
        self.doc.save(path)


# ============================================================================
# BUILD
# ============================================================================

def build() -> None:
    pubs = by_year(load_js_array("publications.js", "PUBLICATIONS"))
    talks = by_year(load_js_array("presentations.js", "PRESENTATIONS"))
    acts = by_year(load_js_array("activities.js", "ACTIVITIES"))

    cv = CV()
    cv.header()

    cv.section("Profile")
    cv.para(PROFILE)

    cv.section("Education")
    for degree, inst, dates in EDUCATION:
        cv.dated(degree, inst, dates)

    cv.section("Academic Appointments and Leadership")
    for args in ACADEMIC:
        cv.dated(*args)

    cv.section("Clinical Experience")
    for args in CLINICAL:
        cv.dated(*args)

    cv.section("Research and Teaching Interests")
    cv.para(INTERESTS)

    cv.section(f"Publications ({len(pubs)})")
    cv.note("Journal articles and peer-reviewed conference/workshop papers, most recent first. "
            "Titles link to the publisher, proceedings or scholarly record; preprint versions are listed once.")
    for i, p in enumerate(pubs, 1):
        tail = [(p.get("venue", ""), True)]
        if p.get("details"):
            tail.append((", " + p["details"], False))
        tail.append((f", {p['year']}." if p.get("year") else ".", False))
        if p.get("note"):
            tail.append((f" [{p['note']}]", False))
        cv.numbered(i, p["title"], p.get("url"), tail)

    cv.section(f"Conference Abstracts and Presentations ({len(talks)})")
    for i, t in enumerate(talks, 1):
        tail = [(t.get("event", ""), True), (f". {t.get('status', '')}", False)]
        if t.get("note"):
            tail.append((f"; {t['note'].lower()}", False))
        tail.append((".", False))
        cv.numbered(i, t["title"], t.get("url"), tail)

    cv.section("Awards and Grants")
    awards = [a for a in acts if a.get("year")]
    for a in awards:
        cv.simple_dated(a["text"], str(a["year"]), a.get("url"), a.get("detail"))

    cv.section("Professional Development")
    for text, date in DEVELOPMENT:
        cv.simple_dated(text, date)

    cv.section("Professional Certifications and Memberships")
    for text, date in CERTIFICATIONS:
        cv.simple_dated(text, date)
    for a in acts:
        if not a.get("year"):
            cv.simple_dated(a["text"], "")

    cv.section("Skills")
    for label, text in SKILLS:
        cv.labelled(label, text)

    cv.section("Languages")
    cv.para(LANGUAGES)

    cv.section("Referees")
    cv.para("Available on request.")

    cv.save(DOCX_OUT)
    print(f"Wrote {DOCX_OUT.relative_to(ROOT)}")


def export_pdf() -> None:
    try:
        import win32com.client  # Windows + Microsoft Word only
    except ImportError:
        print("pywin32 not installed — skipped PDF export (open the .docx in Word and Save As PDF).")
        return
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(str(DOCX_OUT))
        doc.Fields.Update()
        doc.SaveAs2(str(PDF_OUT), FileFormat=17)
        doc.Close(False)
    finally:
        word.Quit()
    print(f"Wrote {PDF_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
    if "--no-pdf" not in sys.argv:
        export_pdf()
