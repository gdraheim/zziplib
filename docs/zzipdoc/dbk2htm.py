import re

_mapping = {
    "<screen>": "<pre>",
    "</screen>": "</pre>",
    "<para>": "<p>",
    "</para>": "</p>" ,
    "<function>": "<link>",
    "</function>": "</link>",
}


def section2html(text):
    for find, replace in _mapping.items():
        text = text.replace(find, replace)
    return text


def paramdef2html(text):
    text = re.sub(r"\s+<paramdef>", r"\n<nobr>", text)
    text = text.replace("<paramdef>", "<nobr>")
    text = text.replace("</paramdef>", "</nobr>")
    text = text.replace("<parameters>", "\n <code>")
    text = text.replace("</parameters>", "</code>\n")
    return text
