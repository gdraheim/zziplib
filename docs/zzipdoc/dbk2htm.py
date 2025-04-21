#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements

from zzipdoc.match import Match

class dbk2htm_conversion:
    mapping = { "<screen>" : "<pre>", "</screen>" : "</pre>",
                "<para>" : "<p>", "</para>" : "</p>" ,
                "<function>" : "<link>", "</function>" : "</link>" }
    def __init__(self) -> None:
        pass
    def section2html(self, text: str) -> str:
        for markup, replace in self.mapping.items():
            text = text.replace(markup, replace)
        return text
    def paramdef2html(self, text: str) -> str:
        s = Match()
        txt = text & s(r"\s+<paramdef>") >> r"\n<nobr>"
        txt &= s(r"<paramdef>") >> r"<nobr>"
        txt &= s(r"</paramdef>") >> r"</nobr>"
        txt &= s(r"<parameters>") >> r"\n <code>"
        txt &= s(r"</parameters>") >> r"</code>\n"
        return txt

def section2html(text: str) -> str:
    return dbk2htm_conversion().section2html(text)
def paramdef2html(text: str) -> str:
    return dbk2htm_conversion().paramdef2html(text)
