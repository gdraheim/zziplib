import re


class FunctionHeader(object):
    """ parsing the comment block that is usually presented before
    a function prototype - the prototype part is passed along
    for further parsing through => FunctionPrototype """

    def __init__(self, functionheaderlist, comment, prototype):
        self.parent = functionheaderlist  # type: FunctionHeaderList
        self.filename = self.parent.filename
        self.comment = comment  # type: str
        self.prototype = prototype  # type: str
        self.firstline = None
        self.otherlines = None
        self.titleline = None
        self.alsolist = []

        x = self.comment.find("\n")
        if x > 0:
            self.firstline = self.comment[:x]
            self.otherlines = self.comment[x:]
        elif x == 0:
            self.firstline = "..."
            self.otherlines = self.comment[1:x]
        else:
            self.firstline = self.comment
            self.otherlines = ""

        line = self.firstline
        self.titleline = line
        self.alsolist = []
        x = line.find("also:")
        if x > 0:
            self._titleline = line[:x]
            for also in line[x + 5:].split(","):
                self.alsolist += [also.strip()]
        self.alsolist = self.alsolist

    @property
    def title(self):
        """ gets titleline unless that is a redirect """
        titleline = self.titleline
        if titleline.strip().startswith("=>"): return ""
        if titleline.strip().startswith("<link>"): return ""
        return titleline


class FunctionHeaderList(object):
    """ scan for comment blocks in the source file that are followed by
    something quite like a C definition (probably a function definition).
    Unpack the occurrences and fill self.comment and self.prototype. """

    def __init__(self, textfile=None):
        self.textfile = textfile
        self.filename = textfile.filename

        text = textfile.src_text
        m = re.compile(
            r"(?s)/\*[*]+(?=\s)((?:.(?!\*/))*.)\*/([^/{};#]+)[{;]")
        self.children = [FunctionHeader(self, comment, prototype)
                         for comment, prototype in m.findall(text)]
