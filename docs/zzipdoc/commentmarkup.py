#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=too-many-branches

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Optional
from zzipdoc.match import Match
from zzipdoc.textfileheader import TextFileHeader
from zzipdoc.functionheader import FunctionHeader

def markup_link_syntax(text: str) -> str:
    """ markup the link-syntax ` => somewhere ` in the text block """
    return (text
            & Match(r"(?m)(^|\s)\=\>\"([^\"]*)\"")
            >> r"\1<link>\2</link>"
            & Match(r"(?m)(^|\s)\=\>\'([^\']*)\'")
            >> r"\1<link>\2</link>"
            & Match(r"(?m)(^|\s)\=\>\s(\w[\w.]*\w\(\d+\))")
            >> r"\1<link>\2</link>"
            & Match(r"(?m)(^|\s)\=\>\s([^\s\,\.\!\?]+)")
            >> r"\1<link>\2</link>")

class CommentMarkupSource:
    def get_comment(self) -> Optional[str]:
        return None
    def get_filename(self) -> Optional[str]:
        return None

class CommentMarkup:
    """ using a structure having a '.comment' item - it does pick it up
    and enhances its text with new markups so that they can be represented
    in xml. Use self.xml_text() to get markup text (knows 'this function') """
    text: Optional[str]
    src: CommentMarkupSource
    def __init__(self, src: CommentMarkupSource) -> None:
        self.src = src
        self.text = None     # xml'text
    def get_filename(self) -> Optional[str]:
        return self.src.get_filename()
    def parse(self, src: Optional[CommentMarkupSource] = None) -> bool:
        if src is not None:
            self.src = src
        comment = self.src.get_comment() or ""
        mode = ""
        text = ""
        for line in comment.split("\n"):
            check = Match()
            if line & check(r"^\s?\s?\s?[*]\s+[*]\s(.*)"):
                if mode != "ul":
                    if mode: text += "</"+mode+">"
                    mode = "ul" ; text += "<"+mode+">"
                line = check.group(1)
                text += "<li><p> "+self.markup_para_line(line)+" </p></li>\n"
            elif line & check(r"^\s?\s?\s?[*](.*)"):
                if mode != "para":
                    if mode: text += "</"+mode+">"
                    mode = "para" ; text += "<"+mode+">"
                line = check.group(1)
                if line.strip() == "":
                    text += "</para><para>"+"\n"
                else:
                    text += " "+self.markup_para_line(line)+"\n"
            else:
                if mode != "screen":
                    if mode: text += "</"+mode+">"
                    mode = "screen" ; text += "<"+mode+">"
                text += " "+self.markup_screen_line(line)+"\n"
        if mode: text += "</"+mode+">"+"\n"
        self.text = (text
                     & Match(r"(<para>)(\s*[R]eturns)") >>r"\1This function\2"
                     & Match(r"(?s)<para>\s*</para><para>") >> "<para>"
                     & Match(r"(?s)<screen>\s*</screen>") >> "")
        return True
    def markup_screen_line(self, line: str) -> str:
        return self.markup_line(line.replace("&","&amp;")
                                .replace("<","&lt;")
                                .replace(">","&gt;"))
    def markup_para_line(self, line: str) -> str:
        return markup_link_syntax(self.markup_line(line))
    def markup_line(self, line: str) -> str:
        return (line
                .replace("<c>","<code>")
                .replace("</c>","</code>"))
    def xml_text(self, functionname: Optional[str] = None) -> Optional[str]:
        if self.text is None:
            if not self.parse(): return None
            assert self.text is not None
        text = self.text
        if functionname is not None:
            def function(text: str) -> str: return "<function>"+text+"</function> function"
            text = (text
                    .replace("this function", "the "+function(functionname))
                    .replace("This function", "The "+function(functionname)))
        return text

class CommentMarkupFunctionHeader(CommentMarkup, CommentMarkupSource):
    def __init__(self, header: FunctionHeader) -> None:
        CommentMarkup.__init__(self, self)
        self.header = header
    def get_comment(self) -> Optional[str]:
        return self.header.get_otherlines()
    def get_filename(self) -> Optional[str]:
        return self.header.get_filename()

class CommentMarkupTextFileHeader(CommentMarkup, CommentMarkupSource):
    def __init__(self, header: TextFileHeader) -> None:
        CommentMarkup.__init__(self, self)
        self.header = header
    def get_comment(self) -> Optional[str]:
        return self.header.comment
    def get_filename(self) -> Optional[str]:
        return self.header.get_filename()
