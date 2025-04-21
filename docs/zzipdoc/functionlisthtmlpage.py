#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=broad-exception-caught,no-else-return

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

import os
import os.path
import logging

from typing import Optional, List
from zzipdoc.match import Match
from zzipdoc.htmldoctypes import DocOptions
from zzipdoc.htmldoctypes import RefDocPart

logg = logging.getLogger(__name__)


def short(filename: str) -> str:
    while filename.startswith("../"):
        filename = filename[3:]
    if filename.startswith(os.sep):
        parts = ["",""] + filename.split(os.sep)
        return os.path.join(parts[-2], parts[-1])
    return filename

class FunctionListHtmlPage:
    """ The main part here is to create a TOC (table of contents) at the
    start of the page - linking down to the descriptions of the functions.
    Sure we need to generate anchors on the fly. Additionally, all the
    non-html (docbook-like) markup needs to be converted for ouput. -
    each element to be added should implement get_name(), get_head() and
    get_body() with the latter two having a xml_text() method."""
    _null_table100 =  '<table border="0" width="100%"' \
                     ' cellpadding="0" cellspacing="0">'
    _ul_start = '<table width="100%">'
    _ul_end = '</table>' + "\n"
    _li_start = '<tr><td valign="top">'
    _li_end = '</td></tr>' + "\n"
    http_opengroup = "http://www.opengroup.org/onlinepubs/000095399/functions/"
    http_zlib = "http://www.zlib.net/manual.html"
    toc: str
    text: str
    head: str
    body: str
    anchors: List[str]
    o: DocOptions
    not_found_in_anchors: List[str]
    def __init__(self, o: Optional[DocOptions] = None) -> None:
        self.toc = ""
        self.text = ""
        self.head = ""
        self.body = ""
        self.anchors = []
        self.o = o if o is not None else DocOptions()
        self.not_found_in_anchors = []
    def cut(self) -> None:
        self.text += ("<dt>"+self._ul_start+self.head+self._ul_end+"</dt>"+"\n"+
                      "<dd>"+self._ul_start+self.body+self._ul_end+"</dd>"+"\n")
        self.head = ""
        self.body = ""
    def add(self, entry: RefDocPart) -> None:
        name = entry.get_name()
        head_text = entry.head_xml_text() or ""
        body_text = entry.body_xml_text(name) or ""
        if not head_text:
            print("no head_text for " + (name or "?"))
            return
        try:
            prespec = entry.head_get_prespec() or ""
            callspec = entry.head_get_callspec() or ""
            namespec = entry.head_get_namespec() or ""
            if namespec:
                head_text = ("<code><b><function>"+namespec+"</function></b>"
                         +callspec+" : "+prespec+"</code>")
        except Exception as e:
            logg.info("unable to add entry: %s", e)
        try:
            extraline = ""
            title = entry.get_title()
            filename = short(entry.get_filename() or "")
            if title:
                subtitle = '&nbsp;<em>'+title+'</em>'
                extraline = (self._null_table100+'<td> '+subtitle+' </td>'+
                             '<td align="right"> '+
                             '<em><small>'+filename+'</small></em>'+
                             '</td></table>' + "\n")
            body_text = extraline + body_text
        except Exception as e:
            logg.info("unable-to add entry: %s", e)
        def link(text: str) -> str:
            return (text & Match("<function>(\\w*)</function>")
                    >> "<link>\\1</link>")
        def here(text: str) -> str:
            has_function = Match("<function>(\\w*)</function>")
            if text & has_function:
                func = has_function[1]
                self.anchors += [ func ]
                return (text & has_function
                        >> '<a name="'+"\\1"+'">'+"\\1"+'</a>')
            else:
                return text
        self.toc += self._li_start+self.sane(link(head_text))+self._li_end
        self.head += self._li_start+self.sane(here(head_text))+self._li_end
        self.body += self._li_start+self.sane(body_text)+self._li_end
    def get_title(self) -> str:
        return self.o.package+" Library Functions"
    def xml_text(self) -> str:
        self.cut()
        return ("<h2>"+self.get_title()+"</h2>"+
                self.version_line()+
                self.mainheader_line()+
                self._ul_start+
                self.resolve_links(self.toc)+
                self._ul_end+
                "<h3>Documentation</h3>"+
                "<dl>"+
                self.resolve_links(self.text)+
                "</dl>")
    def version_line(self) -> str:
        if self.o.version:
            assert isinstance(self.o.version, str)
            return "<p>Version "+self.o.version+"</p>"
        return ""
    def mainheader_line(self) -> str:
        if self.o.onlymainheader:
            assert isinstance(self.o.onlymainheader, str)
            include = "#include &lt;"+self.o.onlymainheader+"&gt;"
            return "<p><big><b><code>"+include+"</code></b></big></p>"
        return ""
    def resolve_links(self, text: str) -> str:
        text &= (Match("(?s)<link>([^<>]*)(\\(\\d\\))</link>")
                 >> (lambda x: self.resolve_external(x.group(1), x.group(2))))
        text &= (Match("(?s)<link>(\\w+)</link>")
                 >> (lambda x: self.resolve_internal(x.group(1))))
        if self.not_found_in_anchors:
            logg.error("not found in anchors: %s", self.not_found_in_anchors)
        return (text & Match("(?s)<link>([^<>]*)</link>")
                >> "<code>\\1</code>")
    def resolve_external(self, func: str, sect: str) -> str:
        x = Match()
        if func & x("^zlib(.*)"):
            return ('<a href="'+self.http_zlib+x[1]+'">'+
                    "<code>"+func+sect+"</code>"+'</a>')
        if sect & x("[23]"):
            return ('<a href="'+self.http_opengroup+func+'.html">'+
                     "<code>"+func+sect+"</code>"+'</a>')
        return "<code>"+func+"<em>"+sect+"</em></sect>"
    def resolve_internal(self, func: str) -> str:
        if func in self.anchors:
            return '<code><a href="#'+func+'">'+func+"</a></code>"
        if func not in self.not_found_in_anchors:
            self.not_found_in_anchors += [ func ]
        return "<code><u>"+func+"</u></code>"
    def sane(self, text: Optional[str]) -> str:
        if not text:
            return ""
        return (text
                .replace("<function>", "<code>")
                .replace("</function>", "</code>"))
