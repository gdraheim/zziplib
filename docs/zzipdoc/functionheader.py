#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements,line-too-long

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Optional, List
from zzipdoc.match import Match
from zzipdoc.textfileheader import TextFileHeader

class FunctionHeader:
    """ parsing the comment block that is usually presented before
    a function prototype - the prototype part is passed along
    for further parsing through => FunctionPrototype """
    parent: "FunctionHeaderList"
    comment: str
    prototype: str
    firstline: Optional[str]
    otherlines: Optional[str]
    titleline: Optional[str]
    alsolist: List[str]
    def __init__(self, functionheaderlist: "FunctionHeaderList", comment: str, prototype: str) -> None:
        self.parent = functionheaderlist
        self.comment = comment
        self.prototype = prototype
        self.firstline = None
        self.otherlines = None
        self.titleline = None
        self.alsolist = []
    def get_filename(self) -> Optional[str]:
        if self.parent:
            return self.parent.get_filename()
        return None
    def src_mainheader(self) -> Optional[str]:
        if self.parent:
            return self.parent.src_mainheader()
        return None
    def parse_firstline(self) -> bool:
        if not self.comment: return False
        x = self.comment.find("\n")
        if x > 0:
            self.firstline = self.comment[:x]
            self.otherlines = self.comment[x:]
        elif x == 0:
            self.firstline = "..."
            self.otherlines = self.comment[1:x]
        else:
            self.firstline = self.comment
            self.otherlines = ""
        return True
    def get_firstline(self) -> str:
        if self.firstline is None:
            self.parse_firstline()
        return self.firstline or ""
    def get_otherlines(self) -> str:
        if self.firstline is None:
            self.parse_firstline()
        return self.otherlines or ""
    def parse_titleline(self) -> bool:
        """ split extra-notes from the firstline - keep only titleline """
        line = self.get_firstline()
        if line is None: return False
        self.titleline = line
        self.alsolist = []
        x = line.find("also:")
        if x > 0:
            self.titleline = line[:x]
            for also in line[x+5:].split(","):
                self.alsolist += [ also.strip() ]
        return True
    def get_alsolist(self) -> List[str]:
        """ gets the see-also notes from the firstline """
        if self.titleline is None:
            self.parse_titleline()
        return self.alsolist
    def get_titleline(self) -> str:
        """ gets firstline with see-also notes removed """
        if self.titleline is None:
            self.parse_titleline()
        return self.titleline or ""
    def get_title(self) -> str:
        """ gets titleline unless that is a redirect """
        titleline = self.get_titleline()
        if titleline & Match(r"^\s*=>"): return ""
        if titleline & Match(r"^\s*<link>"): return ""
        return titleline
    def get_prototype(self) -> Optional[str]:
        return self.prototype

class FunctionHeaderList:
    """ scan for comment blocks in the source file that are followed by
    something quite like a C definition (probably a function definition).
    Unpack the occurrences and fill self.comment and self.prototype. """
    textfile: Optional[TextFileHeader]
    children: Optional[List[FunctionHeader]]
    def __init__(self, textfile: Optional[TextFileHeader] = None) -> None:
        self.textfile = textfile # TextFile
        self.children = None     # src'style
    def parse(self, textfile: Optional[TextFileHeader]  = None) -> bool:
        if textfile is not None:
            self.textfile = textfile
        if self.textfile is None:
            return False
        text = self.textfile.get_src_text() or ""
        m = Match(r"(?s)\/\*[*]+(?=\s)"
                  r"((?:.(?!\*\/))*.)\*\/"
                  r"([^/\{\}\;\#]+)[\{\;]")
        self.children = []
        for found in m.finditer(text):
            child = FunctionHeader(self, found.group(1), found.group(2))
            self.children += [ child ]
        return len(self.children) > 0
    def src_mainheader(self) -> Optional[str]:
        if self.textfile:
            return self.textfile.src_mainheader()
        return None
    def get_filename(self) -> Optional[str]:
        if self.textfile:
            return self.textfile.get_filename()
        return None
    def get_children(self) -> List[FunctionHeader]:
        if self.children is None:
            self.parse()
        return self.children or []
