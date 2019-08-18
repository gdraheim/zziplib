#! /usr/bin/env python

"""
this file converts simple html text into a docbook xml variant.
The mapping of markups and links is far from perfect. But all we
want is the docbook-to-pdf converter and similar technology being
present in the world of docbook-to-anything converters. """

from __future__ import absolute_import, print_function

import re

import sys

_regexlist = [
    ("(?m)</[hH]2>(.*)", "</title>\n<subtitle>\\1</subtitle>"),
    ("<[hH]2>", "<sect1 id=\"--filename--\"><title>"),
    ("(?m)<[Pp]([> ])", "<para\\1"),
    ("</[Pp]>", "</para>"),
    ("<(pre|PRE)>", "<screen>"),
    ("</(pre|PRE)>", "</screen>"),
    ("<[hH]3>", "<sect2><title>"),
    ("(?s)</[hH]3>((?:.(?!<sect2>))*.?)", "</title>\\1</sect2>"),
    ("(?s)<!doctype [^<>]*>", ""),
    ("(?s)<!DOCTYPE [^<>]*>", ""),
    (r"(?s)(<\w+\b[^<>]*\swidth=)(\d+\%)", "\\1\"\\2\""),
    (r"(?s)(<\w+\b[^<>]*\s\w+=)(\d+)", "\\1\"\\2\""),
    ("&&", "&amp;&amp;"),
    (r"\$\<", "$&lt;"),
    (r"&(\w+[\),])", r"&amp;\1"),
    (r"(?s)(</?)span(\s[^<>]*)?>", r"\1phrase\2>"),
    (r"(?s)(</?)small(\s[^<>]*)?>", r"\1note\2>"),
    ("(</?)(b|em|i)>", r"\1emphasis>"),
    ("(</?)(li)>", r"\1listitem>"),
    ("(</?)(ul)>", r"\1itemizedlist>"),
    ("(</?)(ol)>", r"\1orderedlist>"),
    ("(</?)(dl)>", r"\1variablelist>"),
    (r"(?s)<dt\b([^<>]*)>", r"<varlistentry\1><term>"),
    (r"(?s)</dt\b([^<>]*)>", "</term>"),
    (r"(?s)<dd\b([^<>]*)>", r"<listitem\1>"),
    (r"(?s)</dd\b([^<>]*)>", "</listitem></varlistentry>"),
    (r"(?s)<table\b([^<>]*)>", "<informaltable\\1><tgroup cols=\"2\"><tbody>"),
    (r"(?s)</table\b([^<>]*)>", "</tbody></tgroup></informaltable>"),
    (r"(?s)(</?)tr(\s[^<>]*)?>", r"\1row\2>"),
    (r"(?s)(</?)td(\s[^<>]*)?>", r"\1entry\2>"),
    (r"(?s)<informaltable\b[^<>]*>\s*<tgroup\b[^<>]*>\s*<tbody>\s*<row\b[^<>]*>\s*<entry\b[^<>]*>\s*<informaltable\b", "<informaltable"),
    (r"(?s)</informaltable>\s*</entry>\s*</row>\s*</tbody>\s*</tgroup>\s*</informaltable>", "</informaltable>"),
    ("(?s)(<informaltable[^<>]*\\swidth=\"100%\")", "\\1 pgwide=\"1\""),
    ("(?s)(<tbody>\\s*<row[^<>]*>\\s*<entry[^<>]*\\s)(width=\"50%\")", "<colspec colwidth=\"1*\" /><colspec colwidth=\"1*\" />\n\\1\\2"),
    ("<nobr>(['`]*)<tt>", "<cmdsynopsis>\\1"),
    ("</tt>(['`]*)</nobr>", "\\1</cmdsynopsis>"),
    ("<nobr><(?:tt|code)>([`\"'])", "<cmdsynopsis>\\1"),
    ("<(?:tt|code)><nobr>([`\"'])", "<cmdsynopsis>\\1"),
    ("([`\"'])</(?:tt|code)></nobr>", "\\1</cmdsynopsis>"),
    ("([`\"'])</nobr></(?:tt|code)>", "\\1</cmdsynopsis>"),
    ("(</?)tt>", "\\1constant>"),
    ("(</?)code>", "\\1literal>"),
    ("(?s)>([^<>]+)<br>", "><highlights>\\1</highlights>"),
    ("<br>", "<br />"),
    # ("<date>", "<sect1info><date>"),
    # ("</date>", "</date></sect1info>"),
    ("<reference>", "<reference id=\"reference\">"),
    ("(?s)<a\\s+href=\"((?:http|ftp|mailto):[^<>]+)\"\\s*>((?:.(?!</a>))*.)</a>", "<ulink url=\"\\1\">\\2</ulink>"),
    ("(?s)<a\\s+href=\"zziplib.html#([\\w_]+)\"\\s*>((?:.(?!</a>))*.)</a>", "<link linkend=\"\\1\">\\2</link>"),
    ("(?s)<a\\s+href=\"(zziplib.html)\"\\s*>((?:.(?!</a>))*.)</a>", "<link linkend=\"reference\">\\2</link>"),
    ("(?s)<a\\s+href=\"([\\w-]+[.]html)\"\\s*>((?:.(?!</a>))*.)</a>", "<link linkend=\"\\1\">\\2</link>"),
    ("(?s)<a\\s+href=\"([\\w-]+[.](?:h|c|am|txt))\"\\s*>((?:.(?!</a>))*.)</a>", "<ulink url=\"file:\\1\">\\2</ulink>"),
    ("(?s)<a\\s+href=\"([A-Z0-9]+[.][A-Z0-9]+)\"\\s*>((?:.(?!</a>))*.)</a>", "<ulink url=\"file:\\1\">\\2</ulink>"),
    # ("(</?)subtitle>", "\\1para>"),
    # $_ .= "</sect1>" if /<sect1[> ]/
]


def html2docbook(text, ):
    """ the C comment may contain html markup - simulate with docbook tags """
    txt = text.replace("<!--VERSION-->", '')
    for regex, replace in _regexlist:
        txt = re.sub(regex, replace, txt)
    return txt


class htm2dbk_document(object):
    """ create document, add(text) and get the value() """
    doctype = (
            '<!DOCTYPE book PUBLIC "-//OASIS//DTD' +
            ' DocBook XML V4.1.2//EN"' + "\n" +
            '       "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd">' +
            "\n")
    book_start = '<book><chapter><title>Documentation</title>' + "\n"
    book_end_chapters = '</chapter>' + "\n"
    book_end = '</book>' + "\n"

    def __init__(self):
        self.text = self.doctype + self.book_start

    def add(self, text, filename):
        if '<reference' in self.text:
            self.text += self.book_end_chapters
            self.book_end_chapters = ""

        text = html2docbook(text)\
            .replace("--filename--", filename)\
            .replace("<br />", "")
        text = re.sub("<link>([^<>]*)</link>", r"<function>\1</function>", text)
        text = re.sub(
            r"(<refentryinfo>\s*)<sect1info>(<date>[^<>]*</date>)</sect1info>",
            r"\1\2", text, flags=re.S)
        self.text += text

    def __str__(self):
        return self.text + self.book_end_chapters + self.book_end


def htm2dbk_files(args):
    doc = htm2dbk_document()
    for filename in args:
        try:
            with open(filename, "r") as f:
                doc.add(f.read(), filename)
        except IOError:
            print("can not open", filename, file=sys.stderr)
    return str(doc)


if __name__ == "__main__":
    print(htm2dbk_files(sys.argv[1:]))
