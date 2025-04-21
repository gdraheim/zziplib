#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=unspecified-encoding,consider-using-with

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Iterator
import sys
import re
import os
import logging

logg = logging.getLogger("MD2HTM")

def md2htm(filename: str) -> Iterator[str]:
    for line in open(filename):
        part = line.rstrip()
        part = re.sub("`([^`]*)`", "<code>\\1</code>", part)
        # part = re.sub("(?m)(</[hH][1234]>) *(\\S+)", "\\1\n\\2", part)
        part = part.replace("<br>", "<br />")
        part = part.replace("<>", " ")
        # part = part.replace("<center>", "")
        # part = part.replace("</center>", "")
        # part = part.replace("<small>", "")
        # part = part.replace("</small>", "")
        part = part.replace("<nobr>", "")
        part = part.replace("</nobr>", "")
        part = part.replace("<section>", "")
        part = part.replace("</section>", "")
        #part = part.replace("<blockquote>", "<P>")
        #part = part.replace("</blockquote>", "</P>")
        #part = part.replace("<BLOCKQUOTE>", "<P>")
        #part = part.replace("</BLOCKQUOTE>", "</P>")
        part = part.replace("<BLOCKQUOTE>", "<blockquote>")
        part = part.replace("</BLOCKQUOTE>", "</blockquote>")
        part = part.replace("<PRE>", "<pre>")
        part = part.replace("</PRE>", "</pre>")
        part = part.replace("<tt>", "<code>")
        part = part.replace("</tt>", "</code>")
        part = re.sub("(</?)H([1234]>)", "\\1h\\2", part)
        part = part.replace("<p>&nbsp;</p>", "")
        part = part.replace("&nbsp;", "")
        part = part.replace("<blockquote><ul>", "<blockquote>\n<ul>")
        part = part.replace("</ul></blockquote>", "</ul>\n</blockquote>")
        part = part.replace("<P><small>", "<P>\n<small>")
        part = part.replace("</small></P>", "</small>\n</P>")
        part = part.replace("<ul><li>", "<ul>\n<li>")
        part = part.replace("</li></ul>", "</li>\n</ul>")
        part = part.replace("<dd><ul>", "<dd>\n<ul>")
        part = part.replace("</ul></dd>", "</ul>\n</dd>")
        part = part.replace("<code><code>", "<code>")
        part = part.replace("</code></code>", "</code>")
        yield part

def main() -> int:
    import optparse # pylint: disable=deprecated-module,import-outside-toplevel
    cmdline = optparse.OptionParser()
    cmdline.add_option("-v", "--verbose", action="count", default=0, help="more logging")
    cmdline.add_option("-^", "--quiet", action="count", default=0, help="less logging")
    cmdline.add_option("-?","--version", action="count", default=0, help="version info")
    opt, args = cmdline.parse_args()
    logging.basicConfig(level = max(0, logging.INFO - 10 * opt.verbose + 10 * opt.quiet))
    if opt.version:
        print("version:", __version__)
        print("contact:", __contact__)
        print("license:", __license__)
        print("authors:", __copyright__)
        return os.EX_OK
    for arg in args:
        logg.info(" ## %s", arg)
        for part in md2htm(arg):
            print(part)
    return os.EX_OK

if __name__ == "__main__":
    sys.exit(main())
