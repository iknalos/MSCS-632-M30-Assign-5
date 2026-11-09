"""Build report/Solanki_MSCS-632-M30_Assignment5_Report.docx (APA 7 student paper).

Run from the repository root:  python tools/make_report.py
Then export the PDF:          powershell tools/export_pdf.ps1 report/<name>.docx
In body text, `code` is set in Consolas and *text* in italics.
"""

import os
import re
import sys

from docx.oxml import OxmlElement
from PIL import Image
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apa  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "report", "screenshots")
OUT = os.path.join(ROOT, "report", "Solanki_MSCS-632-M30_Assignment5_Report.docx")
REPO = "https://github.com/iknalos/MSCS-632-M30-Assign-5"
TITLE = "Assignment 5: A Class-Based Ride Sharing System in Smalltalk and C++"
DATE = "November 8, 2026"


def runs(p, text):
    """Add text to a paragraph: `code` in Consolas, *italic* in italics."""
    for part in re.split(r"(`[^`]+`|\*[^*]+\*)", text):
        if not part:
            continue
        if part.startswith("`"):
            apa._set_font(p.add_run(part[1:-1]), size=11, name=apa.CODE_FONT)
        elif part.startswith("*"):
            apa._set_font(p.add_run(part[1:-1]), italic=True)
        else:
            apa._set_font(p.add_run(part))


def para(doc, text):
    p = doc.add_paragraph()
    apa._double_space(p, first_line_indent=0.5)
    runs(p, text)
    return p


def link(p, url):
    r_id = p.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                            is_external=True)
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), r_id)
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), apa.FONT)
    fonts.set(qn("w:hAnsi"), apa.FONT)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "24")
    for el in (fonts, color, underline, size):
        rpr.append(el)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = url
    r.append(t)
    h.append(r)
    p._p.append(h)


