#! /usr/bin/env python3

from zzipdoc.match import Match
from typing import Optional, Dict

# use as o.optionname to check for commandline options.
class Options:
    var: Dict[str, Optional[str]] = {}
    def __getattr__(self, name: str) -> Optional[str]:
        if not name in self.var: return None
        return self.var[name]
    def __setattr__(self, name: str, value: Optional[str]) -> None:
        self.var[name] = value
    def scan(self, optionstring: str) -> Optional[str]: # option-name or None
        x = Match()
        if optionstring & x(r"^--?(\w+)=(.*)"):
            self.var[x[1]] = x[2] ;  return x[1]
        if optionstring & x(r"^--?no-(\w+)$"):
            self.var[x[1]] = "" ; return x[1]
        if optionstring & x(r"^--?(\w+)$"):
            self.var[x[1]] = "*"; return x[1]
        return None
#end Options

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
    def scan(self, optionstring: str) -> Optional[str]: # option-name or None
        x = Match()
        if optionstring & x(r"^--?(\w+)=(.*)"):
            self.set(x[1], x[2]) ;  return x[1]
        if optionstring & x(r"^--?no-(\w+)$"):
            self.set(x[1], "") ; return x[1]
        if optionstring & x(r"^--?(\w+)$"):
            self.set(x[1], "*"); return x[1]
        return None
    def set(self, name: str, value: str) -> None:
        if name in ["package"]:
            self.package = value
        elif name in ["vesion"]:
            self.version = value
        elif name in ["program"]:
            self.program = value
        elif name in ["html"]:
            self.html = value
        elif name in ["docbook"]:
            self.docbook = value
        elif name in ["output"]:
            self.output = value
        elif name in ["suffix"]:
            self.suffix = value
        elif name in ["onlymainheader"]:
            self.onlymainheader = value
        elif name in ["body"]:
            self.body = value
        else:
            raise Exception("unknown option " + name)

if False:
    o = Options()
    o.help = """
    scans for options
    """
