#! /usr/bin/python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements,line-too-long
# pylint: disable=wrong-import-position
from typing import Optional, List, Dict

import sys
import os.path
import logging

sys.path = [ os.path.dirname(__file__) ] + sys.path
# from zzipdoc.match import *
# from zzipdoc.textfile import *
# from zzipdoc.textfileheader import *
# from zzipdoc.functionheader import *
# from zzipdoc.functionprototype import *
# from zzipdoc.commentmarkup import *
# from zzipdoc.functionlisthtmlpage import *
# from zzipdoc.functionlistreference import *
# from zzipdoc.dbk2htm import *
# from zzipdoc.htmldoctypes import *
# from zzipdoc.htmldocument import *
# from zzipdoc.docbookdocument import *

from zzipdoc.match import Match
from zzipdoc.htmldoctypes import DocOptions
from zzipdoc.textfileheader import TextFile
from zzipdoc.functionheader import FunctionHeaderList
from zzipdoc.functionprototype import FunctionPrototype
from zzipdoc.commentmarkup import TextFileHeader, CommentMarkupTextFileHeader, FunctionHeader, CommentMarkupFunctionHeader, CommentMarkup
from zzipdoc.functionlisthtmlpage import FunctionListHtmlPage
from zzipdoc.dbk2htm import section2html, paramdef2html
from zzipdoc.htmldoctypes import RefDocPart
from zzipdoc.htmldocument import HtmlDocPart, HtmlDocument
from zzipdoc.docbookdocument import FunctionListReference, DocbookDocument

NIX = ""

def _src_to_xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def _email_to_xml(text: str) -> str:
    return text & Match("<([^<>]*@[^<>]*)>") >> "&lt;\\1&gt;"

class PerFileEntry:
    textfileheader: TextFileHeader
    comment: CommentMarkupTextFileHeader
    def __init__(self, header: TextFileHeader, comment: CommentMarkupTextFileHeader) -> None:
        self.textfileheader = header
        self.filecomment = comment
class PerFile:
    textfileheaders: List[TextFileHeader]
    filecomments: List[CommentMarkupTextFileHeader]
    entries: List[PerFileEntry]
    def __init__(self) -> None:
        self.textfileheaders = []
        self.filecomments = []
        self.entries = []
    def add(self, textfileheader: TextFileHeader, filecomment: CommentMarkupTextFileHeader) -> None:
        self.textfileheaders += [ textfileheader ]
        self.filecomments += [ filecomment ]
        self.entries += [ PerFileEntry(textfileheader, filecomment) ]
    def where_filename(self, filename: str) -> Optional[PerFileEntry]:
        for entry in self.entries:
            if entry.textfileheader.get_filename() == filename:
                return entry
        return None
    def print_list_mainheader(self) -> None:
        for t_fileheader in self.textfileheaders:
            print(t_fileheader.get_filename(), t_fileheader.src_mainheader())

class PerFunctionEntry:
    header: FunctionHeader
    comment: CommentMarkupFunctionHeader
    prototype: FunctionPrototype
    def __init__(self, header: FunctionHeader, comment: CommentMarkupFunctionHeader, prototype: FunctionPrototype) -> None:
        self.header = header
        self.comment = comment
        self.prototype = prototype
    def get_name(self) -> Optional[str]:
        return self.prototype.get_name()
    def get_titleline(self) -> str:
        return self.header.get_titleline()
    def get_head(self) -> FunctionPrototype:
        return self.prototype
    def get_body(self) -> CommentMarkupFunctionHeader:
        return self.comment
