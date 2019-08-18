import re


def _markup_link_syntax(text):
    """ markup the link-syntax ` => somewhere ` in the text block """
    text = re.sub(r"(^|\s)=>\"([^\"]*)\"", r"\1<link>\2</link>", text,
                  flags=re.M)
    text = re.sub(r"(^|\s)=>\'([^\']*)\'", r"\1<link>\2</link>", text,
                  flags=re.M)
    text = re.sub(r"(^|\s)=>\s(\w[\w.]*\w\(\d+\))", r"\1<link>\2</link>", text,
                  flags=re.M)
    text = re.sub(r"(^|\s)=>\s([^\s,.!?]+)", r"\1<link>\2</link>", text,
                  flags=re.M)
    return text


def _markup_line(line):
    return (line
            .replace("<c>", "<code>")
            .replace("</c>", "</code>"))


def _markup_para_line(line):
    return _markup_link_syntax(_markup_line(line))


def _markup_screen_line(line):
    return _markup_line(line.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"))


class CommentMarkup(object):
    """ using a structure having a '.comment' item - it does pick it up
    and enhances its text with new markups so that they can be represented
    in xml. Use self.xml_text() to get markup text (knows 'this function') """

    def __init__(self, header):
        self.header = header
        self.filename = header.filename

        if hasattr(header, 'otherlines'):
            comment = header.otherlines
        else:
            comment = header.comment

        mode = ""
        text = ""
        for line in comment.split("\n"):
            check = re.search(r"^\s?\s?\s?[*]\s+[*]\s(.*)", line)
            if check:
                if mode != "ul":
                    if mode: text += "</" + mode + ">"
                    mode = "ul"
                    text += "<" + mode + ">"
                line = check.group(1)
                text += "<li><p> " + _markup_para_line(line) + " </p></li>\n"
            else:
                check = re.search(r"^\s?\s?\s?[*](.*)", line)
                if check:
                    if mode != "para":
                        if mode: text += "</" + mode + ">"
                        mode = "para";
                        text += "<" + mode + ">"
                    line = check.group(1)
                    if line.strip() == "":
                        text += "</para><para>" + "\n"
                    else:
                        text += " " + _markup_para_line(line) + "\n"
                else:
                    if mode != "screen":
                        if mode: text += "</" + mode + ">"
                        mode = "screen"
                        text += "<" + mode + ">"
                    text += " " + _markup_screen_line(line) + "\n"
        if mode:
            text += "</" + mode + ">" + "\n"
        text = re.sub(r"(<para>)(\s*[R]eturns)", r"\1This function\2", text)
        text = re.sub(r"<para>\s*</para><para>", "<para>", text, flags=re.S)
        text = re.sub(r"<screen>\s*</screen>", "", text, flags=re.S)
        self.text = text

    def xml_text(self, functionname=None):
        text = self.text
        if functionname is not None:
            def function(name):
                return "<function>" + name + "</function> function"

            text = (text
                    .replace("this function", "the " + function(functionname))
                    .replace("This function", "The " + function(functionname)))
        return text
