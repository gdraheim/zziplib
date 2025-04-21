#! /usr/bin/python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements
# pylint: disable=too-many-branches,too-many-public-methods
# pylint: disable=wrong-import-position,ungrouped-imports,invalid-name
""" unit tests for zziplib/docs/zzipdoctool """

__copyright__ = "(C) 2021 Guido Draheim"
__contact__ = "https://github.com/gdraheim/zziplib"
__license__ = "CC0 Creative Commons Zero (Public Domain)"
__version__ = "0.13.79"

import sys
import os.path
import os
import logging
from unittest import TestCase, TestSuite, TextTestRunner
from fnmatch import fnmatchcase as matches

zzipdocdir = os.path.dirname(os.path.abspath(__file__))
sys.path = [zzipdocdir] + sys.path
from zzipdoctool import md2dbk  # noqa

logg = logging.getLogger("TOOLS")

class md2dbkTests(TestCase):
    def test_01000(self) -> None:
        b = md2dbk.blocks4("")
        self.assertEqual(b, [])
    def test_01001(self) -> None:
        b = md2dbk.blocks4("a")
        self.assertEqual(b, ["a\n"])
    def test_01002(self) -> None:
        b = md2dbk.blocks4("a\n")
        self.assertEqual(b, ["a\n"])
    def test_01003(self) -> None:
        b = md2dbk.blocks4("a\nb")
        self.assertEqual(b, ["a\nb\n"])
    def test_01004(self) -> None:
        b = md2dbk.blocks4("a\nb\n")
        self.assertEqual(b, ["a\nb\n"])
    def test_01005(self) -> None:
        b = md2dbk.blocks4("a\nb\n\nc")
        self.assertEqual(b, ["a\nb\n", "c\n"])
    def test_01006(self) -> None:
        b = md2dbk.blocks4("a\nb\n\nc\n")
        self.assertEqual(b, ["a\nb\n", "c\n"])
    def test_01007(self) -> None:
        b = md2dbk.blocks4("a\nb\n\n\nc")
        self.assertEqual(b, ["a\nb\n", "c\n"])
    def test_01008(self) -> None:
        b = md2dbk.blocks4("a\nb\n\n\nc\n")
        self.assertEqual(b, ["a\nb\n", "c\n"])
    def test_01009(self) -> None:
        b = md2dbk.blocks4("a\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a\nb\n", "c\n"])
    def test_01010(self) -> None:
        b = md2dbk.blocks4("a *xx*\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a *xx*\nb\n", "c\n"])
    def test_01011(self) -> None:
        b = md2dbk.blocks4("a **xx**\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a **xx**\nb\n", "c\n"])
    def test_01012(self) -> None:
        b = md2dbk.blocks4("a _xx_\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a _xx_\nb\n", "c\n"])
    def test_01013(self) -> None:
        b = md2dbk.blocks4("a __xx__\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a __xx__\nb\n", "c\n"])
    def test_01014(self) -> None:
        b = md2dbk.blocks4("a `xx`\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a `xx`\nb\n", "c\n"])
    def test_01015(self) -> None:
        b = md2dbk.blocks4("a ``xx``\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a ``xx``\nb\n", "c\n"])
    def test_01016(self) -> None:
        b = md2dbk.blocks4("a [xx]\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a [xx]\nb\n", "c\n"])
    def test_01017(self) -> None:
        b = md2dbk.blocks4("a [xx](foo)\nb\n\n\nc\n\n")
        self.assertEqual(b, ["a [xx](foo)\nb\n", "c\n"])
    def test_01101(self) -> None:
        b = md2dbk.blocks4("# a")
        self.assertEqual(b, ["# a\n"])
    def test_01102(self) -> None:
        b = md2dbk.blocks4("## a")
        self.assertEqual(b, ["## a\n"])
    def test_01103(self) -> None:
        b = md2dbk.blocks4("### a")
        self.assertEqual(b, ["### a\n"])
    def test_01104(self) -> None:
        b = md2dbk.blocks4("#### a")
        self.assertEqual(b, ["#### a\n"])
    def test_01105(self) -> None:
        b = md2dbk.blocks4("##### a")
        self.assertEqual(b, ["##### a\n"])
    def test_01106(self) -> None:
        b = md2dbk.blocks4("###### a")
        self.assertEqual(b, ["###### a\n"])
    def test_01111(self) -> None:
        b = md2dbk.blocks4("# a\n# b")
        self.assertEqual(b, ["# a\n# b\n"])
    def test_01112(self) -> None:
        b = md2dbk.blocks4("## a\n## b")
        self.assertEqual(b, ["## a\n## b\n"])
    def test_01113(self) -> None:
        b = md2dbk.blocks4("### a\n## b")
        self.assertEqual(b, ["### a\n## b\n"])
    def test_01114(self) -> None:
        b = md2dbk.blocks4("#### a\n## b")
        self.assertEqual(b, ["#### a\n## b\n"])
    def test_01115(self) -> None:
        b = md2dbk.blocks4("##### a\n## b")
        self.assertEqual(b, ["##### a\n## b\n"])
    def test_01116(self) -> None:
        b = md2dbk.blocks4("###### a\n## b")
        self.assertEqual(b, ["###### a\n## b\n"])
    def test_01121(self) -> None:
        b = md2dbk.blocks4("# a\n b")
        self.assertEqual(b, ["# a\n b\n"])
    def test_01122(self) -> None:
        b = md2dbk.blocks4("## a\n b")
        self.assertEqual(b, ["## a\n b\n"])
    def test_01123(self) -> None:
        b = md2dbk.blocks4("### a\n b")
        self.assertEqual(b, ["### a\n b\n"])
    def test_01124(self) -> None:
        b = md2dbk.blocks4("#### a\n b")
        self.assertEqual(b, ["#### a\n b\n"])
    def test_01125(self) -> None:
        b = md2dbk.blocks4("##### a\n b")
        self.assertEqual(b, ["##### a\n b\n"])
    def test_01126(self) -> None:
        b = md2dbk.blocks4("###### a\n b")
        self.assertEqual(b, ["###### a\n b\n"])
    def test_01131(self) -> None:
        b = md2dbk.blocks4("a\n===")
        self.assertEqual(b, ["# a\n"])
    def test_01132(self) -> None:
        b = md2dbk.blocks4("a\n---")
        self.assertEqual(b, ["## a\n"])
    def test_01133(self) -> None:
        b = md2dbk.blocks4("a\n===\nb")
        self.assertEqual(b, ["# a\nb\n"])
    def test_01134(self) -> None:
        b = md2dbk.blocks4("a\n---\nb")
        self.assertEqual(b, ["## a\nb\n"])
    def test_01135(self) -> None:
        b = md2dbk.blocks4("a\n===\n## b")
        self.assertEqual(b, ["# a\n## b\n"])
    def test_01136(self) -> None:
        b = md2dbk.blocks4("a\n---\n## b")
        self.assertEqual(b, ["## a\n## b\n"])
    def test_01141(self) -> None:
        b = md2dbk.blocks4("a\n===\n\n")
        self.assertEqual(b, ["# a\n"])
    def test_01142(self) -> None:
        b = md2dbk.blocks4("a\n---\n\n")
        self.assertEqual(b, ["## a\n"])
    def test_01143(self) -> None:
        b = md2dbk.blocks4("a\n===\n\n\nb")
        self.assertEqual(b, ["# a\n", "b\n"])
    def test_01144(self) -> None:
        b = md2dbk.blocks4("a\n---\n\n\nb")
        self.assertEqual(b, ["## a\n", "b\n"])
    def test_01145(self) -> None:
        b = md2dbk.blocks4("a\n===\n\n\n## b")
        self.assertEqual(b, ["# a\n", "## b\n"])
    def test_01146(self) -> None:
        b = md2dbk.blocks4("a\n---\n\n\n## b")
        self.assertEqual(b, ["## a\n", "## b\n"])
    def test_01151(self) -> None:
        b = md2dbk.blocks4("# a\n\n\nb")
        self.assertEqual(b, ["# a\n", "b\n"])
    def test_01152(self) -> None:
        b = md2dbk.blocks4("## a\n\nb")
        self.assertEqual(b, ["## a\n", "b\n"])
    def test_01153(self) -> None:
        b = md2dbk.blocks4("### a\n\n\n\nb")
        self.assertEqual(b, ["### a\n", "b\n"])
    def test_01154(self) -> None:
        b = md2dbk.blocks4("#### a\n\n\nb")
        self.assertEqual(b, ["#### a\n", "b\n"])
    def test_01155(self) -> None:
        b = md2dbk.blocks4("##### a\n\n\n## b")
        self.assertEqual(b, ["##### a\n", "## b\n"])
    def test_01156(self) -> None:
        b = md2dbk.blocks4("###### a\n\n\n## b")
        self.assertEqual(b, ["###### a\n", "## b\n"])
    def test_01201(self) -> None:
        b = md2dbk.blocks4("* a\n\n\n")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "</listitem>", "</itemizedlist>"])
    def test_01202(self) -> None:
        b = md2dbk.blocks4("* a\n\n\nb")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "</listitem>", "</itemizedlist>",
                             "b\n"])
    def test_01203(self) -> None:
        b = md2dbk.blocks4("* a\n\n\nb\n* c")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "</listitem>", "</itemizedlist>", "b\n",
                             "<itemizedlist>", "<listitem>", "* c\n",
                             "</listitem>", "</itemizedlist>"])
    def test_01211(self) -> None:
        b = md2dbk.blocks4("* a\n* x\n\n")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "</listitem><listitem>", "* x\n",
                             "</listitem>", "</itemizedlist>"])
    def test_01212(self) -> None:
        b = md2dbk.blocks4("* a\n* x\n\nb")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "</listitem><listitem>", "* x\n",
                             "</listitem>", "</itemizedlist>", "b\n"])
    def test_01213(self) -> None:
        b = md2dbk.blocks4("* a\n* x\n\nb\n* c")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "</listitem><listitem>", "* x\n",
                             "</listitem>", "</itemizedlist>", "b\n",
                             "<itemizedlist>", "<listitem>", "* c\n",
                             "</listitem>", "</itemizedlist>"])
    def test_01221(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n\n")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "</listitem>", "</itemizedlist>",
                             "</listitem>", "</itemizedlist>"])
    def test_01222(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n\nb")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "</listitem>", "</itemizedlist>",
                             "</listitem>", "</itemizedlist>", "b\n"])
    def test_01223(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n\nb\n* c")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "</listitem>", "</itemizedlist>",
                             "</listitem>", "</itemizedlist>", "b\n",
                             "<itemizedlist>", "<listitem>", "* c\n",
                             "</listitem>", "</itemizedlist>"])
    def test_01224(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n*** y\nb\n* c")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "<itemizedlist>", "<listitem>", "*** y\n",
                             "</listitem>", "</itemizedlist>",
                             "</listitem>", "</itemizedlist>",
                             "</listitem>", "</itemizedlist>", "b\n",
                             "<itemizedlist>", "<listitem>", "* c\n",
                             "</listitem>", "</itemizedlist>"])
    def test_01225(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n** y\nb\n* c")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "</listitem><listitem>", "** y\n",
                             "</listitem>", "</itemizedlist>",
                             "</listitem>", "</itemizedlist>", "b\n",
                             "<itemizedlist>", "<listitem>", "* c\n",
                             "</listitem>", "</itemizedlist>"])
    def test_01226(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n* y\n\nb")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "</listitem>", "</itemizedlist>", "<listitem>", "* y\n",
                             "</listitem>", "</itemizedlist>", "b\n"])
    def test_01227(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n* y\n* z\n\nb")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "</listitem>", "</itemizedlist>",
                             "<listitem>", "* y\n",
                             "</listitem><listitem>", "* z\n",
                             "</listitem>", "</itemizedlist>", "b\n"])
    def test_01228(self) -> None:
        b = md2dbk.blocks4("* a\n** x\n* y\n** z\n\nb")
        self.assertEqual(b, ["<itemizedlist>", "<listitem>", "* a\n",
                             "<itemizedlist>", "<listitem>", "** x\n",
                             "</listitem>", "</itemizedlist>", "<listitem>", "* y\n",
                             "<itemizedlist>", "<listitem>", "** z\n",
                             "</listitem>", "</itemizedlist>",
                             "</listitem>", "</itemizedlist>", "b\n"])
    def test_02000(self) -> None:
        b = md2dbk.blocks4("")
        self.assertEqual(b, [])
    def test_02001(self) -> None:
        b = md2dbk.blocks4("> a")
        self.assertEqual(b, ["<blockquote>", "a\n", "</blockquote>"])
    def test_02002(self) -> None:
        b = md2dbk.blocks4("> a\n")
        self.assertEqual(b, ["<blockquote>", "a\n", "</blockquote>"])
    def test_02003(self) -> None:
        b = md2dbk.blocks4("> a\n> b")
        self.assertEqual(b, ["<blockquote>", "a\nb\n", "</blockquote>"])
    def test_02004(self) -> None:
        b = md2dbk.blocks4("> a\n> b\n")
        self.assertEqual(b, ["<blockquote>", "a\nb\n", "</blockquote>"])
    def test_02005(self) -> None:
        b = md2dbk.blocks4("> a\n> b\n\n> c")
        self.assertEqual(b, ["<blockquote>", "a\nb\n", "</blockquote>",
                             "<blockquote>", "c\n", "</blockquote>"])
    def test_02006(self) -> None:
        b = md2dbk.blocks4("> a\n> b\n\n> c\n")
        self.assertEqual(b, ["<blockquote>", "a\nb\n", "</blockquote>",
                             "<blockquote>", "c\n", "</blockquote>"])
    def test_02007(self) -> None:
        b = md2dbk.blocks4("> a\n> b\n\n\n> c")
        self.assertEqual(b, ["<blockquote>", "a\nb\n", "</blockquote>",
                             "<blockquote>", "c\n", "</blockquote>"])
    def test_02008(self) -> None:
        b = md2dbk.blocks4("> a\n> b\n\n\n> c\n")
        self.assertEqual(b, ["<blockquote>", "a\nb\n", "</blockquote>",
                             "<blockquote>", "c\n", "</blockquote>"])
    def test_02009(self) -> None:
        b = md2dbk.blocks4("> a\n> b\n\n\n> c\n\n")
        self.assertEqual(b, ["<blockquote>", "a\nb\n", "</blockquote>",
                             "<blockquote>", "c\n", "</blockquote>"])
    def test_02101(self) -> None:
        b = md2dbk.blocks4("> # a")
        self.assertEqual(b, ["<blockquote>", "# a\n", "</blockquote>"])
    def test_02102(self) -> None:
        b = md2dbk.blocks4("> ## a")
        self.assertEqual(b, ["<blockquote>", "## a\n", "</blockquote>"])
    def test_02111(self) -> None:
        b = md2dbk.blocks4("> # a\n> # b")
        self.assertEqual(b, ["<blockquote>", "# a\n# b\n", "</blockquote>"])
    def test_02112(self) -> None:
        b = md2dbk.blocks4("> ## a\n> ## b")
        self.assertEqual(b, ["<blockquote>", "## a\n## b\n", "</blockquote>"])
    def test_02131(self) -> None:
        b = md2dbk.blocks4("> a\n> ===")
        self.assertEqual(b, ["<blockquote>", "# a\n", "</blockquote>"])
    def test_02132(self) -> None:
        b = md2dbk.blocks4("> a\n> ---")
        self.assertEqual(b, ["<blockquote>", "## a\n", "</blockquote>"])
    def test_02151(self) -> None:
        b = md2dbk.blocks4("> # a\n>\n>\n> b")
        self.assertEqual(b, ["<blockquote>", "# a\n", "b\n", "</blockquote>"])
    def test_02152(self) -> None:
        b = md2dbk.blocks4("> ## a\n>\n> b")
        self.assertEqual(b, ["<blockquote>", "## a\n", "b\n", "</blockquote>"])
    def test_02153(self) -> None:
        b = md2dbk.blocks4("> ### a\n>\n>\n>\n> b")
        self.assertEqual(b, ["<blockquote>", "### a\n", "b\n", "</blockquote>"])
    def test_02154(self) -> None:
        b = md2dbk.blocks4("> #### a\n>\n>\n> b")
        self.assertEqual(b, ["<blockquote>", "#### a\n", "b\n", "</blockquote>"])
    def test_02155(self) -> None:
        b = md2dbk.blocks4("> ##### a\n>\n>\n> ## b")
        self.assertEqual(b, ["<blockquote>", "##### a\n", "## b\n", "</blockquote>"])
    def test_02156(self) -> None:
        b = md2dbk.blocks4("> ###### a\n>\n>\n> ## b")
        self.assertEqual(b, ["<blockquote>", "###### a\n", "## b\n", "</blockquote>"])

