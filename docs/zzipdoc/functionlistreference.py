#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function

from zzipdoc.htm2dbk import html2docbook


def _sane(text):
    return (html2docbook(text)
            .replace("<link>", "<function>")
            .replace("</link>", "</function>")
            .replace("<fu:protospec>", "<funcprototype>")
            .replace("</fu:protospec>", "</funcprototype>")
            .replace("<fu:prespec>", "<funcdef>")
            .replace("</fu:prespec>", "")
            .replace("<fu:namespec>", "")
            .replace("</fu:namespec>", "</funcdef>")
            .replace("</fu:callspec>", "</paramdef>")
            .replace("<fu:callspec>", "<paramdef>"))


class FunctionListReference(object):
    """ Creating a docbook-style <reference> list of <refentry> parts
    that will each be translated into a unix manual page in a second step """

    def __init__(self, version, package):
        self.version = version
        self.package = package
        self.pages = []
        self.entry = None

    def cut(self):
        if not self.entry:
            return
        self.pages.append(self.entry)
        self.entry = None

    def add(self, entry):
        name = entry.name
        description = entry.body.xml_text(name)
        funcsynopsis = str(entry.head)
        if not funcsynopsis:
            print("no funcsynopsis for", name)
            return
        if self.entry is None:
            self.entry = FunctionListRefEntry(entry, self.version, self.package)
            self.entry.funcsynopsisinfo = entry.mainheader
            self.entry.refpurpose = entry.title
            self.entry.refentrytitle = entry.name
            # self.entry.refname = entry.name
        self.entry.funcsynopsis_list += [funcsynopsis]
        self.entry.description_list += [description]
        self.entry.refname_list += [name]
        for item in entry.list_seealso:
            if item not in self.entry.seealso_list:
                assert item
                self.entry.seealso_list += [item]

    @property
    def title(self):
        return self.package + " Function List"

    def __str__(self):
        T = "<reference><title>" + self.title + "</title>\n"
        for item in self.pages:
            text = item.refentry_text()
            if not text:
                print("OOPS, no text for", item.name)
                continue
            T += _sane(text)
        T += "</reference>\n"
        return T


