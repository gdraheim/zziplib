#! /usr/bin/python3

import re

from optparse import OptionParser
_o = OptionParser()
opt, args = _o.parse_args()

for arg in args:
   for line in open(arg):
       part = line.rstrip()
       part = re.sub("`([^`]*)`", "<code>\\1</code>", part)
       part = re.sub("(?m)(</[hH][1234]>) *(\S+)", "\\1\n\\2", part)
       # part = part.replace("<center>", "")
       # part = part.replace("</center>", "")
       # part = part.replace("<small>", "")
       # part = part.replace("</small>", "")
       part = part.replace("<section>", "")
       part = part.replace("</section>", "")
       #part = part.replace("<blockquote>", "<P>")
       #part = part.replace("</blockquote>", "</P>")
       #part = part.replace("<BLOCKQUOTE>", "<P>")
       #part = part.replace("</BLOCKQUOTE>", "</P>")
       part = part.replace("<BLOCKQUOTE>", "<blockquote>")
       part = part.replace("</BLOCKQUOTE>", "</blockquote>")
       part = part.replace("<PRE>", "<pre>")
       part = part.replace("</PRE>", "</pre>")
       part = part.replace("<tt>", "<code>")
       part = part.replace("</tt>", "</code>")
       part = re.sub("(</?)H([1234]>)", "\\1h\\2", part)
       part = part.replace("<p>&nbsp;</p>", "")
       part = part.replace("&nbsp;", "")
       part = part.replace("<blockquote><ul>", "<blockquote>\n<ul>")
       part = part.replace("</ul></blockquote>", "</ul>\n</blockquote>")
       part = part.replace("<P><small>", "<P>\n<small>")
       part = part.replace("</small></P>", "</small>\n</P>")
       part = part.replace("<ul><li>", "<ul>\n<li>")
       part = part.replace("</li></ul>", "</li>\n</ul>")
       print(part)
