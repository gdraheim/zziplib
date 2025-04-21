#! /usr/bin/python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=too-few-public-methods,consider-using-with

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Union, Optional
import logging

logg = logging.getLogger(__name__)

NIX = ""

def _src_to_xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt")

def decodes(text: Union[bytes, str, None]) -> str:
    if not text:
        return NIX
    if isinstance(text, bytes):
        try:
            return text.decode("utf-8") # type: ignore[union-attr]
        except UnicodeDecodeError:
            try:
                return text.decode("latin-1") # type: ignore[union-attr]
            except UnicodeDecodeError:
                return str(text)
    return text

class TextFile:
    filename: Optional[str]
    src_text: Optional[str]
    xml_text: Optional[str]
    def __init__(self, filename: Optional[str] = None) -> None:
        self.filename = filename
        self.src_text = None
        self.xml_text = None
    def parse(self, filename: Optional[str] = None) -> bool:
        if filename is not None:
            self.filename = filename
        if self.filename is None:
            return False
        try:
            fd = open(self.filename, "rb")
            self.src_text = decodes(fd.read())
            fd.close()
            return True
        except IOError as e:
            logg.info("could not write '%s': %s", self.filename, e)
        return False
    def assert_src_text(self) -> bool:
        if self.src_text: return True
        return self.parse()
    def assert_xml_text(self) -> bool:
        if self.xml_text: return True
        if not self.assert_src_text(): return False
        assert self.src_text is not None
        self.xml_text = _src_to_xml(self.src_text)
        return True
    def get_src_text(self) -> str:
        self.assert_src_text()
        assert self.src_text is not None
        return self.src_text
    def get_xml_text(self) -> str:
        self.assert_xml_text()
        assert self.xml_text is not None
        return self.xml_text
    def get_filename(self) -> Optional[str]:
        return self.filename
    def line_xml_text(self, offset: int) -> int:
        assert self.xml_text is not None
        return self._line(self.xml_text, offset)
    def line_src_text(self, offset: int) -> int:
        assert self.src_text is not None
        return self._line(self.src_text, offset)
    def _line(self, text: str, offset: int) -> int:
        line = 1
        for x in range(0,offset):
            if text[x] == "\n":
                line += 1
        return line