def main():
    doc = apa.new_document()
    apa.title_page(doc, TITLE, "Rahul Solanki", "University of the Cumberlands",
                   "MSCS-632-M30: Advanced Programming Language", "Jay Thom", DATE)

    apa.heading1(doc, TITLE)
    p = para(doc, "I built the same ride sharing system in GNU Smalltalk 3.2.5 and in C++17. Each version "
                  "has a `Ride` base class with three subclasses (`StandardRide`, `PremiumRide`, and "
                  "`SharedRide`, which extends `StandardRide`), a `Driver` class, a `Rider` class, and a "
                  "`RideSystem` class that gives each requested ride to the driver with the fewest rides. "
                  "Premium rides go only to drivers rated 4.8 or higher. Both programs print the same 56 "
                  "lines after their first line (Figure A14). The code is at ")
    link(p, REPO)
    runs(p, ", and the Appendix shows the code and sample runs.")

    apa.heading1(doc, "Encapsulation")
    para(doc, "C++ states access rules in each class. `Driver` keeps its rating and its `assignedRides_` "
              "list private, so other code can only add a ride with `addRide()`, count its rides, total its earnings, "
              "or get a copy of the list from `rides()`. `updateRating()` refuses values outside 1.0 to "
              "5.0, and the `Ride` constructor throws an exception for a distance of zero or less. "
              "`Ride` keeps its own fields private too, so even subclasses store a fare through the "
              "protected method `recordFare()` (Stroustrup, 2013). Smalltalk has no access keywords: an "
              "object's instance variables can be used only by its own methods, and any method can be "
              "called by anyone (Goldberg & Robson, 1983). `Driver` has no method that returns "
              "`assignedRides`, so the list cannot be reached from outside, and `rides` returns a copy. "
              "Section 6 of each run shows both checks working (Figures A11 and A13).")

    apa.heading1(doc, "Inheritance")
    para(doc, "In C++ the parent is named in the class header, as in `class SharedRide : public "
              "StandardRide`. Constructors are not inherited unless asked for, so each subclass adds a "
              "declaration such as `using Ride::Ride;` (Stroustrup, 2013). In Smalltalk a class is made by "
              "sending `subclass:` to its parent, as in `Ride subclass: StandardRide`. Subclasses use "
              "inherited instance variables directly, so `StandardRide`'s `fare` reads `distance` with no "
              "getter, and class methods are inherited as well, so one constructor, "
              "`id:from:to:miles:`, builds every kind of ride. Both versions reuse the parent's formula "
              "the same way: `SharedRide` calls `StandardRide::fare()` in C++ and `super fare` in "
              "Smalltalk, then takes 30% off.")

    apa.heading1(doc, "Polymorphism")
    para(doc, "In C++, `fare()`, `rideType()`, `needsTopDriver()`, and `rideDetails()` are `virtual` in "
              "`Ride` and marked `override` in the subclasses, and the destructor is virtual so rides are "
              "deleted correctly through `Ride` pointers. All rides sit in one "
              "`std::vector<std::shared_ptr<Ride>>`, and the loop in `main.cpp` calls `rideDetails()` and "
              "`fare()` on each, so each ride runs its own version (Figure A5). A virtual call inside a "
              "constructor runs the base version (Stroustrup, 2013), so the fare is worked out by `fare()` "
              "when needed rather than in the constructor. In Smalltalk every message is looked up in the "
              "receiver's class when it is sent (Goldberg & Robson, 1983), so no keyword is needed: the "
              "rides are kept in an `OrderedCollection`, and `rides do: [:ride | ride rideDetails]` works "
              "the same way (Figure A9). The dispatcher also asks each ride `needsTopDriver` instead of "
              "checking its class. In short, C++ makes the programmer declare access and dynamic binding "
              "and checks them when compiling, while Smalltalk applies both to every object by default.")

    apa.references(doc, [
        "Goldberg, A., & Robson, D. (1983). *Smalltalk-80: The language and its implementation*. "
        "Addison-Wesley.",
        "Stroustrup, B. (2013). *The C++ programming language* (4th ed.). Addison-Wesley.",
    ])

    # A single appendix: its figures are numbered A1, A2, ... (APA 7).
    h = apa.heading1(doc, "Appendix")
    h.paragraph_format.page_break_before = True
    apa.heading1(doc, "Screenshots of the Code and Sample Output")
    figures = [
        ("01_cpp_ride_h.png", "C++ Ride Base Class (cpp/ride.h)", None),
        ("02_cpp_subclasses_h.png", "C++ StandardRide, PremiumRide, and SharedRide Subclasses (cpp/ride.h)", None),
        ("03_cpp_ride_cpp.png", "C++ Overridden fare() and rideDetails() Methods (cpp/ride.cpp)", None),
        ("04_cpp_driver_h.png", "C++ Driver Class With a Private Ride List (cpp/driver.h)", None),
        ("05_cpp_main.png", "C++ Demo: Mixed Ride Types in One List (cpp/main.cpp)", None),
        ("06_st_ride.png", "Smalltalk Ride Base Class (smalltalk/RideSharing.st)", None),
        ("07_st_subclasses.png", "Smalltalk StandardRide, PremiumRide, and SharedRide Subclasses", None),
        ("08_st_driver.png", "Smalltalk Driver Class (smalltalk/RideSharing.st)", None),
        ("09_st_main.png", "Smalltalk Demo: Mixed Ride Types in One List (smalltalk/main.st)", None),
        ("10_cpp_run_part1.png", "C++ Version Built and Run, Part 1: Requests, Dispatch, and All Rides", 4.8),
        ("11_cpp_run_part2.png", "C++ Version, Part 2: Drivers, Riders, and Encapsulation Checks", 4.8),
        ("12_st_run_part1.png", "Smalltalk Version Run, Part 1: Requests, Dispatch, and All Rides", 4.8),
        ("13_st_run_part2.png", "Smalltalk Version, Part 2: Drivers, Riders, and Encapsulation Checks", 4.8),
        ("14_compare.png", "Both Outputs Compared: Identical After the Header Line", 6.0),
    ]
    for i, (name, caption, width) in enumerate(figures, 1):
        path = os.path.join(SHOTS, name)
        if width is None:  # code screenshot: same scale for every one
            width = min(6.0, Image.open(path).width / 300)
        apa.figure(doc, path, caption, f"A{i}", width=width)

    doc.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
