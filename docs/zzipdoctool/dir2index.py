#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=too-many-branches,too-many-locals
# pylint: disable=unspecified-encoding,consider-using-f-string,consider-using-with

""" Searches through a directory and creates an index page for it
"""

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import List, Iterator, Optional
import logging
import os.path
import re
import xml.etree.ElementTree as ET

logg = logging.getLogger("dir2index")

def esc(text: str) -> str:
    text = text.replace(".", "\\&.")
    text = text.replace("-", "\\-")
    return text
def unescape(text: str) -> str:
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    return text
def htm(text: str) -> str:
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text
def splitname(filename: str) -> str:
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    if name.endswith(".3"): name = name[:-2]
    return name

def parse_html(filename: str) -> ET.Element:
    tree = ET.parse(filename)
    return tree.getroot()

def zzip_sorted(filenames: List[str]) -> Iterator[str]:
    for name in filenames:
        if "zziplib" in name:
            yield name
    for name in filenames:
        if "zziplib" not in name:
            yield name

def dir2(man: str, dirs: List[str], into: str) -> None: # pylint: disable=unused-argument
    text = "<html><body>" + "\n"
    file2name = {}
    file2text = {}
    for dirname in dirs:
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            file2name[filename] = splitname(filename)
            file2text[filename] = open(filepath).read()
    # find the overview filenames and generate the pages order
    overviews = []
    for filename, filetext in file2text.items():
        if " overview</title>" in filetext:
            overviews.append(filename)
    logg.warning("overviews = %s", overviews)
    logg.warning("overviews = %s", [file2name[f] for f in overviews])
    file2item = {}
    pages = []
    for overview in zzip_sorted(overviews):
        if overview not in pages:
            pages.append(overview)
        for line in file2text[overview].split("\n"):
            m = re.match('<li><a href="([^"]*)".*</li>', line)
            if m:
                filename = m.group(1)
                if filename not in file2item:
                    file2item[filename] = line
                if filename not in pages:
                    pages.append(filename)
    for filename in sorted(file2name):
        if filename not in pages:
            pages.append(filename)
    text += "<ul>"
    for page in pages:
        if page in file2item:
            text += file2item[page]
        elif page in overviews:
            name = file2name[page]
            logg.warning("page %s = %s", page, name)
            text += '<li><a href="%s"><h4>%s</h4></a></li>' % (page, name)
        else:
            name = file2name[page]
            text += '<li><a href="%s">%s</a></li>' % (page, name)
        text += "\n"
    text += "</ul>"
    text += "</body></html>" + "\n"
    writefile("%s/index.html" % into, text)

def writefile(filename: str, manpagetext: str) -> None:
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        logg.debug("mkdir %s", dirname)
        os.makedirs(dirname)
    with open(filename, "w") as f:
        f.write(manpagetext)
    logg.debug("written %s [%s]", filename, manpagetext.split("\n", 1)[0])

def main(doc: Optional[str] = None) -> int:
    from optparse import OptionParser # pylint: disable=deprecated-module,import-outside-toplevel
    cmdline = OptionParser("%prog [options] directories...", epilog=doc)
    cmdline.add_option("-v","--verbose", action="count", default=0, help="more logging")
    cmdline.add_option("-^","--quiet", action="count", default=0, help="less logging")
    cmdline.add_option("-?","--version", action="count", default=0, help="version info")
    cmdline.add_option("-o","--into", metavar="DIR", default=".",
        help="specify base directory for output [%default]")
    cmdline.add_option("-t","--make", metavar="DIR", default="man",
        help="make 'man'/'html' output pages [%default]")
    opt, args = cmdline.parse_args()
    logging.basicConfig(level = max(0, logging.WARNING - 10 * opt.verbose + 10 * opt.quiet))
    if opt.version:
        print("version:", __version__)
        print("contact:", __contact__)
        print("license:", __license__)
        print("authors:", __copyright__)
        return os.EX_OK
    # ensure commandline is compatible with "xmlto -o DIR TYPE INPUTFILE"
    make = opt.make
    dir2(make == 'man', args, opt.into) # only "html" mode is implemented
    return os.EX_OK

if __name__ == "__main__":
    import sys
    sys.exit(main(__doc__))
