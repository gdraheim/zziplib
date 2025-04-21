#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements,line-too-long
# pylint: disable=unspecified-encoding,invalid-name,consider-using-with,too-few-public-methods
"""
this file converts simple html text into a docbook xml variant. 
The mapping of markups and links is far from perfect. But all we
want is the docbook-to-pdf converter and similar technology being
present in the world of docbook-to-anything converters. """

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

import sys

from typing import Iterable
from zzipdoc.match import Match

M = Match

class htm2dbk_conversion_base:
    regexlist = [
        M()("</[hH]2>(.*)", "m") >> "</title>\n<subtitle>\\1</subtitle>",
        M()("<[hH]2>") >> "<sect1 id=\"--filename--\"><title>",
        M()("<[Pp]([> ])","m") >> "<para\\1",
        M()("</[Pp]>") >> "</para>",
        M()("<(pre|PRE)>") >> "<screen>",
        M()("</(pre|PRE)>") >> "</screen>",
        M()("<[hH]3>") >> "<sect2><title>",
        M()("</[hH]3>((?:.(?!<sect2>))*.?)", "s") >> "</title>\\1</sect2>",
        M()("<!doctype [^<>]*>","s") >> "",
        M()("<!DOCTYPE [^<>]*>","s") >> "",
        M()("(<\\w+\\b[^<>]*\\swidth=)(\\d+\\%)","s") >> "\\1\"\\2\"",
        M()("(<\\w+\\b[^<>]*\\s\\w+=)(\\d+)","s") >> "\\1\"\\2\"",
        M()("&&") >> "\\&amp\\;\\&amp\\;",
        M()("\\$\\<") >> "\\$\\&lt\\;",
        M()("&(\\w+[\\),])") >> "\\&amp\\;\\1",
        M()("(</?)span(\\s[^<>]*)?>","s") >> "\\1phrase\\2>",
        M()("(</?)small(\\s[^<>]*)?>","s") >> "\\1note\\2>",
        M()("(</?)(b|em|i)>")>> "\\1emphasis>",
        M()("(</?)(li)>") >> "\\1listitem>",
        M()("(</?)(ul)>") >> "\\1itemizedlist>",
        M()("(</?)(ol)>") >> "\\1orderedlist>",
        M()("(</?)(dl)>") >> "\\1variablelist>",
        M()("<dt\\b([^<>]*)>","s") >> "<varlistentry\\1><term>",
        M()("</dt\\b([^<>]*)>","s") >> "</term>",
        M()("<dd\\b([^<>]*)>","s") >> "<listitem\\1>",
        M()("</dd\\b([^<>]*)>","s") >> "</listitem></varlistentry>",
        M()("<table\\b([^<>]*)>","s") >> "<informaltable\\1><tgroup cols=\"2\"><tbody>",
        M()("</table\\b([^<>]*)>","s") >> "</tbody></tgroup></informaltable>",
        M()("(</?)tr(\\s[^<>]*)?>","s") >> "\\1row\\2>",
        M()("(</?)td(\\s[^<>]*)?>","s") >> "\\1entry\\2>",
        M()("<informaltable\\b[^<>]*>\\s*<tgroup\\b[^<>]*>\\s*<tbody>"+
          "\\s*<row\\b[^<>]*>\\s*<entry\\b[^<>]*>\\s*<informaltable\\b","s") >> "<informaltable",
        M()("</informaltable>\\s*</entry>\\s*</row>"+
          "\\s*</tbody>\\s*</tgroup>\\s*</informaltable>", "s") >> "</informaltable>",
        M()("(<informaltable[^<>]*\\swidth=\"100\\%\")","s") >> "\\1 pgwide=\"1\"",
        M()("(<tbody>\\s*<row[^<>]*>\\s*<entry[^<>]*\\s)(width=\"50\\%\")","s") >> "<colspec colwidth=\"1*\" /><colspec colwidth=\"1*\" />\n\\1\\2",
        M()("<nobr>(['`]*)<tt>") >> "<cmdsynopsis>\\1",
        M()("</tt>(['`]*)</nobr>") >> "\\1</cmdsynopsis>",
        M()("<nobr><(?:tt|code)>([`'\"])") >> "<cmdsynopsis>\\1",
        M()("<(?:tt|code)><nobr>([`'\"])") >> "<cmdsynopsis>\\1",
        M()("([`'\"])</(?:tt|code)></nobr>") >> "\\1</cmdsynopsis>",
        M()("([`'\"])</nobr></(?:tt|code)>") >> "\\1</cmdsynopsis>",
        M()("(</?)tt>") >> "\\1constant>",
        M()("(</?)code>") >> "\\1literal>",
        M()(">([^<>]+)<br>","s") >> "><highlights>\\1</highlights>",
        M()("<br>") >> "<br />",
        #        m()("<date>") >> "<sect1info><date>",
        #        m()("</date>") >> "</date></sect1info>",
        M()("<reference>") >> "<reference id=\"reference\">" >> 1,
        M()("<a\\s+href=\"((?:http|ftp|mailto):[^<>]+)\"\\s*>((?:.(?!</a>))*.)</a>","s") >> "<ulink url=\"\\1\">\\2</ulink>",
        M()("<a\\s+href=\"zziplib.html\\#([\\w_]+)\"\\s*>((?:.(?!</a>))*.)</a>","s") >> "<link linkend=\"$1\">$2</link>",
        M()("<a\\s+href=\"(zziplib.html)\"\\s*>((?:.(?!</a>))*.)</a>","s") >> "<link linkend=\"reference\">$2</link>",
        M()("<a\\s+href=\"([\\w-]+[.]html)\"\\s*>((?:.(?!</a>))*.)</a>","s") >> "<link linkend=\"\\1\">\\2</link>",
        M()("<a\\s+href=\"([\\w-]+[.](?:h|c|am|txt))\"\\s*>((?:.(?!</a>))*.)</a>","s") >> "<ulink url=\"file:\\1\">\\2</ulink>",
        M()("<a\\s+href=\"([A-Z0-9]+[.][A-Z0-9]+)\"\\s*>((?:.(?!</a>))*.)</a>","s")
        >> "<ulink url=\"file:\\1\">\\2</ulink>"
        # m()("(</?)subtitle>") >> "\\1para>"
        # $_ .= "</sect1>" if /<sect1[> ]/
        ]
    regexlist2 = [
        M()(r"<br\s*/?>") >> "",
        M()(r"(</?)em>") >> r"\1emphasis>",
        M()(r"<code>") >> "<userinput>",
        M()(r"</code>") >> "</userinput>",
        M()(r"<link>") >> "<function>",
        M()(r"</link>") >> "</function>",
        M()(r"(?s)\s*</screen>") >> "</screen>",
        # m()(r"<ul>") >> "</para><programlisting>\n",
        # m()(r"</ul>") >> "</programlisting><para>",
        M()(r"<ul>") >> "<itemizedlist>",
        M()(r"</ul>") >> "</itemizedlist>",
        # m()(r"<li>") >> "",
        # m()(r"</li>") >> ""
        M()(r"<li>") >> "<listitem><para>",
        M()(r"</li>") >> "</para></listitem>\n",
        ]
