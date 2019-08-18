import cgi


class TextFile(object):
    def __init__(self, filename):
        self.filename = filename  # type: str
        with open(filename, "r") as fd:
            self.src_text = fd.read()
        self.xml_text = cgi.escape(self.src_text)  # type: str

    def __str__(self):
        return self.xml_text