class PerFunction:
    headers: List[FunctionHeader]
    comments: List[CommentMarkup]
    prototypes: List[FunctionPrototype]
    entries: List[PerFunctionEntry]
    def __init__(self) -> None:
        self.headers = []
        self.comments = []
        self.prototypes = []
        self.entries = []
    def add(self, functionheader: FunctionHeader, functioncomment: CommentMarkupFunctionHeader, functionprototype: FunctionPrototype) -> None:
        self.headers += [ functionheader ]
        self.comments += [ functioncomment ]
        self.prototypes += [ functionprototype ]
        self.entries += [ PerFunctionEntry(functionheader, functioncomment,
                                           functionprototype) ]
    def print_list_titleline(self) -> None:
        for funcheader in self.headers:
            print(funcheader.get_filename(), "[=>]", funcheader.get_titleline())
    def print_list_name(self) -> None:
        for funcheader in self.prototypes:
            print(funcheader.get_filename(), "[>>]", funcheader.get_name())

class PerFunctionFamilyEntry:
    leader: PerFunctionEntry
    functions: List[PerFunctionEntry]
    def __init__(self, leader: PerFunctionEntry) -> None:
        self.leader = leader
        self.functions = []
    def contains(self, func: PerFunctionEntry) -> bool:
        for item in self.functions:
            if item == func: return True
        return False
    def add(self, func: PerFunctionEntry) -> None:
        if not self.contains(func):
            self.functions += [ func ]
    def get_name(self) -> Optional[str]:
        if self.leader is None: return None
        return self.leader.get_name()
class PerFunctionFamily:
    functions: List[PerFunctionEntry]
    families: List[PerFunctionFamilyEntry]
    retarget: Dict[str, str]
    entries: List[PerFunctionFamilyEntry]
    def __init__(self) -> None:
        self.functions = []
        self.families = []
        self.retarget = {}
        self.entries = []
    def add_PerFunction(self, per_list: PerFunction) -> None:
        for item in per_list.entries:
            self.add_PerFunctionEntry(item)
    def add_PerFunctionEntry(self, item: PerFunctionEntry) -> None:
        self.functions += [ item ]
    def get_function(self, name: str) -> Optional[PerFunctionEntry]:
        for item in self.functions:
            if item.get_name() == name:
                return item
        return None
    def get_entry(self, name: str) -> Optional[PerFunctionFamilyEntry]:
        for item in self.entries:
            if item.get_name() == name:
                return item
        return None
    def fill_families(self) -> None:
        name_list = {}
        for func in self.functions:
            name = func.get_name()
            name_list[name] = func
        for func in self.functions:
            name = func.get_name()
            line = func.get_titleline()
            if not name or not line:
                continue
            is_retarget = Match("=>\\s*(\\w+)")
            if line & is_retarget:
                retarget = is_retarget[1]
                self.retarget[name] = retarget
        lead_list = []
        for name in self.retarget:
            into = self.retarget[name]
            if into not in name_list:
                print("function '"+name+"' retarget into '"+into+
                      "' does not exist - keep alone")
            if into in self.retarget:
                other = self.retarget[into]
                print("function '"+name+"' retarget into '"+into+
                      "' which is itself a retarget into '"+other+"'")
            if into not in lead_list:
                lead_list += [ into ]
        for func in self.functions:
            name = func.get_name()
            if not name:
                continue
            if name not in lead_list and name not in self.retarget:
                lead_list += [ name ]
        for name in lead_list:
            func1 = self.get_function(name)
            if func1 is not None:
                entry1 = PerFunctionFamilyEntry(func1)
                entry1.add(func1) # the first
                self.entries += [ entry1 ]
            else:
                print("head function '"+name+" has no entry")
        for func in self.functions:
            name = func.get_name()
            if name in self.retarget:
                into2 = self.retarget[name]
                entry2 = self.get_entry(into2)
                if entry2 is not None:
                    entry2.add(func) # will not add duplicates
                else:
                    print("into function '"+name+" has no entry")
    def print_list_name(self) -> None:
        for family in self.entries:
            name = family.get_name()
            print(name, ":", end = " ")
            for item in family.functions:
                print(item.get_name(), ",", end = " ")
            print("")
