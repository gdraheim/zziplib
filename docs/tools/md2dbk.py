#! /usr/bin/python3

from __future__ import print_function, absolute_import, division

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.74"

from typing import List, Generator, Optional
import re
from html import escape

import logging
logg = logging.getLogger("MD2DBK")

SingleUnderscore = False
SingleAsterisk = False

hint = """ The markdown syntax as clarified by CommonMark wants to make sure that parsers
can be written easily. That comes from a first pass to detect the block structure
and a second pass to convert the markup within. As such you should make sure that
after each block there is an empty line. As such, to put empty lines into a block
you need to use some kind of fenced block. The GFM (github flavoured markdown)
clarifies that fenced blocks do not need a blank line before or after. Text lines
not inside a fenced block will always be added rstrip()ed to the block."""

class ContainerMarkup:
    newBQ = ""  # default "<BQ>"
    endBQ = ""  # default "</BQ>"
    newUL = ""  # default "<UL>"
    endUL = ""  # default "</UL>"
    newLI = ""  # default "<LI>"
    endLI = ""  # default "</LI>"
    endnewLI = ""  # default "</LI><LI>"
    BQ = "blockquote"
    UL = "itemizedlist"
    LI = "listitem"
    preSE1 = "# "
    preSE2 = "## "
    preHR1 = "--- "
    preHR2 = "--- "
    preHR3 = "--- "

def blocks(text: str) -> List[str]:
    logg.debug(">> (%i)", len(text))
    blocks: List[str] = []
    for block in _blocks(text):
        blocks.append(block)
    return blocks
