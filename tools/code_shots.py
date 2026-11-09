"""Render source excerpts as editor-style screenshots for the report appendix.

Each excerpt becomes an HTML page (pygments highlighting, real line numbers,
a file-name tab) that headless Edge saves as a PNG in report/screenshots/.
Run from the repository root:  python tools/code_shots.py
"""

import os
import subprocess
import tempfile

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CppLexer, SmalltalkLexer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "report", "screenshots")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# (output name, file, first line, last line)
SHOTS = [
    ("01_cpp_ride_h.png", "cpp/ride.h", 1, 34),
    ("02_cpp_subclasses_h.png", "cpp/ride.h", 36, 64),
    ("03_cpp_ride_cpp.png", "cpp/ride.cpp", 22, None),
    ("04_cpp_driver_h.png", "cpp/driver.h", 1, None),
    ("05_cpp_main.png", "cpp/main.cpp", 14, 43),
    ("06_st_ride.png", "smalltalk/RideSharing.st", 32, 73),
    ("07_st_subclasses.png", "smalltalk/RideSharing.st", 75, 114),
    ("08_st_driver.png", "smalltalk/RideSharing.st", 116, 165),
    ("09_st_main.png", "smalltalk/main.st", 1, 36),
]

LINE_PX = 19      # matches the CSS line-height below
WIDTH_PX = 1100  # wide enough for any line; the right side is cropped after

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin: 0; background: #ffffff; font-family: Consolas, monospace; }}
.tab {{ background: #f3f3f3; border-bottom: 1px solid #d0d0d0; padding: 7px 14px;
        font: 13px 'Segoe UI', sans-serif; color: #333; }}
.tab b {{ color: #000; }}
.highlight, .highlighttable {{ font-size: 13.5px; line-height: {line}px; }}
.highlighttable {{ border-spacing: 0; margin: 6px 0; }}
.linenos {{ color: #9a9a9a; text-align: right; padding: 0 12px 0 14px;
            border-right: 1px solid #e3e3e3; user-select: none; }}
.code {{ padding-left: 14px; }}
pre {{ margin: 0; font-family: Consolas, monospace; }}
{css}
</style></head><body>
<div class="tab"><b>{name}</b> &nbsp; lines {first}-{last}</div>
{code}
</body></html>"""


def render(name, rel, first, last):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        lines = f.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    last = last or len(lines)
    excerpt = "\n".join(lines[first - 1:last]) + "\n"
    lexer = SmalltalkLexer() if rel.endswith(".st") else CppLexer()
    fmt = HtmlFormatter(linenos="table", linenostart=first, style="vs")
    page = PAGE.format(line=LINE_PX, css=fmt.get_style_defs(".highlight"), name=rel,
                       first=first, last=last, code=highlight(excerpt, lexer, fmt))
    height = 34 + 14 + LINE_PX * (last - first + 1)

    with tempfile.TemporaryDirectory() as tmp:
        html = os.path.join(tmp, "page.html")
        with open(html, "w", encoding="utf-8") as f:
            f.write(page)
        out = os.path.join(OUT, name)
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars",
                        f"--user-data-dir={os.path.join(tmp, 'profile')}",
                        "--force-device-scale-factor=2", f"--window-size={WIDTH_PX},{height}",
                        f"--screenshot={out}", "file:///" + html.replace("\\", "/")],
                       check=True, capture_output=True, timeout=60)
    trim(out)
    print("wrote", out, f"({rel} {first}-{last})")


def trim(path, margin=16, tab_px=70):
    """Cut the empty white space below the last line and right of the longest
    line (the tab bar at the top is gray all the way across, so it is skipped
    when finding the right edge). Every image keeps the same scale."""
    from PIL import Image, ImageChops
    img = Image.open(path).convert("RGB")
    diff = ImageChops.difference(img, Image.new("RGB", img.size, "white"))
    bottom = diff.getbbox()[3]
    right = diff.crop((0, tab_px, img.width, img.height)).getbbox()[2]
    img.crop((0, 0, min(img.width, right + 3 * margin), min(img.height, bottom + margin))).save(path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for shot in SHOTS:
        render(*shot)