class htm2dbk_conversion(htm2dbk_conversion_base):
    def __init__(self) -> None:
        self.version = "" # str(date.today)
        self.filename = "."
    def convert(self, text: str) -> str: # $text
        txt = text.replace("<!--VERSION-->", self.version)
        for conv in self.regexlist:
            txt &= conv
        return txt.replace("--filename--", self.filename)
    def convert2(self,text: str) -> str: # $text
        txt = text.replace("<!--VERSION-->", self.version)
        for conv in self.regexlist:
            txt &= conv
        return txt

class htm2dbk_document(htm2dbk_conversion):
    """ create document, add(text) and get the value() """
    doctype = (
        '<!DOCTYPE book PUBLIC "-//OASIS//DTD'+
        ' DocBook XML V4.1.2//EN"'+"\n"+
        '       "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd">'+
        "\n")
    book_start = '<book><chapter><title>Documentation</title>'+"\n"
    book_end_chapters = '</chapter>'+"\n"
    book_end = '</book>'+"\n"
    def __init__(self) -> None:
        htm2dbk_conversion.__init__(self)
        self.text = self.doctype + self.book_start
    def add(self,text: str) -> None:
        if self.text & M()("<reference"):
            self.text += self.book_end_chapters ; self.book_end_chapters = ""
        self.text += self.convert(text).replace(
            "<br />","") & (
            M()("<link>([^<>]*)</link>") >> "<function>\\1</function>") & (
            M()("(?s)(<refentryinfo>\\s*)<sect1info>" +
                "(<date>[^<>]*</date>)</sect1info>") >> "\\1\\2")
    def value(self) -> str:
        return self.text + self.book_end_chapters + self.book_end

def htm2dbk_files(args: Iterable[str]) -> str:
    doc = htm2dbk_document()
    for filename in args:
        try:
            f = open(filename, "r")
            doc.filename = filename
            doc.add(f.read())
            f.close()
        except IOError:
            print("can not open "+filename, file=sys.stderr)
    return doc.value()

def html2docbook(text: str) -> str:
    """ the C comment may contain html markup - simulate with docbook tags """
    return htm2dbk_conversion().convert2(text)

def main() -> int:
    import optparse # pylint: disable=deprecated-module,import-outside-toplevel
    cmdline = optparse.OptionParser("%prog [options] files...")
    cmdline.add_option("-o", "--into", metavar="FILE", default="")
    opt, cmdline_args = cmdline.parse_args()
    result = htm2dbk_files(cmdline_args)
    if not opt.into:
        print(result)
    else:
        with open(opt.into, "w") as _into:
            _into.write(result)
    return 0

if __name__ == "__main__":
    sys.exit(main())