def _blocks(input: str, mark: Optional[ContainerMarkup] = None) -> Generator[str, None, None]:
    """ this function cuts the input string into text blocks.
    The original text content is not modified but some additional
    container blocks are generated which return the single-line 
    xml start/stop tag of blockquote and itemizedlist."""
    mark = mark or ContainerMarkup()
    logg.debug(">> (%i)", len(input))
    text = ""
    fenced = ""  # or indent or html
    blockquote = ""
    listblock = ""
    for nextline in input.splitlines():
        logg.debug("| %s", nextline)
        line = nextline
        endblockquote = []
        if blockquote:
            newblock = ""
            _blockquote1 = re.match("([>]+)(\\s*)$", nextline)
            _blockquote2 = re.match("([>]+)\\s(.*)", nextline)
            if _blockquote1:
                newblock = _blockquote1.group(1)
                line = _blockquote1.group(2)
            elif _blockquote2:
                newblock = _blockquote2.group(1)
                line = _blockquote2.group(2)
            if fenced:
                pass
            elif blockquote.count(">") < newblock.count(">"):
                for newdepth in range(blockquote.count(">"), newblock.count(">")):
                    yield mark.newBQ or "<%s>" % mark.BQ
                blockquote = newblock
            elif newblock.count(">") < blockquote.count(">"):
                for newdepth in range(newblock.count(">"), blockquote.count(">")):
                    if text:
                        yield text
                        text = ""
                    endblockquote += [mark.endBQ or "</%s>" % mark.BQ]
                blockquote = newblock  # may become empty
        if listblock:
            newblock = ""
            _indents = re.match("( *)(.*)", line)
            _newlist1 = re.match("([*]+)(\\s*)$", line)
            _newlist2 = re.match("([*]+)\\s(.*)", line)
            if _newlist1 or _newlist2:
                if _newlist1:
                    newblock = _newlist1.group(1)
                if _newlist2:
                    newblock = _newlist2.group(1)
            assert _indents is not None
            indent = _indents.group(1)
            # if less indent then end listblock
            if len(indent) >= len(listblock):
                pass
            elif fenced:
                pass
            elif listblock.count("*") < newblock.count("*"):
                for newdepth in range(listblock.count("*"), newblock.count("*")):
                    if text:
                        yield text
                        text = ""
                    yield mark.newUL or "<%s>" % mark.UL
                    yield mark.newLI or "<%s>" % mark.LI
                listblock = newblock
            elif newblock.count("*") < listblock.count("*"):
                for newdepth in range(newblock.count("*"), listblock.count("*")):
                    if text:
                        yield text
                        text = ""
                    yield mark.endLI or "</%s>" % mark.LI
                    yield mark.endUL or "</%s>" % mark.UL
                listblock = newblock  # may become empty
                if _newlist1 or _newlist2:
                    yield mark.newLI or "<%s>" % mark.LI
            else:
                if True:
                    if text:
                        yield text
                        text = ""
                if mark.endnewLI:
                    yield mark.endnewLI
                else:
                    yield (mark.endLI or "</%s>" % mark.LI) + (mark.newLI or "<%s>" % mark.LI)
        for newblock in endblockquote:
            yield newblock
        if not line.strip():
            if not fenced:
                if text:
                    yield text
                    text = ""
                continue
        # check to end an html block
        if fenced.startswith("<"):
            if fenced == "<script":
                if "</script>" in line:
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if fenced == "<pre":
                if "</pre>" in line:
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if fenced == "<style":
                if "</style>" in line:
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if fenced == "<![CDATA[":
                if "]]>" in line:
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if fenced == "<!--":
                if "-->" in line:
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if fenced == "<!":
                if ">" in line:
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if fenced == "<?":
                text += line + "\n"
                if "?>" in line:
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if fenced.startswith("</"):
                if fenced in line:
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
            if not line.strip():
                yield text
                text = ""
                fenced = ""
                continue
            # or else
            text += line + "\n"
            continue
        # check to start an html block
        if not fenced and not text and line.startswith("<"):
            if re.search("^[<]script(>| |$)", line):
                fenced = "<script"
                text = line + "\n"
                continue
            if re.search("^[<]pre(>| |$)", line):
                fenced = "<pre"
                text = line + "\n"
                continue
            if re.search("^[<]style(>| |$)", line):
                fenced = "<style"
                text = line + "\n"
                continue
            if line.startswith("<![CDATA["):
                fenced = "<![CDATA["
                text = line + "\n"
                continue
            if line.startswith("<!--"):
                fenced = "<!--"
                text = line + "\n"
                continue
            if line.startswith("<!"):
                fenced = "<!"
                text = line + "\n"
                continue
            if line.startswith("<?"):
                fenced = "<?"
                text = line + "\n"
                continue
            tag = re.match("<(\\w+>)", line)
            if tag:
                fenced = "</" + tag.group(1)
                text = line + "\n"
                continue
            tag = re.match("<(\\w+) [ ]*\\w+=[^<>]*>", line)
            if tag:
                fenced = "</" + tag.group(1) + ">"
                text = line + "\n"
                continue
        # check for indented code blocks
        if re.match("^    .*", line):
            m = re.match("^( *).*", line)
            assert m is not None
            indent = m.group(1)
            if not fenced and not text:
                text = line
                fenced = indent
                continue
            if fenced and indent.startswith(fenced):
                text += line + "\n"
                continue
        if fenced.startswith(" "):
            if not line.strip():
                text += line
                continue
            # not enough indent
            if text:
                yield text
                text = ""
            fenced = ""
            # fallthrough
        if line.strip().startswith("```"):
            if not fenced:
                if text:
                    yield text
                    text = ""
                fenced = line[:line.rfind("`") + 1]
                text = line + "\n"
                logg.debug("> fenced = '%s'", fenced)
                continue
            if fenced.strip().startswith("```"):
                if line.startswith(fenced):
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
        if line.strip().startswith("~~~"):
            if not fenced:
                if text:
                    yield text
                    text = ""
                fenced = line[:line.rfind("~") + 1]
                text = line + "\n"
                logg.debug("> fenced = '%s'", fenced)
                continue
            if fenced.strip().startswith("~~~"):
                if line.startswith(fenced):
                    text += line + "\n"
                    yield text
                    text = ""
                    fenced = ""
                    continue
        if fenced:
            text += line + "\n"
            continue
        # setext headers should not be paragraphs or thematic brakes
        # ... unlike GFM we do simply required atleast 3 "=" or "-"
        if re.match(" ? ? ?[=][=][=][=]* *$", line):
            if not text.strip(): pass
            elif re.match("^ ? ? ?[#][#]* .*", text): pass
            elif re.match("^ ? ? ?[-][-]* .*", text): pass
            elif re.match("^ ? ? ?[>][>]* .*", text): pass
            else:
                text = mark.preSE1 + text  # level 1 sections
                continue
        if re.match(" ? ? ?[-][-][-][-]* *$", line):
            if not text.strip(): pass
            elif re.match("^ ? ? ?[#][#]* .*", text): pass
            elif re.match("^ ? ? ?[-][-]* .*", text): pass
            elif re.match("^ ? ? ?[>][>]* .*", text): pass
            else:
                text = mark.preSE2 + text  # level 2 section
                continue
        # thematic breaks allow a lot of space characters in GFM
        if re.match(" ? ? ?[*] *[*] *[*] *[* ]*$", line):
            if text:
                yield text
                text = ""
            yield mark.preHR1 + line
            continue
        if re.match("^ ? ? ?[-] *[-] *[-] *[- ]*$", line):
            if text:
                yield text
                text = ""
            yield mark.preHR2 + line
            continue
        if re.match("^ ? ? ?[_] *[_] *[_] *[_ ]*$", line):
            if text:
                yield text
                text = ""
            yield mark.preHR3 + line
            continue
        endblockquote = []
        _blockquote1 = re.match("([>]+)(\\s*)$", nextline)
        _blockquote2 = re.match("([>]+)\\s(.*)", nextline)
        if _blockquote1 or _blockquote2:
            newblock = ""
            if _blockquote1:
                newblock = _blockquote1.group(1)
                line = _blockquote1.group(2)
            if _blockquote2:
                newblock = _blockquote2.group(1)
                line = _blockquote2.group(2)
            # assert not fenced
            if blockquote.count(">") < newblock.count(">"):
                for newdepth in range(blockquote.count(">"), newblock.count(">")):
                    yield mark.newBQ or "<%s>" % mark.BQ
                blockquote = newblock
            elif newblock.count(">") < blockquote.count(">"):
                for newdepth in range(newblock.count(">"), blockquote.count(">")):
                    if text:
                        yield text
                        text = ""
                    endblockquote += [mark.endBQ or "</%s>" % mark.BQ]
                blockquote = newblock  # may become empty
        _newlist1 = re.match("([*]+)(\\s*)$", line)
        _newlist2 = re.match("([*]+)\\s(.*)", line)
        if _newlist1 or _newlist2:
            newblock = ""
            if _newlist1:
                newblock = _newlist1.group(1)
            if _newlist2:
                newblock = _newlist2.group(1)
            # assert not fenced
            if listblock.count("*") < newblock.count("*"):
                for newdepth in range(listblock.count("*"), newblock.count("*")):
                    if text:
                        yield text
                        text = ""
                    yield mark.newUL or "<%s>" % mark.UL
                    yield mark.newLI or "<%s>" % mark.LI
                listblock = newblock
            elif newblock.count("*") < listblock.count("*"):
                for newdepth in range(newblock.count("*"), listblock.count("*")):
                    if text:
                        yield text
                        text = ""
                    yield mark.endLI or "</%s>" % mark.LI
                    yield mark.endUL or "</%s>" % mark.UL
                listblock = newblock  # may become empty
                if _newlist1 or _newlist2:
                    yield mark.newLI or "<%s>" % mark.LI
            else:
                if text:
                    yield text
                    text = ""
                    if mark.endnewLI:
                        yield mark.endnewLI
                    else:
                        yield (mark.endLI or "</%s>" % mark.LI) + (mark.newLI or "<%s>" % mark.LI)
            listblock = newblock
        for newblock in endblockquote:
            yield newblock
        # or else
        if line.rstrip():
            text += line.rstrip() + "\n"
    if text:
        yield text
        text = ""
    for olddepth in range(listblock.count("*")):
        yield mark.endLI or "</%s>" % mark.LI
        yield mark.endUL or "</%s>" % mark.UL
        listblock = ""
    for olddepth in range(blockquote.count(">")):
        yield mark.endBQ or "</%s>" % mark.BQ
        blockquote = ""

