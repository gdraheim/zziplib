from __future__ import print_function
import re

from zzipdoc.textfile import TextFile


class TextFileHeader(object):
    """ scan for a comment block at the source file start and fill the
    inner text into self.comment - additionally scan for the first
    #include statement and put the includename into self.mainheader
    (TextFileHeader re-exports all => TextFile methods for processing)"""
    def __init__(self, textfile):  # type: (TextFile) -> None
        self.textfile = textfile
        self.comment = ""
        self.mainheader = ""

        text = textfile.src_text
        if not text:
            raise Exception("nonexistent file:", textfile.filename)

        comment = re.search(r"(?s)[/][*]+(\s(?:.(?!\*/))*.)\*/", text)
        if comment:
            self.comment = comment.group(1)

        mainheader = re.search(r"(?s)(?:\s*#(?:define|ifdef|endif)[ ]*\S*[ ]*\S*)*"
                               r"(\s*#include\s*<[^<>]*>(?:\s*//[^\n]*)?)",
                               text)
        if mainheader:
            self.mainheader = mainheader.group(1).strip()

    # re-export textfile functions - allows textfileheader to be used instead
    @property
    def filename(self):
        return self.textfile.filename

    @property
    def src_text(self):
        return self.textfile.src_text

    def __str__(self):
        return self.src_text
