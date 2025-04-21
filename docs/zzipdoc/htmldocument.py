#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=broad-exception-caught,unnecessary-pass,unspecified-encoding,no-else-return

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Optional, List
import logging

from zzipdoc.match import Match
from zzipdoc.htmldoctypes import DocOptions
from zzipdoc.htmldoctypes import HtmlDocPart, HtmlStylePart, HtmlMetaPart

logg = logging.getLogger(__name__)

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
        except Exception as e:
            logg.info("can not get title: %s", e)
        return self.title
    def _html_meta(self, meta: HtmlMetaPart) -> str:
        """ accepts adapter objects with .html_meta() """
        try:   return meta.html_meta()
        except Exception as e:
            logg.info("can not get meta: %s", e)
        return str(meta)
    def _html_style(self, style: HtmlStylePart) -> str:
        """ accepts adapter objects with .html_style() and .xml_style() """
        ee: Optional[Exception] = None
        try:
            return style.html_style()
        except Exception as e:
            ee = e
        try:
            return style.xml_style()
        except Exception as e:
            logg.error("HtmlDocument/style %s %s", ee, e)
        try:
            return str(style)
        except Exception as e:
            logg.error("HtmlDocument/style %s", e)
        return ""
    def _html_text(self, html: HtmlDocPart) -> Optional[str]:
        """ accepts adapter objects with .html_text() and .xml_text() """
        ee = None
        try:
            return html.html_text()
        except Exception as e:
            ee = e
        try:
            return html.xml_text()
        except Exception as e:
            logg.error("HtmlDocument/text %s %s", ee, e)
        try:
            return str(html)
        except Exception as e:
            logg.error("HtmlDocument/text %s", e)
            return "&nbsp;"
        return None
    def navigation(self) -> Optional[str]:
        if self.navi:
            return self.navi
        if self.o.body:
            try:
                with open(self.o.body, "r") as fd:
                    self.navi = fd.read()
                return self.navi
            except Exception as e:
                logg.info("can not read body: %s", e)
        return None
    def html_header(self) -> str:
        navi = self.navigation()
        if not navi:
            text = "<html><head>"
            title = self.get_title()
            if title:
                text += "<title>"+title+"</title>"
            text += "\n"
            for style in self.stylelist:
                text += self._html_style(style)
                text += "\n"
            return text+"</head><body>"
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
        logg.info("writing '%s'", filename)
        try:
            with  open(filename, "w") as fd:
                print(self.html_header(), file=fd)
                for text in self.text:
                    print(self._html_text(text), file=fd)
                print(self.html_footer(), file=fd)
            return True
        except IOError as e:
            logg.error("could not open '%s': %s", filename, e)
            return False