def xmlblocks(text: str) -> List[str]:
    """ Combines _blocks() and _xml() conversion, so that a full
        text becomes a series of xml snippets in docbook format."""
    blocks: List[str] = []
    for block in _blocks(text):
        blocks += _xmlblocks(block)
    return blocks

def firstline(block: str) -> str:
    x = block.find("\r")
    y = block.find("\n")
    if x >= 0 and y >= 0:
        return block[:min(x, y)]
    elif x >= 0 or y >= 0:
        return block[:max(x, y)]
    return block

def _xmlblocks(block: str) -> List[str]:
    """ Given a text block from the _blocks() sequence the text is
    converted into a series of xml snippets. Blocks from multiple 
    files may be concatenatd in this stream. """
    line = firstline(block)
    # html is passed through as such
    if line.startswith("<"):
        if re.search("^[<]script(>| |$)", line):
            return [block]
        if re.search("^[<]pre(>| |$)", line):
            return [block]
        if re.search("^[<]style(>| |$)", line):
            return [block]
        if line.startswith("<![CDATA["):
            return [block]
        if line.startswith("<!--"):
            return [block]
        if line.startswith("<!"):
            return [block]
        if line.startswith("<?"):
            return [block]
        tag = re.match("(</?(\\w+)>)", line)
        if tag:
            if tag.group(2) in ["blockquote", "itemizedlist", "date"]:
                return [block]
            else:
                return ["<para>" + block + "</para>"]
        tag = re.match("(</?(\\w+) [ ]*\\w+=[^<>]*>)", line)
        if tag:
            if True:
                return [block]
    # indended code needs to be escaped
    if re.match("^    .*", line):
        return ["<pre>%s</pre>" % escape(block)]
    if line.strip().startswith("```"):
        result = ""
        x = line.find("`")
        y = line.rfind("`")
        indent = line[x]
        fenced = line[:y + 1]
        for nextline in block.splitlines():
            if not result:  # first line
                y = nextline.rfind("`")
                info = nextline[y + 1:]
                if info:
                    result = "<screen info=\"%s\">" % escape(info)
                else:
                    result = "<screen>"
                continue
            if nextline.startswith(fenced):
                break
            result += escape(nextline[x:]) + "\n"
        if result:
            return [result + "</screen>\n"]
        return []
    if line.strip().startswith("~~~"):
        result = ""
        x = line.find("`")
        y = line.rfind("`")
        indent = line[x]
        fenced = line[:y + 1]
        for nextline in block.splitlines():
            if not result:  # first line
                y = nextline.rfind("`")
                info = nextline[y + 1:]
                if info:
                    result = "<screen info=\"%s\">" % escape(info)
                else:
                    result = "<screen>"
                continue
            if nextline.startswith(fenced):
                break
            result += escape(nextline[x:]) + "\n"
        if result:
            return [result + "</screen>\n"]
        return []
    if True:
        # thematic breaks allow a lot of space characters in GFM
        if re.match(" ? ? ?[*] *[*] *[*] *[* ]*$", line):
            return ["<hr />"]
        if re.match("^ ? ? ?[-] *[-] *[-] *[- ]*$", line):
            return ["<hr width=\"60%\" align=\"center\" />"]
        if re.match("^ ? ? ?[_] *[_] *[_] *[_ ]*$", line):
            return ["<hr width=\"80%\" align=\"center\" />"]
    #################################################
    blocks = []
    if re.match("\\[\w[-\w]*\\]:", line):
        text = ""
        remainder = ""
        for line in block.splitlines():
            if remainder:
                remainder += line + "\n"
                continue
            m = re.match("\\[(\w[-\w]*)]: +(\\S+) +(\\S.*)", line)
            if m:
                if m.group(2) in ["#"] and m.group(1) in ["date"]:
                    text += "<%s>%s</%s>" % (m.group(1), escape(m.group(3)), m.group(1))
                else:
                    text += "<meta name=\"%s\" href=\"%s\" content=\"%s\" />" % (
                        m.group(1), escape(m.group(2)), escape(m.group(3)))
                blocks += [text]
                continue
            m = re.match("\\[(\w[-\w]*)]: +(\\S+)", line)
            if m:
                text += "<meta name=\"%s\" href=\"%s\" content=\"%s\" />" % (m.group(1), escape(m.group(2)), m.group(1))
                blocks += [text]
                continue
            m = re.match("\\[(\w[-\w]*)]:", line)
            if m:
                text += "<a name=\"%s\" />" % (m.group(1))
                blocks += [text]
                continue
            remainder = line + "\n"
        block = remainder
        line = firstline(block)
    heading = re.match(" ? ? ?([#][#]*)(.*)", line)
    if heading:
        marks = heading.group(1)
        title = heading.group(2)
        subtitle = ""
        if marks in title:
            title, subtitle = title.split(marks, 1)
        result = ""
        end = ""
        for nextline in block.splitlines():
            if not result:  # first line
                result = "<sect%i>" % len(marks)
                end = "\n</sect%i>" % len(marks)
                result += "<title>%s</title>" % formatting(title.strip())
                if subtitle.strip():
                    end = "</subtitle>" + end
                    result += "\n<subtitle>" + formatting(subtitle.strip())
                continue
            if nextline.strip():
                if "<subtitle>" not in result:
                    end = "</subtitle>" + end
                    result += "\n<subtitle>"
                result += formatting(nextline) + "\n"
        blocks = [result + end]
        return blocks
    if re.match(" ? ? ?[*][*]* *(.*)", line):
        # decompose a tight block
        lines = list(block.splitlines())
        endblock = ""
        for n in range(len(lines)):
            line_0 = lines[n]
            line_1 = ""
            if n + 1 < len(lines): line_1 = lines[n + 1]
            _li0 = re.match(" ? ? ?([*][*]*) *(.*)", line_0)
            _li1 = re.match(" ? ? ?([*][*]*) *(.*)", line_1)
            if not endblock:
                if _li0 and (_li1 or not line_1.strip()):
                    blocks += ["<listitem>%s</listitem>" % formatting(_li0.group(2))]
                    continue
            else:
                if _li0:
                    blocks += ["<listitem><para>%s</para></listitem>" % formatting(endblock)]
                    endblock = ""
                if _li0 and (_li1 or not line_1.strip()):
                    blocks += ["<listitem>%s</listitem>" % formatting(_li0.group(2))]
                    continue
            if _li0:
                endblock += _li0.group(2) + "\n"
            else:
                endblock += line_0 + "\n"
        if endblock:
            blocks += ["<listitem><para>%s</para></listitem>" % formatting(endblock)]
        return blocks
    if re.match(" ? ? ?[-] *(.*)", line):
        blocks += ["<listitem><para>%s</para></listitem>" % formatting(block)]
        return blocks
    if block.strip():
        blocks += ["<para>%s</para>" % formatting(block)]
    return blocks

