from __future__ import print_function

import re


def _sane(text):
    return (text
            .replace("<function>", "<code>")
            .replace("</function>", "</code>"))


class FunctionListHtmlPage(object):
    """ The main part here is to create a TOC (table of contents) at the
    start of the page - linking down to the descriptions of the functions.
    Sure we need to generate anchors on the fly. Additionally, all the
    non-html (docbook-like) markup needs to be converted for ouput. -
    each element to be added should have the properties name, head and
    body with the latter two having a xml_text() method."""
    _null_table100 = '<table border="0" width="100%"' \
                     ' cellpadding="0" cellspacing="0">'
    _ul_start = '<table width="100%">'
    _ul_end = '</table>'
    _li_start = '<tr><td valign="top">'
    _li_end = '</td></tr>'
    http_opengroup = "http://www.opengroup.org/onlinepubs/000095399/functions/"
    http_zlib = "http://www.zlib.net/manual.html"

    def __init__(self, package, version, onlymainheader):
        self.package = package
        self.version = version
        self.onlymainheader = onlymainheader
        self.toc = ""
        self.text = ""
        self.head = ""
        self.body = ""
        self.anchors = []
        self.not_found_in_anchors = []

    def cut(self):
        self.text += (
            "<dt>" + self._ul_start + self.head + self._ul_end + "</dt>" +
            "<dd>" + self._ul_start + self.body + self._ul_end + "</dd>")
        self.head = ""
        self.body = ""

    def add(self, entry):
        name = entry.name
        head_text = str(entry.head)
        body_text = entry.body.xml_text(name)
        if not head_text:
            print("no head_text for", name)
            return

        prespec = entry.head.prespec
        namespec = entry.head.namespec
        callspec = entry.head.callspec
        head_text = ("<code><b><function>" + namespec + "</function></b>"
                     + callspec + " : " + prespec + "</code>")

        extraline = ""
        title = entry.title
        filename = entry.filename.replace("../", "")
        if title:
            subtitle = '&nbsp;<em>' + title + '</em>'
            extraline = (
                        self._null_table100 + '<td> ' + subtitle + ' </td>' +
                        '<td align="right"> ' +
                        '<em><small>' + filename + '</small></em>' +
                        '</td></table>')
        body_text = extraline + body_text

        function_tag = re.compile(r"<function>(\w*)</function>")

        def link(text):
            return function_tag.sub(r"<link>\1</link>", text)

        def here(text):
            has_function = function_tag.search(text)
            if has_function:
                self.anchors.append(has_function.group(1))
                return function_tag.sub(r'<a name="\1">\1</a>', text)
            else:
                return text

        self.toc += self._li_start + _sane(link(head_text)) + self._li_end
        self.head += self._li_start + _sane(here(head_text)) + self._li_end
        self.body += self._li_start + _sane(body_text) + self._li_end

    @property
    def title(self):
        return self.package + " Library Functions"

    def make_xml_text(self):
        self.cut()
        return ("<h2>" + self.title + "</h2>" +
                self.version_line +
                self.mainheader_line +
                self._ul_start +
                self.resolve_links(self.toc) +
                self._ul_end +
                "<h3>Documentation</h3>" +
                "<dl>" +
                self.resolve_links(self.text) +
                "</dl>")

    @property
    def version_line(self):
        if self.version:
            return "<p>Version " + self.version + "</p>"
        return ""

    @property
    def mainheader_line(self):
        if self.onlymainheader:
            include = "#include &lt;" + self.onlymainheader + "&gt;"
            return "<p><big><b><code>" + include + "</code></b></big></p>"
        return ""

    def resolve_links(self, text):
        text = re.sub(r"(?s)<link>([^<>]*)(\(\d\))</link>",
                      (lambda x: self.resolve_external(x.group(1), x.group(2))),
                      text)
        text = re.sub(r"(?s)<link>(\w+)</link>",
                      (lambda x: self.resolve_internal(x.group(1))), text)
        text = re.sub(r"(?s)<link>([^<>]*)</link>", r"<code>\1</code>", text)

        # Note: not_found_in_anchors mutated by resolve_internal, do not reorder
        if len(self.not_found_in_anchors):
            print("not found in anchors:", self.not_found_in_anchors)

        return text

    def resolve_external(self, func, sect):
        zlib_found = re.search("^zlib(.*)", func)
        if zlib_found:
            return ('<a href="' + self.http_zlib + zlib_found.group(1) + '">' +
                    "<code>" + func + sect + "</code>" + '</a>')

        manpage_found = re.search("[23]", sect)
        if manpage_found:
            return ('<a href="' + self.http_opengroup + func + '.html">' +
                    "<code>" + func + sect + "</code>" + '</a>')
        return "<code>" + func + "<em>" + sect + "</em></sect>"

    def resolve_internal(self, func):
        if func in self.anchors:
            return '<code><a href="#{func}">{func}</a></code>'.format(func=func)
        if func not in self.not_found_in_anchors:
            self.not_found_in_anchors.append(func)
        return "<code><u>{func}</u></code>".format(func=func)
