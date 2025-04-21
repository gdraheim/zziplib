#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=too-few-public-methods

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

from typing import Optional, List

class HtmlDocPart:
    def xml_text(self) -> Optional[str]:
        return None
    def html_text(self) ->  Optional[str]:
        return None
    def get_title(self) -> str:
        return ""

class HtmlStylePart:
    def xml_style(self) -> str:
        return ""
    def html_style(self) -> str:
        return ""

class HtmlMetaPart:
    def html_meta(self) -> str:
        return ""

class RefDocPart:
    def head_xml_text(self) -> Optional[str]:
        return None
    def body_xml_text(self, name: Optional[str]) -> Optional[str]: # pylint: disable=unused-argument
        return None
    def get_name(self) -> Optional[str]:
        return None
    def head_get_prespec(self) -> Optional[str]:
        return None
    def head_get_namespec(self) -> Optional[str]:
        return None
    def head_get_callspec(self) -> Optional[str]:
        return None
    def get_title(self) -> Optional[str]:
        return None
    def get_filename(self) -> Optional[str]:
        return None
    def get_mainheader(self) -> Optional[str]:
        return None
    def get_includes(self) -> Optional[str]:
        return None
    def list_seealso(self) -> List[str]:
        return []
    def get_authors(self) -> Optional[str]:
        return None
    def get_copyright(self) -> Optional[str]:
        return None

class DocOptions:
    package = ""
    program = ""
    html = "html"
    docbook = "docbook"
    output = ""
    suffix = ""
    onlymainheader = ""
    version = ""
    body = ""
