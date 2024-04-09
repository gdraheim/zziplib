#! /usr/bin/env python3
from typing import Optional, Union, Iterator, Callable, Any
import re

try:
    basestring # type: ignore[used-before-def]
except NameError:
    basestring = str

# ---------------------------------------------------------- Regex Match()
# beware, stupid python interprets backslashes in replace-parts only partially!
class MatchReplace:
    """ A MatchReplace is a mix of a Python Pattern and a Replace-Template """
    matching: "Match"
    template: Union[str, Callable[[Any], str]]
    def __init__(self, matching: Union[str, "Match"], template: Union[None, str, Callable[[Any], str]], count: int = 0, flags: Optional[str] = None) -> None:
        """ setup a substition from regex 'matching' into 'template',
            the replacement count default of 0 will replace all occurrences.
            The first argument may be a Match object or it is a string that
            will be turned into one by using Match(matching, flags). """
        MatchReplace.__call__(self, matching, template, count, flags)
    def __call__(self, matching: Union[str, "Match"], template: Union[None, str, Callable[[Any], str]] = None, count: int = 0, flags: Optional[str] = None) -> None:
        """ other than __init__ the template may be left off to be unchanged"""
        if isinstance(count, basestring): # count/flags swapped over?
            flags = count; count = 0
        if isinstance(matching, Match):
            self.matching = matching
        else:
            assert isinstance(matching, str)
            self.matching = Match()(matching, flags) ## python 2.4.2 bug
        if template is not None:
            self.template = template
        self.count = count
    def __and__(self, string: str) -> str:
        """ z = MatchReplace('foo', 'bar') & 'foo'; assert z = 'bar' """
        text, self.matching.replaced = \
              self.matching.regex.subn(self.template, string, self.count)
        return text
    def __rand__(self, string: str) -> str:
        """ z = 'foo' & Match('foo') >> 'bar'; assert z = 'bar' """
        text, self.matching.replaced = \
              self.matching.regex.subn(self.template, string, self.count)
        return text
    def __iand__(self, string: str) -> str:
        """ x = 'foo' ; x &= Match('foo') >> 'bar'; assert x == 'bar' """
        string, self.matching.replaced = \
                self.matching.regex.subn(self.template, string, self.count)
        return string
    def __rshift__(self, count: int) -> "MatchReplace":
        " shorthand to set the replacement count: Match('foo') >> 'bar' >> 1 "
        self.count = count ; return self
    def __rlshift__(self, count: int) -> "MatchReplace":
        self.count = count ; return self

class Match:
    """ A Match is actually a mix of a Python Pattern and MatchObject """
    pattern: Optional[str]
    replaced: int
    regex: re.Pattern[str]
    found: Optional[re.Match[str]]
    def __init__(self, pattern: Optional[str] = None, flags: Optional[str] = None) -> None:
        """ flags is a string: 'i' for case-insensitive etc.; it is just
        short for a regex prefix: Match('foo','i') == Match('(?i)foo') """
        Match.__call__(self, pattern, flags)
    def __call__(self, pattern: Optional[str], flags: Optional[str] = None) -> "Match":
        assert isinstance(pattern, str) or pattern is None
        assert isinstance(flags, str) or flags is None
        self.replaced = 0 # set by subn() inside MatchReplace
        self.found = None # set by search() to a MatchObject
        self.pattern = pattern
        if pattern is not None:
            if flags:
                self.regex = re.compile("(?"+flags+")"+pattern)
            else:
                self.regex = re.compile(pattern)
        return self
    def __repr__(self) -> str:
        return self.pattern or ""
    def __truth__(self) -> bool:
        return self.found is not None
    def __and__(self, string: str) -> bool:
        self.found = self.regex.search(string)
        return self.__truth__()
    def __rand__(self, string: str) -> bool:
        self.found = self.regex.search(string)
        return self.__truth__()
    def __rshift__(self, template: Union[str, Callable[[Any], str]]) -> MatchReplace:
        return MatchReplace(self, template)
    def __rlshift__(self, template: Union[str, Callable[[Any], str]]) -> MatchReplace:
        return MatchReplace(self, template)
    def __getitem__(self, index: int) -> str:
        return self.group(index)
    def group(self, index: int) -> str:
        assert self.found is not None
        return self.found.group(index)
    def finditer(self, string: str) -> Iterator[re.Match[str]]:
        return self.regex.finditer(string)

if __name__ == "__main__":
    # matching:
    if "foo" & Match("oo"):
        print("oo")
    x = Match()
    if "foo" & x("(o+)"):
        print(x[1])
    # replacing:
    y = "fooboo" & Match("oo") >> "ee"
    print(y)
    r = Match("oo") >> "ee"
    print("fooboo" & r)
    s = MatchReplace("oo", "ee")
    print("fooboo" & s)
