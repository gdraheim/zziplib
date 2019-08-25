from __future__ import absolute_import, print_function

import cgi
import re
from collections import OrderedDict
from optparse import OptionParser

try:
    # noinspection PyCompatibility
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from zzipdoc.commentmarkup import CommentMarkup
from zzipdoc.dbk2htm import section2html, paramdef2html
from zzipdoc.docbookdocument import DocbookDocument
from zzipdoc.functionheader import FunctionHeaderList, FunctionHeader
from zzipdoc.functionlisthtmlpage import FunctionListHtmlPage
from zzipdoc.functionlistreference import FunctionListReference
from zzipdoc.functionprototype import FunctionPrototype
from zzipdoc.htmldocument import HtmlDocument
from zzipdoc.textfile import TextFile
from zzipdoc.textfileheader import TextFileHeader

MYPY = False
if MYPY:
    from typing import List, Callable, TypeVar, Any, Optional
    T = TypeVar('T')


class PerFileEntry(object):
    def __init__(self, textfileheader, filecomment):
        self.textfileheader = textfileheader  # type: TextFileHeader
        self.filecomment = filecomment  # type: CommentMarkup


class PerFile(object):
    def __init__(self):
        self.entries = []  # type: List[PerFileEntry]

    def add(self, textfileheader, filecomment):
        # type: (TextFileHeader, CommentMarkup) -> None
        self.entries += [PerFileEntry(textfileheader, filecomment)]

    def where_filename(self, filename):
        # type: (str) -> Optional[PerFileEntry]
        for entry in self.entries:
            if entry.textfileheader.filename == filename:
                return entry
        return None


class PerFunctionEntry(object):
    def __init__(self, header, comment, prototype):
        self.header = header  # type: FunctionHeader
        self.body = comment  # type: CommentMarkup
        self.head = prototype  # type: FunctionPrototype

    @property
    def name(self):
        return self.head.name

    @property
    def titleline(self):
        return self.header.titleline


class PerFunctionFamilyEntry(object):
    def __init__(self, leader):
        self.functions = [leader]
        self.name = leader.name

    def __contains__(self, func):
        return func in self.functions

    def add(self, func):
        if func not in self:
            self.functions.append(func)


class PerFunctionFamily(object):
    def __init__(self):
        self.functions = OrderedDict()
        self.retarget = {}
        self.entries = []  # type: List[PerFunctionFamilyEntry]

    def add_function(self, item):
        self.functions[item.name] = item

    def get_entry(self, name):
        for item in self.entries:
            if item.name == name:
                return item
        return None

    def fill_families(self):
        name_list = {}
        for func in self.functions.values():
            name = func.name
            name_list[name] = func

        for func in self.functions.values():
            name = func.name
            line = func.titleline
            is_retarget = re.search(r"=>\s*(\w+)", line)
            if is_retarget:
                into = is_retarget.group(1)
                self.retarget[name] = into

        lead_list = []

        for name, into in self.retarget.items():
            if into not in name_list:
                print("function '" + name + "' retarget into '" + into +
                      "' does not exist - keep alone")
            if into in self.retarget:
                other = self.retarget[into]
                print("function '" + name + "' retarget into '" + into +
                      "' which is itself a retarget into '" + other + "'")
            if into not in lead_list:
                lead_list.append(into)

        for name in self.functions:
            if name not in lead_list and name not in self.retarget:
                lead_list.append(name)

        for name in lead_list:
            func = self.functions.get(name)
            if func is None:
                print("head function '" + name + "' has no entry")
                continue

            entry = PerFunctionFamilyEntry(func)
            entry.add(func)  # the first
            self.entries.append(entry)

        for name, func in self.functions.items():
            if name in self.retarget:
                into = self.retarget[name]
                entry = self.get_entry(into)
                if entry is None:
                    print("into function '" + name + "' has no entry")
                    continue

                entry.add(func)  # will not add duplicates


class BaseManualPageAdapter(object):
    def __init__(self, entry):  # type: (PerFunctionEntry) -> None
        self.entry = entry

    @property
    def name(self):
        return self.entry.name

    @property
    def head(self):
        return self.entry.head

    @property
    def body(self):
        return self.entry.body

    @property
    def src_mainheader(self):
        return self.body.header.parent.textfile.mainheader

    @property
    def title(self):
        return self.body.header.title

    @property
    def filename(self):
        return self.body.header.filename

    @property
    def mainheader(self):
        return cgi.escape(self.src_mainheader)


