#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function

from zzipdoc.document import BaseDocument


class HtmlDocument(BaseDocument):
    """ binds some html content page with additional markup - in this
    base version it is just the header information while other variants
    might add navigation items around the content block elements """

    def __init__(self, version):
        super(HtmlDocument, self).__init__()
        self.version = version

    def html_header(self):
        text = "<html><head>"
        title = self.title
        if title:
            text += "<title>" + title + "</title>"
        text += "\n"
        return text + "</head><body>"

    def html_footer(self):
        return "</body></html>"

    def save(self, fd):
        print(self.html_header(), file=fd)
        for text in self.text:
            print(text, file=fd)
        print(self.html_footer(), file=fd)