class HtmlManualPageAdapter(RefDocPart):
    entry: PerFunctionEntry
    def __init__(self, entry: PerFunctionEntry) -> None:
        """ usually takes a PerFunctionEntry """
        self.entry = entry
    def get_name(self) -> Optional[str]:
        return self.entry.get_name()
    def _head(self) -> FunctionPrototype:
        return self.entry.get_head()
    def _body(self) -> CommentMarkupFunctionHeader:
        return self.entry.get_body()
    def head_xml_text(self) -> Optional[str]:
        return self._head().xml_text()
    def body_xml_text(self, name: Optional[str]) -> Optional[str]:
        return self._body().xml_text(name)
    def head_get_prespec(self) -> Optional[str]:
        return self._head().get_prespec()
    def head_get_namespec(self) -> Optional[str]:
        return self._head().get_namespec()
    def head_get_callspec(self) -> Optional[str]:
        return self._head().get_callspec()
    def get_title(self) -> Optional[str]:
        return self._body().header.get_title()
    def get_filename(self) -> Optional[str]:
        return self._body().header.get_filename()
    def src_mainheader(self) -> Optional[str]:
        return self._body().header.src_mainheader()
    def get_mainheader(self) -> Optional[str]:
        return _src_to_xml(self.src_mainheader() or "")
class RefEntryManualPageAdapter(RefDocPart):
    entry: PerFunctionEntry
    per_file: Optional[PerFile]
    def __init__(self, entry: PerFunctionEntry, per_file: Optional[PerFile] = None) -> None:
        """ usually takes a PerFunctionEntry """
        self.entry = entry
        self.per_file = per_file
    def get_name(self) -> Optional[str]:
        return self.entry.get_name()
    def _head(self) -> FunctionPrototype:
        return self.entry.get_head()
    def _body(self) -> CommentMarkupFunctionHeader:
        return self.entry.get_body()
    def head_xml_text(self) -> Optional[str]:
        return self._head().xml_text()
    def body_xml_text(self, name: Optional[str]) -> Optional[str]:
        return self._body().xml_text(name)
    def get_title(self) -> Optional[str]:
        return self._body().header.get_title()
    def get_filename(self) -> Optional[str]:
        return self._body().header.get_filename()
    def src_mainheader(self) -> Optional[str]:
        return self._body().header.src_mainheader()
    def get_mainheader(self) -> str:
        return _src_to_xml(self.src_mainheader() or "")
    def get_includes(self) -> str:
        return ""
    def list_seealso(self) -> List[str]:
        return self._body().header.get_alsolist()
    def get_authors(self) -> Optional[str]:
        comment = None
        filename = self.get_filename()
        if self.per_file and filename:
            entry = self.per_file.where_filename(filename)
            if entry:
                comment = entry.filecomment.xml_text()
        if comment:
            check = Match(r"(?s)<para>\s*[Aa]uthors*\b:*"
                          r"((?:.(?!</para>))*.)</para>")
            if comment & check: return _email_to_xml(check[1])
        return None
    def get_copyright(self) -> Optional[str]:
        comment = None
        filename = self.get_filename()
        if self.per_file and filename:
            entry = self.per_file.where_filename(filename)
            if entry:
                comment = entry.filecomment.xml_text()
        if comment:
            check = Match(r"(?s)<para>\s*[Cc]opyright\b"
                          r"((?:.(?!</para>))*.)</para>")
            if comment & check: return _email_to_xml(check[0])
        return None

