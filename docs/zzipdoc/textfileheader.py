#! /usr/bin/python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=too-few-public-methods,no-else-return

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Optional
from zzipdoc.match import Match
from zzipdoc.textfile import TextFile

class TextFileHeader:
    """ scan for a comment block at the source file start and fill the
    inner text into self.comment - additionally scan for the first
    #include statement and put the includename into self.mainheader
    (TextFileHeader re-exports all => TextFile methods for processing)"""
    textfile: Optional[TextFile]
    comment: str
    mainheader: str
    def __init__(self, textfile: Optional[TextFile] = None):
        self.textfile = textfile # TextFile
        self.comment = ""    # src'style
        self.mainheader = ""     # src'style
    def parse(self, textfile: Optional[TextFile] = None) -> bool:
        if textfile is not None:
            self.textfile = textfile
        if self.textfile is None:
            return False
        assert self.textfile is not None
        x = Match()
        text = self.textfile.get_src_text()
        if not text:
            filename = self.textfile.get_filename() or "_"
            print("nonexistent file: " + filename)
            return False
        if text & x(r"(?s)[/][*]+(\s(?:.(?!\*\/))*.)\*\/"
                    r"(?:\s*\#(?:define|ifdef|endif)[ ]*\S*[ ]*\S*)*"
                    r"(\s*\#include\s*<[^<>]*>(?:\s*//[^\n]*)?)"):
            self.comment = x[1]
            self.mainheader = x[2].strip()
        elif text & x(r"(?s)[/][*]+(\s(?:.(?!\*\/))*.)\*\/"):
            self.comment = x[1]
        elif text & x(r"(?s)(?:\s*\#(?:define|ifdef|endif)[ ]*\S*[ ]*\S*)*"
                      r"(\s*\#include\s*<[^<>]*>(?:\s*//[^\n]*)?)"):
            self.mainheader = x[1].strip()
        return True
    def src_mainheader(self) -> str:
        return self.mainheader
    def src_filecomment(self) -> str:
        return self.comment
    # re-export textfile functions - allows textfileheader to be used instead
    def get_title(self) -> Optional[str]:
        if not self.textfile:
            return None
        else:
            return self.textfile.get_filename()
    def get_filename(self) -> Optional[str]:
        if not self.textfile:
            return None
        else:
            return self.textfile.get_filename()
    def get_src_text(self) -> Optional[str]:
        if not self.textfile:
            return None
        else:
            return self.textfile.get_src_text()
    def get_xml_text(self) -> Optional[str]:
        if not self.textfile:
            return None
        else:
            return self.textfile.get_src_text()
    def line_src__text(self, offset: int) -> int:
        if not self.textfile:
            return 0
        else:
            return self.textfile.line_src_text(offset)
    def line_xml__text(self, offset: int) -> int:
        if not self.textfile:
            return 0
        else:
            return self.textfile.line_xml_text(offset)
