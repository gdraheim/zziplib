#! /usr/bin/python
from __future__ import print_function

""" Searches through a directory and creates an index page for it
"""

__author__ = "Guido U. Draheim"

import logging
import os.path
import re
import xml.etree.ElementTree as ET

logg = logging.getLogger("dir2index")

def esc(text):
    text = text.replace(".", "\\&.")
    text = text.replace("-", "\\-")
    return text
def unescape(text):
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    return text
def htm(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text

def parse_html(filename):
    tree = ET.parse(filename)
    return tree.getroot()

def dir2(man, dirs, into):
    text = "<html><body>" + "\n"
    for dirname in dirs:
        text += "<ul>"
        for filename in os.listdir(dirname):
            name = filename
            if name.endswith(".html"): name = name[:-5]
            if name.endswith(".htm"): name = name[:-4]
            if name.endswith(".3"): name = name[:-2]
            text += '<li><a href="%s">%s</a></li>' % (filename, name)
            text += "\n"
        text += "</ul>"
    text += "</body></html>" + "\n"
    writefile("%s/index.html" % into, text)

def writefile(filename, manpagetext):
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        logg.debug("mkdir %s", dirname)
        os.makedirs(dirname)
    with open(filename, "w") as f:
        f.write(manpagetext)
    logg.debug("written %s [%s]", filename, manpagetext.split("\n", 1)[0])

if __name__ == "__main__":
    from optparse import OptionParser
    _o = OptionParser("%prog [options] directories...")
    _o.add_option("-o","--into", metavar="DIR", default=".",
        help="specify base directory for output [%default]")
    _o.add_option("-t","--make", metavar="DIR", default="man",
        help="make 'man'/'html' output pages [%default]")
    _o.add_option("-v","--verbose", action="count", default=0,
        help="increase logging level [%default]")
    opt, args = _o.parse_args()
    logging.basicConfig(level = max(0, logging.WARNING - 10 * opt.verbose))
    # ensure commandline is compatible with "xmlto -o DIR TYPE INPUTFILE"
    make = opt.make
    dir2(make == 'man', args, opt.into)