escaping = {"*": "ast", "[": "lbra", "]": "rbra", "(": "lpar", ")": "rpar", "\n<br />": "br"}
descaping = dict([(name, char) for char, name in escaping.items()])

def formatting(block: str) -> str:
    return descapes(inlines(escapes(block)))
def descapes(block: str) -> str:
    return re.sub("(&(\w+);)", lambda m: ((m.group(2) in descaping) and descaping[m.group(2)] or m.group(1)), block)
def keeping(block: str) -> str:
    return re.sub("(.)", lambda m: ((m.group(1) in escaping) and ("&%s;" % escaping[m.group(1)]) or m.group(1)), block)
def escapes(block: str) -> str:
    """ it does html escape plus remove backslash escapes """
    # the backslash will use escaping/descaping codes to help inline markup later
    text = ""
    esc = ""
    for c in block:
        if esc == "\\":
            if c == "\r":
                esc = "\r"
                continue
            if c == "\n":
                esc = ""
                text += "&br;"
                continue
            if c in escaping:
                text += "&%s;" % escaping[c]
            else:
                text += c
            esc = ""
            continue
        if esc == "\r":
            if c == "\n":
                esc = ""
                text += "&br;"
                continue
            esc = ""
            # fallthrough
        if c == "\\":
            esc = c
            continue
        if c == "`":
            text += "`"
            continue
        if c == "<":
            text += "&lt;"
            continue
        if c == ">":
            text += "&gt;"
            continue
        if c == "&":
            text += "&amp;"
            continue
        if c == "\"":
            text += "&quot;"
            continue
        text += c
    return text
