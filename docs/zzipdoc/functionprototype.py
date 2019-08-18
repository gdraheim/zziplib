import re


class FunctionPrototype(object):
    """ takes a single function prototype line (cut from some source file)
    and parses it into the relevant portions 'prespec', 'namespec' and
    'callspec'. Additionally we present 'name' from the namespec that is
    usually used as the filename stem for a manual page """
    def __init__(self, functionheader=None):
        self.functionheader = functionheader
        self.prototype = self.functionheader.prototype
        self.filename = self.functionheader.filename
        found = re.search(r"(?s)^(.*[^.])"
                          r"\b(\w[\w.]*\w)\b"
                          r"(\s*\(.*)$",
                          self.prototype)
        if not found:
            raise Exception("Function prototype regex did not grab anything")

        self.prespec = found.group(1).lstrip()
        self.namespec = found.group(2)
        self.callspec = found.group(3).lstrip()
        self.name = self.namespec.strip()

    def __str__(self):
        return ("<fu:protospec><fu:prespec>"+self.prespec+"</fu:prespec>"+
                "<fu:namespec>"+self.namespec+"</fu:namespec>"+
                "<fu:callspec>"+self.callspec+"</fu:callspec></fu:protospec>")
