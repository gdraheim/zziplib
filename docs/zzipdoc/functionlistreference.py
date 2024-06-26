#! /usr/bin/env python3

from __future__ import print_function
from typing import Optional, List
from zzipdoc.match import Match
from zzipdoc.htm2dbk import *
from zzipdoc.options import DocOptions
from zzipdoc.functionprototype import FunctionPrototype
from zzipdoc.htmldoctypes import RefDocPart

class FunctionListReference:
    """ Creating a docbook-style <reference> list of <refentry> parts
    that will each be translated into a unix manual page in a second step """
    o: DocOptions
    pages: List["FunctionListRefEntry"]
    entry: Optional["FunctionListRefEntry"]
    def __init__(self, o: Optional[DocOptions] = None) -> None:
        self.o = o if o else DocOptions()
        self.pages = []
        self.entry = None
    def cut(self) -> None:
        if not self.entry: return
        self.pages += [ self.entry ]
        self.entry = None
    def add(self, entry: RefDocPart) -> None:
        refname = entry.get_name()
        description = entry.body_xml_text(refname)
        funcsynopsis = entry.head_xml_text()
        if not funcsynopsis:
            print("no funcsynopsis for " + (refname or "?"))
            return
        if self.entry is None:
            self.entry = FunctionListRefEntry(entry, self.o)
            self.entry.funcsynopsisinfo = entry.get_mainheader()
            self.entry.refpurpose = entry.get_title()
            self.entry.refentrytitle = entry.get_name()
            # self.entry.refname = entry.get_name()
        if funcsynopsis:
            self.entry.funcsynopsis_list += [ funcsynopsis ]
        if description:
            self.entry.description_list += [ description ]
        if refname:
            self.entry.refname_list += [ refname ]
        if entry.list_seealso():
            for item in entry.list_seealso():
                if item not in self.entry.seealso_list:
                    self.entry.seealso_list += [ item ]
    def get_title(self) -> str:
        return self.o.package+" Function List"
    def xml_text(self) -> str:
        T = "<reference><title>"+self.get_title()+"</title>\n"
        for item in self.pages:
            text = item.refentry_text()
            if not text: "OOPS, no text for", item.name ; continue
            T += self.sane(text)
        T += "</reference>\n"
        return T
    def sane(self, text: str) -> str:
        return (html2docbook(text)
                .replace("<link>","<function>")
                .replace("</link>","</function>")
                .replace("<fu:protospec>","<funcprototype>")
                .replace("</fu:protospec>","</funcprototype>")
                .replace("<fu:prespec>","<funcdef>")
                .replace("</fu:prespec>","")
                .replace("<fu:namespec>","")
                .replace("</fu:namespec>","</funcdef>")
                .replace("</fu:callspec>","</paramdef>")
                .replace("<fu:callspec>","<paramdef>")) 

    
