#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=too-many-branches,too-many-return-statements,too-many-statements,too-many-instance-attributes,no-else-return
# pylint: disable=invalid-name,unspecified-encoding,consider-using-with
""" use pygments.lexer.CLexer to scan for C comment blocks and convert to basic markdown format """

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Iterator, Tuple
import os
import re
import sys
import logging
import pygments.lexers.compiled as lexer

from pygments.token import Token

logg = logging.getLogger("CPP2MD")

OK = True
TODO = False
FileComment = "FileComment"
FileInclude = "FileInclude"
FunctionComment = "FunctionComment"
FunctionPrototype = "FunctionPrototype"

# use the markdown lexer to identify elements
# then filter only those we want. The returned
# token list is more global flagging the role
# of each token for the manual generation.
class CppToMarkdown:
    def __init__(self) -> None:
        self.alldefinitions = 0
        self.internaldefs = ["static"]
        self.filecomment_done = ""
        self.fileinclude_done = ""
        self.filecomment_text = ""
        self.fileinclude_text = ""
        self.comment_text = ""
        self.function_text = ""
        self.nesting = 0
    def commentblock(self, text: str) -> str:
        emptyprefix = re.compile(r"(?s)^\s*[/][*]+[ \t]*(?=\n)")
        prefix = re.compile(r"(?s)^\s*[/][*]+([^\n]*)(?=\n)")
        suffix = re.compile(r"(?s)\n [*][/]\s*")
        empty = re.compile(r"(?s)\n [*][ \t]*(?=\n)")
        lines1 = re.compile(r"(?s)\n [*][ ][\t]")
        lines2 = re.compile(r"(?s)\n [*][ ]")
        lines3 = re.compile(r"(?s)\n [*][\t][\t]")
        lines4 = re.compile(r"(?s)\n [*][\t]")
        text = suffix.sub("\n", text)
        text = emptyprefix.sub("", text)
        text = prefix.sub("> \\1\n", text)
        text = empty.sub("\n", text)
        text = lines1.sub("\n     ", text)
        text = lines2.sub("\n", text)
        text = lines3.sub("\n         ", text)
        text = lines4.sub("\n     ", text)
        return text
    def functionblock(self, text: str) -> str:
        empty = re.compile(r"(?s)\n[ \t]*(?=\n)")
        text = "    " + text.replace("\n", "\n    ")
        text = empty.sub("", text)
        return text
    def functionname(self, text: str) -> str:
        check1 = re.compile(r"^[^()=]*(\b\w+)\s*[(=]")
        found = check1.match(text)
        if found:
            return found.group(1)
        check2 = re.compile(r"^[^()=]*(\b\w+)\s*$")
        found = check2.match(text)
        if found:
            return found.group(1)
        return ""
    def run(self, filename: str) -> None:
        filetext = open(filename).read()
        for line in self.process(filetext, filename):
            print(line)
    def process(self, filetext:str, filename: str ="") -> Iterator[str]:
        for token, text in self.parse(filetext):
            if token == FileInclude:
                yield "## SOURCE " + filename.replace("../", "")
                yield "    #" + text.replace("\n", "\n    ")
            elif token == FileComment:
                yield "## INTRODUCTION"
                yield self.commentblock(text)
            elif token == FunctionPrototype:
                name = self.functionname(text)
                yield "-----------------------------------------"
                yield "### " + name
                yield "#### NAME"
                yield "    " + name
                yield "#### SYNOPSIS"
                yield self.functionblock(text)
            elif token == FunctionComment:
                if text:
                    yield "#### DESCRIPTION"
                    yield self.commentblock(text)
            else:
                if text:
                    yield "#### NOTES"
                    print(token + " " + text.replace("\n", "\n  "))
    def isexported_function(self) -> bool:
        function = self.function_text.strip().replace("\n"," ")
        logg.debug("@ --------------------------------------")
        logg.debug("@ ALLDEFINITIONS %s", self.alldefinitions)
        if function.startswith("static ") and self.alldefinitions < 3:
            logg.debug("@ ONLY INTERNAL %s", function)
            return False
        if not self.comment_text:
            if not self.alldefinitions:
                logg.info("@ NO COMMENT ON %s", function)
                return False
            else:
                logg.warning("@ NO COMMENT ON %s", function)
        text = self.comment_text
        if text.startswith("/**"): return True
        if text.startswith("/*!"): return True
        if text.startswith("///"): return True
        if text.startswith("//!"): return True
        if self.alldefinitions >= 1:
            if text.startswith("/*"): return True
            if text.startswith("//"): return True
        if self.alldefinitions >= 2:
            return True
        logg.debug("@ NO ** COMMENT %s", self.function_text.strip())
        if not TODO:
            defs = self.function_text # pylint: disable=unused-variable
        return False
    def parse(self, filetext: str) -> Iterator[Tuple[str,str]]:
        c = lexer.CLexer()
        for token, text in c.get_tokens(filetext):
            logg.debug("|| %s %s", token, text.replace("\n", "\n |"))
            # completion
            if token != Token.Comment.Preproc and self.fileinclude_done == "no":
                if OK:
                    yield FileInclude, self.fileinclude_text
                    if self.filecomment_text:
                        yield FileComment, self.filecomment_text
                    self.fileinclude_done = "done"
            # parsing
            if token == Token.Comment.Multiline:
                if not self.filecomment_done:
                    self.filecomment_done = "done"
                    self.filecomment_text = text
                    # wait until we know it is not a function documentation
                    self.comment_text = text
                else:
                    self.comment_text = text
            elif token == Token.Comment.Preproc and "include" in text:
                if not self.fileinclude_done:
                    self.fileinclude_done = "no"
                    self.fileinclude_text += text
                    self.comment_text = ""
            elif token == Token.Comment.Preproc and self.fileinclude_done == "no":
                if "\n" not in self.fileinclude_text:
                    self.fileinclude_text += text
                self.comment_text = ""
            elif token == Token.Comment.Preproc:
                if OK:
                    self.comment_text = ""
                    self.function_text = ""
            elif token == Token.Operator and text == "=":
                if not self.nesting and self.function_text.strip():
                    if self.isexported_function():
                        yield FunctionPrototype, self.function_text
                        yield FunctionComment, self.comment_text
                self.comment_text = ""
                self.function_text = ""
            elif token == Token.Punctuation and text == ";":
                self.comment_text = ""
                self.function_text = ""
            elif token == Token.Punctuation and text == "{":
                if not self.nesting and self.function_text.strip():
                    if self.isexported_function():
                        yield FunctionPrototype, self.function_text
                        yield FunctionComment, self.comment_text
                self.comment_text = ""
                self.function_text = ""
                self.nesting += 1
            elif token == Token.Punctuation and text == "}":
                self.nesting -= 1
                self.comment_text = ""
                self.function_text = ""
            else:
                if not self.nesting:
                    self.function_text += text
                else:
                    pass # yield "|",text


def main() -> int:
    import optparse # pylint: disable=deprecated-module,import-outside-toplevel
    cmdline = optparse.OptionParser("%prog files..", epilog=__doc__)
    cmdline.add_option("-v", "--verbose", action="count", default=0, help="more logging")
    cmdline.add_option("-^", "--quiet", action="count", default=0, help="less logging")
    cmdline.add_option("-?", "--version", action="count", default=0, help="author info")
    cmdline.add_option("-a", "--all", action="count", default=0,
                  help="include all definitions in the output (not only /**)")
    opt, cmdline_args = cmdline.parse_args()
    logging.basicConfig(level = max(0, logging.WARNING - 10 * opt.verbose + 10 * opt.quiet))
    logg.addHandler(logging.StreamHandler())
    if opt.version:
        print("version:", __version__)
        print("contact:", __contact__)
        print("license:", __license__)
        print("authors:", __copyright__)
        return os.EX_OK
    c = CppToMarkdown()
    if opt.all:
        c.alldefinitions = opt.all
    for arg in cmdline_args:
        c.run(arg)
    return os.EX_OK

if __name__ == "__main__":
    sys.exit(main())
