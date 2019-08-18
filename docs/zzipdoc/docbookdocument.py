#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import re

from zzipdoc.document import BaseDocument


class DocbookDocument(BaseDocument):
    """ binds some xml content page with additional markup - in this
    variant we set the rootnode container to 'reference' and the DTD
    to the Docbook 4.1.2 version. Modify as you like."""
    has_title_child = ["book", "chapter", "section", "reference"]
    docbook_dtd = (
            ' PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN"' + "\n" +
            '       "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd"')

    def __init__(self):
        super(DocbookDocument, self).__init__()
        self.rootnode = "reference"

    def _xml_doctype(self, rootnode):
        return "<!DOCTYPE " + rootnode + self.docbook_dtd + ">"

    def _xml_text(self, xml):
        """ accepts adapter objects with .xml_text() """
        try:
            return xml.xml_text()
        except Exception as e:
            print("DocbookDocument/text", e)
        return str(xml)

    def _fetch_rootnode(self, text):
        fetch = re.search(r"^[^<>]*<(\w+)\b", text)
        if fetch:
            return fetch.group(1)
        return self.rootnode

    def save(self, fd):
        if len(self.text) > 1:
            self.save_all(fd)
        else:
            self.save_text(fd, self.text[0])

    def save_text(self, fd, text):
        xml_text = self._xml_text(text)
        rootnode = self._fetch_rootnode(xml_text)
        doctype = self._xml_doctype(rootnode)
        print(doctype, file=fd)
        print(xml_text, file=fd)

    def save_all(self, fd):
        assert len(self.text) > 1
        xml_text = self._xml_text(self.text[0])
        rootnode = self._fetch_rootnode(xml_text)
        if rootnode == self.rootnode:
            rootnode = "book"
        else:
            rootnode = self.rootnode
        doctype = self._xml_doctype(rootnode)
        print(doctype, file=fd)
        title = self.title
        if title and self.rootnode in self.has_title_child:
            print("<" + self.rootnode + '><title>' + title + '</title>',
                  file=fd)
        elif title:
            print("<" + self.rootnode + ' id="' + title + '">', file=fd)
        else:
            print("<" + self.rootnode + '>', file=fd)
        for text in self.text:
            text = self._xml_text(text)
            print(text, file=fd)
        print("</" + self.rootnode + ">", file=fd)