def makedocs(filenames: List[str], o: DocOptions) -> None:
    textfiles = []
    for filename in filenames:
        textfile = TextFile(filename)
        textfile.parse()
        textfiles += [ textfile ]
    per_file = PerFile()
    for textfile in textfiles:
        textfileheader = TextFileHeader(textfile)
        textfileheader.parse()
        filecomment = CommentMarkupTextFileHeader(textfileheader)
        filecomment.parse()
        per_file.add(textfileheader, filecomment)
    funcheaders = []
    for textfileheader in per_file.textfileheaders:
        funcheader = FunctionHeaderList(textfileheader)
        funcheader.parse()
        funcheaders += [ funcheader ]
    per_function = PerFunction()
    for funcheader in funcheaders:
        for child in funcheader.get_children():
            funcprototype = FunctionPrototype(child)
            funcprototype.parse()
            funccomment = CommentMarkupFunctionHeader(child)
            funccomment.parse()
            per_function.add(child, funccomment, funcprototype)
    per_family = PerFunctionFamily()
    for item in per_function.entries:
        per_family.add_PerFunctionEntry(item)
    per_family.fill_families()
    # debug output....
    # per_file.print_list_mainheader()
    # per_function.print_list_titleline()
    # per_function.print_list_name()
    # per_family.print_list_name()
    #
    html = FunctionListHtmlPage(o)
    for entry in per_family.entries:
        for func in entry.functions:
            html_adapter = HtmlManualPageAdapter(func)
            src_mainheader = html_adapter.src_mainheader() or ""
            if o.onlymainheader:
                include = "<"+o.onlymainheader+">"
                if include not in src_mainheader:
                    continue
            html.add(html_adapter)
        html.cut()
    html.cut()
    class HtmlPage(HtmlDocPart):
        def __init__(self, html: FunctionListHtmlPage) -> None:
            self.html = html
        def html_text(self) -> str:
            return section2html(paramdef2html(self.html.xml_text()))
        def get_title(self) -> str:
            return self.html.get_title()
    HtmlDocument(o).add(HtmlPage(html)).save(o.output+o.suffix)
    #
    man3 = FunctionListReference(o)
    for entry in per_family.entries:
        for func in entry.functions:
            func_adapter = RefEntryManualPageAdapter(func, per_file)
            src_mainheader = func_adapter.src_mainheader() or ""
            if o.onlymainheader:
                include = "<"+o.onlymainheader+">"
                if include not in src_mainheader:
                    continue
            man3.add(func_adapter)
        man3.cut()
    man3.cut()
    DocbookDocument(o).add(man3).save(o.output+o.suffix)


def main() -> int:
    import optparse # pylint: disable=deprecated-module,import-outside-toplevel
    cmdline = optparse.OptionParser("%prog [file.c].. --package=x --version=y --onlymainheader=zzip/lib.h")
    cmdline.add_option("-v", "--verbose", action="count", default=0, help="more logging")
    cmdline.add_option("-^", "--quiet", action="count", default=0, help="less logging")
    cmdline.add_option("--program", metavar="NAM", default=sys.argv[0], help="[%default]")
    cmdline.add_option("--package", metavar="NAM", default="ZzipLib", help="[%default]")
    cmdline.add_option("--version", metavar="X.Y", default=NIX)
    cmdline.add_option("--html", metavar="EXT", default="html", help="extension [%default]")
    cmdline.add_option("--docbook", metavar="EXT", default="docbook", help="extension [%default]")
    cmdline.add_option("--output", metavar="BASE", default="zziplib", help="basename for output files")
    cmdline.add_option("--suffix", metavar="NAM", default=NIX, help="suffix for basename output")
    cmdline.add_option("--onlymainheader", metavar="x/lib.h", default=NIX, help="put this include first")
    cmdline.add_option("--body", metavar="FILE", default=NIX, help="append this body text")
    opt, args = cmdline.parse_args()
    logging.basicConfig(level = max(0, logging.WARNING - 10 * opt.verbose + 10 * opt.quiet))
    #
    o = DocOptions()
    o.program = opt.program or sys.argv[0]
    o.package = opt.package or "ZZipLib"
    o.version = opt.version
    o.html = opt.html or "html"
    o.docbook = opt.docbook or "docbook"
    o.output = opt.output or "zziplib"
    o.suffix = opt.suffix
    o.onlymainheader = opt.onlymainheader
    o.body = opt.body
    makedocs(args, o)
    return 0

if __name__ == "__main__":
    sys.exit(main())
