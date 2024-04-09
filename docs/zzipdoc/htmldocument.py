#! /usr/bin/env python3

from __future__ import print_function

from typing import Optional, List
from zzipdoc.match import Match
from zzipdoc.options import DocOptions
from zzipdoc.htmldoctypes import HtmlDocPart, HtmlStylePart, HtmlMetaPart

class HtmlDocument:
    """ binds some html content page with additional markup - in this
    base version it is just the header information while other variants
    might add navigation items around the content block elements """
    o: DocOptions
    filename: Optional[str]
    title: str
    metalist: List[HtmlMetaPart]
    stylelist: List[HtmlStylePart]
    text: List[HtmlDocPart]
    navi: Optional[str]
    def __init__(self, o: DocOptions, filename: Optional[str] = None) -> None:
        self.o = o
        self.filename = filename
        self.title = ""
        self.metalist = []
        self.stylelist = []
        self.text = []
        self.navi = None
    def meta(self, meta: HtmlMetaPart) -> "HtmlDocument":
        """ add some header meta entry """
        self.metalist += [ meta ]
        return self
    def style(self, style: HtmlStylePart) -> "HtmlDocument":
        """ add a style block """
        self.stylelist += [ style ]
        return self
    def add(self, text: HtmlDocPart) -> "HtmlDocument":
        """ add some content """
        self.text += [ text ]
        return self
    def get_title(self) -> str:
        if self.title: return self.title
        try:   return self.text[0].get_title()
        except Exception as e: pass
        return self.title
    def _html_meta(self, meta: HtmlMetaPart) -> str:
        """ accepts adapter objects with .html_meta() """
        try:   return meta.html_meta()
        except Exception as e: pass
        return str(meta)
    def _html_style(self, style: HtmlStylePart) -> str:
        """ accepts adapter objects with .html_style() and .xml_style() """
        ee = None
        try:   return style.html_style()
        except Exception as e: ee = e; pass
        try:   return style.xml_style()
        except Exception as e: print("HtmlDocument/style {} {}".format(ee, e)); pass
        try:   return str(style)
        except Exception as e: print("HtmlDocument/style {}".format(e)); return ""
    def _html_text(self, html: HtmlDocPart) -> Optional[str]:
        """ accepts adapter objects with .html_text() and .xml_text() """
        ee = None
        try:   return html.html_text()
        except Exception as e: ee = e; pass
        try:   return html.xml_text()
        except Exception as e: print("HtmlDocument/text {} {}".format(ee, e)); pass
        try:   return str(html)
        except Exception as e: print("HtmlDocument/text {}".format(e)); return "&nbsp;"
        return None
    def navigation(self) -> Optional[str]:
        if self.navi:
            return self.navi
        if self.o.body:
            try:
                fd = open(self.o.body, "r")
                self.navi = fd.read()
                fd.close()
                return self.navi
            except Exception as e:
                pass
        return None
    def html_header(self) -> str:
        navi = self.navigation()
        if not navi:
            T = "<html><head>"
            title = self.get_title()
            if title:
                T += "<title>"+title+"</title>"
            T += "\n"
            for style in self.stylelist:
                T += self._html_style(style)
                T += "\n"
            return T+"</head><body>"
        else:
            title = self.get_title()
            version: str = self.o.version # type: ignore[assignment]
            return navi & (
                Match(r"<!--title-->") >> " - "+title) & (
                Match(r"<!--VERSION-->") >> version) & (
                Match(r"(?m).*</body></html>") >> "")
    def html_footer(self) -> str:
        navi = self.navigation()
        if not navi:
            return "</body></html>"
        else:
            return navi & (
                Match(r"(?m)(.*</body></html>)") >> "%&%&%&%\\1") & (
                Match(r"(?s).*%&%&%&%") >> "")
    def _filename(self, filename: Optional[str]) -> str:
        if filename is not None:
            self.filename = filename
        filename = self.filename
        assert filename is not None
        if not filename & Match(r"\.\w+$"):
            ext = self.o.html
            if not ext: ext = "html"
            filename += "."+ext
        return filename
    def save(self, filename: Optional[str] = None) -> bool:
        filename = self._filename(filename)
        print("writing '"+filename+"'")
        try:
            fd = open(filename, "w")
            print(self.html_header(), file=fd)
            for text in self.text:
                print(self._html_text(text), file=fd)
            print(self.html_footer(), file=fd)
            fd.close()
            return True
        except IOError as e:
            print("could not open '"+filename+"'file {}".format(e))
            return False