def inlines(block: str) -> str:
    """ if some text is identfied the inline markdown formatting is applied."""
    text = block[:]
    text = re.sub("\\[([^\\[\\]<>]*)\\]\\(<([^\\[\\]<>()]*)>\\)",
                  lambda m: "<a href=\"%s\">%s</a>" % (keeping(m.group(2)), m.group(1)),
                  text)
    text = re.sub("\\[([^\\[\\]<>]*)\\]\\(([/#][^\\[\\]<>()]*)\\)",
                  lambda m: "<a href=\"%s\">%s</a>" % (keeping(m.group(2)), m.group(1)),
                  text)
    text = re.sub("\\[([^\\[\\]<>]*)\\]\\(([^\\[\\]<>()]*[./][^[\\]<>()]*)\\)",
                  lambda m: "<a href=\"%s\">%s</a>" % (keeping(m.group(2)), m.group(1)),
                  text)
    text = re.sub("\\[([^\\[\\]<>]*)\\]\\(([^\\[\\]<>()]*)\\)",
                  # lambda m: "<a link=\"%s\">%s</a>" % (keeping(m.group(2)), m.group(1)),
                  lambda m: "<a href=\"%s\">%s</a>" % (keeping(m.group(2)), m.group(1)),
                  text)
    text = re.sub("\\[(\\[[^\\[\\]<>]*\\])\\]\\(([^\\[\\]<>()]*)\\)",
                  # lambda m: "<a link=\"%s\">%s</a>" % (keeping(m.group(2)), m.group(1)),
                  lambda m: "<a href=\"%s\">%s</a>" % (keeping(m.group(2)), m.group(1)),
                  text)
    text = re.sub("([`]([^`<>]*)[`])",
                  lambda m: "<code>%s</code>" % keeping(m.group(2)),
                  text)
    text = re.sub("([*][*][*]([^*]*)[*][*][*])",
                  lambda m: "<strong><big>%s</big></strong>" % m.group(2),
                  text)
    text = re.sub("([_][_][_]([^_]*)[_][_][_])",
                  lambda m: "<strong><small>%s</small></strong>" % m.group(2),
                  text)
    text = re.sub("([*][*]([^*]*)[*][*])",
                  lambda m: "<strong>%s</strong>" % m.group(2),
                  text)
    text = re.sub("([_][_]([^_]*)[_][_])",
                  lambda m: "<em><small>%s</small></em>" % m.group(2),
                  text)
    if SingleAsterisk:
        text = re.sub("(?m)([*]([^*]*)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
    else:
        text = re.sub("(?m)([*](\".*\")[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
        text = re.sub("(?m)([*](&quot;.*&quot;)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
        text = re.sub("(?m)([*]([^ ]*)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
        text = re.sub("(?m)([*]([^ ]* [^ ]*)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
    if SingleUnderscore:
        text = re.sub("([_]([^_]*)[_])",
                      lambda m: "<em>%s</em>" % (escape(m.group(2))),
                      text)
    text = re.sub("([*][*][*](.*)[*][*][*])",
                  lambda m: "<strong><big>%s</big></strong>" % m.group(2),
                  text)
    text = re.sub("([_][_][_](.*)[_][_][_])",
                  lambda m: "<strong><small>%s</small></strong>" % m.group(2),
                  text)
    text = re.sub("([*][*](.*)[*][*])",
                  lambda m: "<strong>%s</strong>" % m.group(2),
                  text)
    text = re.sub("([_][_](.*)[_][_])",
                  lambda m: "<em><small>%s</small></em>" % m.group(2),
                  text)
    if SingleAsterisk:
        text = re.sub("([*](.*)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
    else:
        text = re.sub("(?m)([*](\"[^\"]*\")[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
        text = re.sub("(?m)([*](&quot;.*&quot;)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
        text = re.sub("(?m)([*]([^ ]*)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
        text = re.sub("(?m)([*]([^ ]* [^ ]*)[*])",
                      lambda m: "<em>%s</em>" % m.group(2),
                      text)
    if SingleUnderscore:
        text = re.sub("([_](.*)[_])",
                      lambda m: "<em>%s</em>" % (escape(m.group(2))),
                      text)
    return text

if __name__ == "__main__":
    from optparse import OptionParser
    _o = OptionParser("%prog [-options] filename...")
    _o.add_option("-v", "--verbose", action="count", default=0,
                  help="increase logging level")
    _o.add_option("-b", "--blocks", action="store_true", default=0,
                  help="show block structure")
    _o.add_option("-c", "--xmlblocks", action="store_true", default=0,
                  help="show xml block structure")
    _o.add_option("-r", "--htm", action="store_true", default=0,
                  help="returns as htm text")
    opt, args = _o.parse_args()
    logging.basicConfig(level=logging.ERROR - 10 * opt.verbose)
    document: List[str] = []
    for arg in args:
        logg.info(">> %s", arg)
        document += blocks(open(arg, "r").read())
    if opt.blocks:
        for block in document:
            show = "| " + block.replace("\n", "\n| ")
            if show.endswith("\n| "): show = show[:-2]
            if not show.endswith("\n"): show += "\n"
            print(show)
            if opt.verbose > 2:
                print("-----------")
    if opt.xmlblocks:
        for block in document:
            for part in _xmlblocks(block):
                show = "| " + part.replace("\n", "\n| ")
                if show.endswith("\n| "): show = show[:-2]
                if not show.endswith("\n"): show += "\n"
                print(show)
                if opt.verbose > 2:
                    print("-----------")
    if opt.htm:
        # this is usually used in zziplib to provide input to the old mksite.sh script.
        for block in document:
            if block in ["<listitem>", "</listitem>", "</listitem><listitem>"]:
                continue
            for part in _xmlblocks(block):
                if "<subtitle>" in part:
                    part = re.sub("(?s)</title>\\s*<subtitle>", "</title> <subtitle>", part)
                part = re.sub("<sect1><title>(.*)</title>", "<h1>\\1</h1>", part)
                part = re.sub("<sect2><title>(.*)</title>", "<h2>\\1</h2>", part)
                part = re.sub("<sect3><title>(.*)</title>", "<h3>\\1</h3>", part)
                part = re.sub("<sect4><title>(.*)</title>", "<h4>\\1</h4>", part)
                part = re.sub("<sect6><title>(.*)</title>", "<DT>\\1</DT>", part)
                part = part.replace("<para>", "<P>\n")
                part = part.replace("</para>", "</P>")
                part = part.replace("</sect1>", "")
                part = part.replace("</sect2>", "")
                part = part.replace("</sect3>", "")
                part = part.replace("</sect4>", "")
                part = part.replace("</sect6>", "")
                part = part.replace("<subtitle>", "")
                part = part.replace("</subtitle>", "")
                part = part.replace("<screen>", "<PRE>\n")
                part = part.replace("</screen>", "</PRE>")
                part = part.replace("<strong>", "<b>")
                part = part.replace("</strong>", "</b>")
                # part = part.replace("<code>", "`")
                # part = part.replace("</code>", "`")
                part = part.replace("<itemizedlist>", "<ul>\n")
                part = part.replace("</itemizedlist>", "</ul>")
                part = part.replace("<listitem>", "<li>")
                part = part.replace("</listitem>", "</li>")
                part = part.replace("&quot;", "\"")
                print(part + "\n")
    if not opt.htm and not opt.xmlblocks and not opt.blocks:
        # the docbook xml needs some enhancements.
        for block in document:
            for part in _xmlblocks(block):
                print(part)