def main() -> int:
    import optparse # pylint: disable=deprecated-module,import-outside-toplevel
    cmdline = optparse.OptionParser("%prog [options] test_xxx", epilog=__doc__)
    cmdline.add_option("-v", "--verbose", action="count", default=0, help="more logging")
    cmdline.add_option("-^", "--quiet", action="count", default=0, help="less logging")
    cmdline.add_option("-?", "--version", action="count", default=0, help="author info")
    cmdline.add_option("--failfast", action="store_true", default=False,
                       help="Stop the test run on the first error or failure. [%default]")
    cmdline.add_option("--xmlresults", metavar="FILE", default=None,
                       help="capture results as a junit xml file [%default]")
    opt, args = cmdline.parse_args()
    logging.basicConfig(level=logging.WARNING - 10 * opt.verbose + 10 * opt.quiet)
    if opt.version:
        print("version:", __version__)
        print("contact:", __contact__)
        print("license:", __license__)
        print("authors:", __copyright__)
        return os.EX_OK
    #
    if not args: args += ["test_"]
    suite = TestSuite()
    for arg in args:
        for classname in sorted(list(globals())):
            if not classname.endswith("Tests"):
                continue
            testclass = globals()[classname]
            for method in sorted(dir(testclass)):
                if arg.endswith("/"):
                    arg = arg[:-1]
                if "*" not in arg:
                    arg += "*"
                if len(arg) > 2 and arg[1] == "_":
                    arg = "test_" + arg[2:]
                if matches(method, arg):
                    suite.addTest(testclass(method))
    xmlresults = opt.xmlresults
    if xmlresults:
        try:
            import xmlrunner  # type: ignore[import] # pylint: disable=import-error,import-outside-toplevel
        except ImportError:
            xmlresults = None
    if xmlresults:
        if os.path.exists(opt.xmlresults):
            os.remove(opt.xmlresults)
        logg.info("xml results into %s", opt.xmlresults)
        Runner = xmlrunner.XMLTestRunner
        result = Runner(output=opt.xmlresults).run(suite)
    else:
        Runner = TextTestRunner
        result = Runner(verbosity=opt.verbose, failfast=opt.failfast).run(suite)
    if not result.wasSuccessful():
        return os.EX_DATAERR
    return os.EX_OK

if __name__ == "__main__":
    sys.exit(main())