class HtmlManualPageAdapter(BaseManualPageAdapter):
    pass


class RefEntryManualPageAdapter(BaseManualPageAdapter):
    def __init__(self, entry, per_file):
        # type: (PerFunctionEntry, PerFile) -> None
        super(RefEntryManualPageAdapter, self).__init__(entry)
        self.per_file = per_file  # type: PerFile

    @property
    def includes(self):
        return ""

    @property
    def list_seealso(self):
        return self.body.header.alsolist

    @property
    def comment(self):
        if not self.per_file:
            return ""

        entry = self.per_file.where_filename(self.filename)
        if not entry:
            return ""

        return entry.filecomment.xml_text()

    def parse_email_para(self, name):
        name = '[' + name[0].upper() + name[0].lower() + ']' + name[1:]
        check = re.search(
            r"(?s)<para>\s*" + name + r"\b((?:.(?!</para>))*.)</para>",
            self.comment)
        if check:
            return re.sub("<([^<>]*@[^<>]*)>", r"&lt;\1&gt;", check.group(0))
        return None

    @property
    def authors(self):
        return self.parse_email_para('authors')

    @property
    def copyright(self):
        return self.parse_email_para('copyright')


def makedocs(filenames, o):  # type: (List[str], Any) -> None
    textfiles = [TextFile(filename) for filename in filenames]

    per_file = PerFile()
    for textfile in textfiles:
        textfileheader = TextFileHeader(textfile)
        per_file.add(textfileheader, CommentMarkup(textfileheader))

    funcheaders = [FunctionHeaderList(e.textfileheader)
                   for e in per_file.entries]
    per_family = PerFunctionFamily()
    for funcheader in funcheaders:
        for child in funcheader.children:
            entry = PerFunctionEntry(child, CommentMarkup(child),
                                     FunctionPrototype(child))
            per_family.add_function(entry)
    per_family.fill_families()

    out_filename = o.output + o.suffix

    html = make_page_from_functions(
        o.onlymainheader, per_family,
        page=FunctionListHtmlPage(o.package, o.version, o.onlymainheader),
        make_adapter=HtmlManualPageAdapter)

    doc = HtmlDocument(o.version) \
        .set_title(html.title) \
        .add(section2html(paramdef2html(html.make_xml_text())))
    _save_doc(doc, out_filename + "." + o.html)

    man3 = make_page_from_functions(
        o.onlymainheader, per_family,
        page=FunctionListReference(o.version, o.package),
        make_adapter=lambda f: RefEntryManualPageAdapter(f, per_file))
    doc = DocbookDocument() \
        .set_title(man3.title) \
        .add(man3)
    _save_doc(doc, out_filename + "." + o.docbook)


def _save_doc(doc, filename):
    try:
        print("Preparing {filename}".format(filename=filename))
        output = StringIO()
        doc.save(output)
        print("Writing {filename}".format(filename=filename))
        with open(filename, "w") as f:
            f.write(output.getvalue())
    except IOError:
        print("Error saving document to {filename}".format(filename=filename))


def make_page_from_functions(onlymainheader, per_family, page, make_adapter):
    # type: (str, PerFunctionFamily, T, Callable[[PerFunctionEntry], BaseManualPageAdapter]) -> T
    for item in per_family.entries:
        for func in item.functions:
            func_adapter = make_adapter(func)
            if onlymainheader:
                if not re.search("<" + onlymainheader + ">",
                                 func_adapter.src_mainheader):
                    continue
            page.add(func_adapter)
        page.cut()
    page.cut()
    return page


def main():
    parser = OptionParser()
    parser.add_option("--package", default="ZZipLib", metavar="NAME",
                      help="Name of software being documented")
    parser.add_option("--html", default="html", metavar="SUFFIX",
                      help="Extension for generated HTML files")
    parser.add_option("--docbook", default="docbook", metavar="SUFFIX",
                      help="Extension for generated docbook files")
    parser.add_option("--output", default="zziplib", metavar="FILENAME",
                      help="Help filename base")
    parser.add_option("--suffix", default="", help="Help filename suffix")
    parser.add_option("--version", default="", metavar="VERSION",
                      help="Current version of software being documented")
    parser.add_option("--onlymainheader", default="", metavar="FILENAME",
                      help="Specific header to focus on")
    opts, args = parser.parse_args()

    makedocs(args, opts)


if __name__ == "__main__":
    main()
