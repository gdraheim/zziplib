#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=broad-exception-caught,unspecified-encoding,consider-using-with,no-else-return

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Optional, List
import logging

from zzipdoc.match import Match
from zzipdoc.htmldoctypes import DocOptions
from zzipdoc.functionlistreference import FunctionListReference

logg = logging.getLogger(__name__)

class DocbookDocument:
    """ binds some xml content page with additional markup - in this
    variant we set the rootnode container to 'reference' and the DTD
    to the Docbook 4.1.2 version. Modify as you like."""
    has_title_child = [ "book", "chapter", "section", "reference" ]
    docbook_dtd = (
        ' PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN"'+"\n"+
        '       "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd"')
    o: DocOptions
    rootnode: str
    filename: Optional[str]
    title: str
    text: List[FunctionListReference]
    def __init__(self, o: DocOptions, filename: Optional[str] = None):
        self.o = o
        self.rootnode = "reference"
        self.filename = filename
        self.title = ""
        self.text = []
    def add(self, text: FunctionListReference) -> "DocbookDocument":
        """ add some content """
        self.text += [ text ]
        return self
    def get_title(self) -> Optional[str]:
        if self.title: return self.title
        try:
            return self.text[0].get_title()
        except Exception as e:
            logg.info("could not get title: %s", e)
        return self.title
    def _xml_doctype(self, rootnode: str) -> str:
        return "<!DOCTYPE "+rootnode+self.docbook_dtd+">"
    def _xml_text(self, xml: FunctionListReference) -> str:
        """ accepts adapter objects with .xml_text() """
        try:
            return xml.xml_text()
        except Exception as e:
            logg.error("DocbookDocument/text %s", e)
        return str(xml)
    def _fetch_rootnode(self, text: str) -> str:
        fetch = Match(r"^[^<>]*<(\w+)\b")
        if text & fetch: return fetch[1]
        return self.rootnode
    def _filename(self, filename: Optional[str]) -> str:
        if filename is not None:
            self.filename = filename
        filename = self.filename
        assert filename is not None
        if not filename & Match(r"\.\w+$"):
            ext = self.o.docbook
            if not ext: ext = "docbook"
            filename += "."+ext
        return filename or ""
    def save(self, filename: Optional[str] = None) -> bool:
        filename = self._filename(filename)
        print("writing '"+filename+"'")
        if len(self.text) > 1:
            return self.save_all(filename)
        else:
            return self.save_text(filename, self.text[0])
    def save_text(self, filename: str, text: FunctionListReference) -> bool:
        try:
            fd = open(filename, "w")
            xml_text = self._xml_text(text)
            rootnode = self._fetch_rootnode(xml_text)
            doctype = self._xml_doctype(rootnode)
            print(doctype, file=fd)
            print(xml_text, file=fd)
            fd.close()
            return True
        except IOError as e:
            print("could not open '"+filename+"'file" + str(e))
            return False
    def save_all(self, filename: str) -> bool:
        assert len(self.text) > 1
        try:
            fd = open(filename, "w")
            xml_text = self._xml_text(self.text[0])
            rootnode = self._fetch_rootnode(xml_text)
            if rootnode == self.rootnode:
                rootnode = "book"
            else:
                rootnode = self.rootnode
            doctype = self._xml_doctype(rootnode)
            print(doctype, file=fd)
            title = self.get_title()
            if title and self.rootnode in self.has_title_child:
                print("<"+self.rootnode+'><title>'+title+'</title>', file=fd)
            elif title:
                print("<"+self.rootnode+' id="'+title+'">', file=fd)
            else:
                print("<"+self.rootnode+'>', file=fd)
            for text in self.text:
                part = self._xml_text(text)
                print(part, file=fd)
            print("</"+self.rootnode+">", file=fd)
            fd.close()
            return True
        except IOError as e:
            print("could not open '"+filename+"'file" + str(e))
            return False
