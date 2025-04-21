#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Optional
from zzipdoc.match import Match
from zzipdoc.functionheader import FunctionHeader

class FunctionPrototype:
    """ takes a single function prototype line (cut from some source file)
    and parses it into the relevant portions 'prespec', 'namespec' and
    'callspec'. Additionally we present 'name' from the namespec that is
    usually used as the filename stem for a manual page """
    functionheader: Optional[FunctionHeader]
    prespec: Optional[str]
    namespec: Optional[str]
    callspec: Optional[str]
    name: Optional[str]
    def __init__(self, functionheader: Optional[FunctionHeader] = None) -> None:
        self.functionheader = functionheader
        self.prespec = None
        self.namespec = None
        self.callspec = None
        self.name = None
    def get_functionheader(self) -> Optional[FunctionHeader]:
        return self.functionheader
    def get_prototype(self) -> Optional[str]:
        if self.functionheader is None:
            return None
        return self.functionheader.get_prototype()
    def get_filename(self) -> Optional[str]:
        if self.functionheader is None:
            return None
        return self.functionheader.get_filename()
    def parse(self, functionheader: Optional[FunctionHeader] = None) -> bool:
        if functionheader is not None:
            self.functionheader = functionheader
        if self.functionheader is None:
            return False
        prototype = self.get_prototype()
        if not prototype:
            return False
        assert prototype is not None
        found = Match()
        if prototype & found(r"(?s)^(.*[^.])"
                             r"\b(\w[\w.]*\w)\b"
                             r"(\s*\(.*)$"):
            self.prespec = found.group(1).lstrip()
            self.namespec = found.group(2)
            self.callspec = found.group(3).lstrip()
            self.name = self.namespec.strip()
            return True
        return False
    def _assert_parsed(self) -> bool:
        if self.name is None:
            return self.parse()
        return True
    def get_prespec(self) -> Optional[str]:
        if not self._assert_parsed(): return None
        assert self.prespec is not None
        return self.prespec
    def get_namespec(self) -> Optional[str]:
        if not self._assert_parsed(): return None
        assert self.namespec is not None
        return self.namespec
    def get_callspec(self) -> Optional[str]:
        if not self._assert_parsed(): return None
        assert self.callspec is not None
        return self.callspec
    def get_name(self) -> Optional[str]:
        if not self._assert_parsed(): return None
        assert self.name is not None
        return self.name
    def xml_text(self) -> Optional[str]:
        prespec = self.prespec or ""
        callspec = self.callspec or ""
        namespec = self.namespec or ""
        if not namespec:
            return None
        return ("<fu:protospec><fu:prespec>"+prespec+"</fu:prespec>"+
                "<fu:namespec>"+namespec+"</fu:namespec>"+
                "<fu:callspec>"+callspec+"</fu:callspec></fu:protospec>")