class FunctionListRefEntry(object):
    def __init__(self, func, version, package):
        """ initialize the fields needed for a man page entry - the fields are
           named after the docbook-markup that encloses (!!) the text we store
           the entries like X.refhint = "hello" will be printed therefore as
           <refhint>hello</refhint>. Names with underscores are only used as
           temporaries but they are memorized, perhaps for later usage. """
        self.name = func.name
        self.refhint = "\n<!--========= " + self.name + " (3) ============-->\n"
        self.refentry_date = version.strip()  # ! //refentryinfo/date
        self.refentry_productname = package.strip()  # ! //refentryinfo/prod*
        self.manvolnum = "3"  # //refmeta/manvolnum
        self.refentrytitle = None  # //refmeta/refentrytitle
        self.refpurpose = None  # //refnamediv/refpurpose
        self.refname_list = []
        self.mainheader = func.mainheader
        self.includes = func.includes
        self.funcsynopsisinfo = ""  # //funcsynopsisdiv/funcsynopsisinfo
        self.funcsynopsis_list = []
        self.description_list = []
        # optional sections
        self.authors_list = []  # //sect1[authors]/listitem
        self.seealso_list = []
        for item in func.list_seealso:
            assert item
            self.seealso_list += [item]
        self.file_authors = None
        if func.authors:
            self.file_authors = func.authors
            assert self.file_authors
            self.authors_list += [self.file_authors]
        self.file_copyright = ""
        if func.copyright:
            self.file_copyright = func.copyright
            assert self.file_copyright

    @property
    def refentryinfo_text(self):
        """ the manvol formatter wants to render a footer line and header line
            on each manpage and such info is set in <refentryinfo> """
        if self.refentry_date and self.refentry_productname:
            return (
                    "\n <date>" + self.refentry_date + "</date>" +
                    "\n <productname>" + self.refentry_productname + "</productname>")
        return ""

    @property
    def refmeta_text(self):
        """ the manvol formatter needs to know the filename of the manpage to
            be made up and these parts are set in <refmeta> actually """
        if self.manvolnum and self.refentrytitle:
            return (
                    "\n <refentrytitle>" + self.refentrytitle + "</refentrytitle>" +
                    "\n <manvolnum>" + self.manvolnum + "</manvolnum>")
        if self.manvolnum and self.name:
            return (
                    "\n <refentrytitle>" + self.name + "</refentrytitle>" +
                    "\n <manvolnum>" + self.manvolnum + "</manvolnum>")
        return ""

    @property
    def refnamediv_text(self):
        """ the manvol formatter prints a header line with a <refpurpose> line
            and <refname>'d functions that are described later. For each of
            the <refname>s listed here, a mangpage is generated, and for each
            of the <refname>!=<refentrytitle> then a symlink is created """
        if self.refpurpose and self.refname_list:
            T = ""
            for refname in self.refname_list:
                T += "\n <refname>" + refname + '</refname>'
            T += "\n <refpurpose>" + self.refpurpose + " </refpurpose>"
            return T
        return ""

    @property
    def funcsynopsisdiv_text(self):
        """ refsynopsisdiv shall be between the manvol mangemaent information
            and the reference page description blocks """
        T = ""
        if self.funcsynopsis_list:
            T += "\n<funcsynopsis>"
            if self.funcsynopsisinfo:
                T += "\n<funcsynopsisinfo>" + self.funcsynopsisinfo + \
                     "\n</funcsynopsisinfo>\n"
            for funcsynopsis in self.funcsynopsis_list:
                T += funcsynopsis
            T += "\n</funcsynopsis>\n"
        return T

    @property
    def description_text(self):
        """ the description section on a manpage is the main part. Here
            it is generated from the per-function comment area. """
        return "".join(self.description_list).strip()\
               or "<para>(missing description)</para>"

    @property
    def authors_text(self):
        """ part of the footer sections on a manpage and a description of
            original authors. We prever an itimizedlist to let the manvol
            show a nice vertical aligment of authors of this ref item """
        if self.authors_list:
            return "<itemizedlist>"\
                + ''.join("\n <listitem><para>" + author + "</para></listitem>"
                          for author in sorted(set(self.authors_list)))\
                + "</itemizedlist>"
        return ""

    @property
    def seealso_text(self):
        """ the last section on a manpage is called 'SEE ALSO' usually and
            contains a comma-separated list of references. Some manpage
            viewers can parse these and convert them into hyperlinks """
        return ', '.join(self.seealso_list)

    def refentry_text(self, id=None):
        """ combine fields into a proper docbook refentry """
        if id:
            T = '<refentry id="' + id + '">'
        else:
            T = '<refentry>'  # this is an error

        if self.refentryinfo_text:
            T += "\n<refentryinfo>" + self.refentryinfo_text + \
                 "\n</refentryinfo>\n"
        if self.refmeta_text:
            T += "\n<refmeta>" + self.refmeta_text + \
                 "\n</refmeta>\n"
        if self.refnamediv_text:
            T += "\n<refnamediv>" + self.refnamediv_text + \
                 "\n</refnamediv>\n"
        if self.funcsynopsisdiv_text:
            T += "\n<refsynopsisdiv>\n" + self.funcsynopsisdiv_text + \
                 "\n</refsynopsisdiv>\n"
        if self.description_text:
            T += "\n<refsect1><title>Description</title> " + \
                 self.description_text + "\n</refsect1>"
        if self.authors_text:
            T += "\n<refsect1><title>Author</title> " + \
                 self.authors_text + "\n</refsect1>"
        if self.file_copyright:
            T += "\n<refsect1><title>Copyright</title> " + \
                 self.file_copyright + "\n</refsect1>\n"
        if self.seealso_text:
            T += "\n<refsect1><title>See Also</title><para> " + \
                 self.seealso_text + "\n</para></refsect1>\n"

        T += "\n</refentry>\n"
        return T