class FunctionListRefEntry:
    refhint: Optional[str]
    refentry: Optional[str]
    refentry_date: Optional[str]
    refentry_productname: Optional[str]
    refentry_title: Optional[str]
    refentryinfo: Optional[str]
    manvolnum: str
    refentrytitle: Optional[str]
    refmeta: Optional[str]
    refpurpose: Optional[str]
    refname: Optional[str]
    refname_list: List[str]
    refnamediv: Optional[str]
    mainheader: Optional[str]
    includes: Optional[str]
    funcsynopsisinfo: Optional[str]
    funcsynopsis: Optional[str]
    funcsynopsis_list: List[str]
    description: Optional[str]
    description_list: List[str]
    seealso: Optional[str]
    seealso_list: List[str]
    authors: Optional[str]
    authors_list: List[str]
    copyright: Optional[str]
    copyright_list: List[str]
    def __init__(self, func: RefDocPart, o: DocOptions) -> None:
        """ initialize the fields needed for a man page entry - the fields are
           named after the docbook-markup that encloses (!!) the text we store
           the entries like X.refhint = "hello" will be printed therefore as
           <refhint>hello</refhint>. Names with underscores are only used as
           temporaries but they are memorized, perhaps for later usage. """
        self.name = func.get_name() or "_"
        self.refhint = "\n<!--========= "+self.name+" (3) ============-->\n"
        self.refentry = None
        self.refentry_date = o.version.strip()        #! //refentryinfo/date
        self.refentry_productname = o.package.strip() #! //refentryinfo/prod*
        self.refentry_title = None                    #! //refentryinfo/title
        self.refentryinfo = None                      #! override
        self.manvolnum = "3"                         # //refmeta/manvolnum
        self.refentrytitle = None                    # //refmeta/refentrytitle
        self.refmeta = None                          # override
        self.refpurpose = None                       # //refnamediv/refpurpose
        self.refname = None                          # //refnamediv/refname
        self.refname_list = []
        self.refnamediv = None                       # override
        self.mainheader = func.get_mainheader()
        self.includes = func.get_includes()
        self.funcsynopsisinfo = ""       # //funcsynopsisdiv/funcsynopsisinfo
        self.funcsynopsis = None         # //funcsynopsisdiv/funcsynopsis
        self.funcsynopsis_list = []
        self.description = None
        self.description_list = []
        # optional sections
        self.authors_list = []           # //sect1[authors]/listitem
        self.authors = None              # override
        self.copyright = None
        self.copyright_list = []
        self.seealso = None
        self.seealso_list = []
        if  func.list_seealso():
            for item in func.list_seealso():
                self.seealso_list += [ item ]
        self.file_authors = None
        authors = func.get_authors()
        if authors:
            self.file_authors = authors
            self.authors_list += [ self.file_authors ]
        self.file_copyright = None
        copyright = func.get_copyright()
        if copyright:
            self.file_copyright = copyright
            self.copyright_list += [ self.file_copyright ]
    #fu
    def refentryinfo_text(self) -> str:
        """ the manvol formatter wants to render a footer line and header line
            on each manpage and such info is set in <refentryinfo> """
        if self.refentryinfo:
            return self.refentryinfo
        if self.refentry_date and \
           self.refentry_productname and \
           self.refentry_title: return (
            "\n <date>"+self.refentry_date+"</date>"+ 
            "\n <productname>"+self.refentry_productname+"</productname>"+
            "\n <title>"+self.refentry_title+"</title>")
        if self.refentry_date and \
           self.refentry_productname: return (
            "\n <date>"+self.refentry_date+"</date>"+ 
            "\n <productname>"+self.refentry_productname+"</productname>")
        return ""
    def refmeta_text(self) -> str:
        """ the manvol formatter needs to know the filename of the manpage to
            be made up and these parts are set in <refmeta> actually """
        if self.refmeta:
            return self.refmeta
        if self.manvolnum and self.refentrytitle:
            return (
                "\n <refentrytitle>"+self.refentrytitle+"</refentrytitle>"+
                "\n <manvolnum>"+self.manvolnum+"</manvolnum>")
        if self.manvolnum and self.name:
            return (
                "\n <refentrytitle>"+self.name+"</refentrytitle>"+
                "\n <manvolnum>"+self.manvolnum+"</manvolnum>")
        return ""
    def refnamediv_text(self) -> str:
        """ the manvol formatter prints a header line with a <refpurpose> line
            and <refname>'d functions that are described later. For each of
            the <refname>s listed here, a mangpage is generated, and for each
            of the <refname>!=<refentrytitle> then a symlink is created """
        if self.refnamediv:
            return self.refnamediv
        if self.refpurpose and self.refname:
            return ("\n <refname>"+self.refname+'</refname>'+
                    "\n <refpurpose>"+self.refpurpose+" </refpurpose>")
        if self.refpurpose and self.refname_list:
            T = ""
            for refname in self.refname_list:
                T += "\n <refname>"+refname+'</refname>'
            T += "\n <refpurpose>"+self.refpurpose+" </refpurpose>"
            return T
        return ""
    def funcsynopsisdiv_text(self) -> str:
        """ refsynopsisdiv shall be between the manvol mangemaent information
            and the reference page description blocks """
        T=""
        if self.funcsynopsis:
            T += "\n<funcsynopsis>"
            if self.funcsynopsisinfo:
                T += "\n<funcsynopsisinfo>"+    self.funcsynopsisinfo + \
                     "\n</funcsynopsisinfo>\n"
            T += self.funcsynopsis + \
                 "\n</funcsynopsis>\n"
        if self.funcsynopsis_list:
            T += "\n<funcsynopsis>"
            if self.funcsynopsisinfo:
                T += "\n<funcsynopsisinfo>"+    self.funcsynopsisinfo + \
                     "\n</funcsynopsisinfo>\n"
            for funcsynopsis in self.funcsynopsis_list:
                T += funcsynopsis
            T += "\n</funcsynopsis>\n"
        #fi
        return T
    def description_text(self) -> str:
        """ the description section on a manpage is the main part. Here
            it is generated from the per-function comment area. """
        if self.description:
            return self.description
        if self.description_list:
            T = ""
            for description in self.description_list:
                if not description: continue
                T += description
            if T.strip() != "": return T
        return "<para>(missing description)</para>"
    def authors_text(self) -> str:
        """ part of the footer sections on a manpage and a description of
            original authors. We prever an itimizedlist to let the manvol
            show a nice vertical aligment of authors of this ref item """
        if self.authors:
            return self.authors
        if self.authors_list:
            T = "<itemizedlist>"
            previous=""
            for authors in self.authors_list:
                if not authors: continue
                if previous == authors: continue
                T += "\n <listitem><para>"+authors+"</para></listitem>"
                previous = authors
            T += "</itemizedlist>"
            return T
        if self.authors:
            return self.authors
        return ""
    def copyright_text(self) -> str:
        """ the copyright section is almost last on a manpage and purely
            optional. We list the part of the per-file copyright info """
        if self.copyright:
            return self.copyright
        """ we only return the first valid instead of merging them """
        if self.copyright_list:
            T = ""
            for copyright in self.copyright_list:
                if copyright:
                    return copyright # !!!
        return ""
    def seealso_text(self) -> str:
        """ the last section on a manpage is called 'SEE ALSO' usually and
            contains a comma-separated list of references. Some manpage
            viewers can parse these and convert them into hyperlinks """
        if self.seealso:
            return self.seealso
        if self.seealso_list:
            T = ""
            for seealso in self.seealso_list:
                if not seealso: continue
                if T: T += ", "
                T += seealso
            if T: return T
        return ""
    def refentry_text(self, ref: Optional[str]=None) -> str:
        """ combine fields into a proper docbook refentry """
        if ref is None:
            ref = self.refentry
        if ref:
            T = '<refentry id="'+ref+'">'
        else:
            T = '<refentry>' # this is an error
           
        if self.refentryinfo_text():
            T += "\n<refentryinfo>"+       self.refentryinfo_text()+ \
                 "\n</refentryinfo>\n"
        if self.refmeta_text():
            T += "\n<refmeta>"+            self.refmeta_text() + \
                 "\n</refmeta>\n" 
        if self.refnamediv_text():
            T += "\n<refnamediv>"+         self.refnamediv_text() + \
                 "\n</refnamediv>\n"
        if self.funcsynopsisdiv_text():     
            T += "\n<refsynopsisdiv>\n"+   self.funcsynopsisdiv_text()+ \
                 "\n</refsynopsisdiv>\n"
        if self.description_text():
            T += "\n<refsect1><title>Description</title> " + \
                 self.description_text() + "\n</refsect1>"
        if self.authors_text():
            T += "\n<refsect1><title>Author</title> " + \
                 self.authors_text() + "\n</refsect1>"
        if self.copyright_text():
            T += "\n<refsect1><title>Copyright</title> " + \
                 self.copyright_text() + "\n</refsect1>\n"
        if self.seealso_text():
            T += "\n<refsect1><title>See Also</title><para> " + \
                 self.seealso_text() + "\n</para></refsect1>\n"

        T +=  "\n</refentry>\n"
        return T
    #fu
#end
