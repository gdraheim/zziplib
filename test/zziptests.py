import unittest
import subprocess
import logging
import os
import collections
import shutil
import random
import re
from fnmatch import fnmatchcase as matches
from cStringIO import StringIO

logg = logging.getLogger("test")

topsrcdir = "../.."
testdatadir = "testdata.d"
readme = "README"
mkzip = "zip"
unzip = "unzip"
exeext = ""

def shell_string(command):
   return " ".join(["'%s'" % arg.replace("'","\\'") for arg in command])

def shell(command, shell=True, calls=False, cwd=None, env=None, lang=None, returncodes=None):
    returncodes = returncodes or [ None, 0 ]
    Shell = collections.namedtuple("Shell",["returncode", "output", "errors", "shell"])
    if isinstance(command, basestring):
       sh_command = command
       command = [ command ]
    else:
       sh_command = shell_string(command)
    if lang:
        if not env: env = os.environ.copy()
        for name, value in env.items():
            if name.startswith("LC_"):
                env[name] = lang
        env["LANG"] = lang # defines message format
        env["LC_ALL"] = lang # other locale formats
    try:
        output, errors = "", ""
        if calls:
            logg.debug("result from %s: %s", cwd and cwd+"/" or "shell", sh_command)
            run = subprocess.Popen(command, shell=shell, cwd=cwd, env=env)
            if run.returncode:
                logg.warning("EXIT %s: %s", run.returncode, command)
            run.wait()
        else:
            logg.debug("output from %s: %s", cwd and cwd+"/" or "shell", sh_command)
            run = subprocess.Popen(command, shell=shell, cwd=cwd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=None, env=env)
            if run.returncode:
                logg.warning("EXIT %s: %s", run.returncode, command)
            output, errors = run.communicate() # run.wait()
    except:
        logg.error("*E*: %s", sh_command)
        for line in output.split("\n"):
            if line:
                logg.error("OUT: %s", line)
        for line in errors.split("\n"):
            if line:
                logg.error("ERR: %s", line)
        raise
    if run.returncode not in returncodes:
        logg.warning("*%02i: %s", run.returncode, sh_command)
        for line in output.split("\n"):
            if line:
                logg.warning("OUT: %s", line)
        for line in errors.split("\n"):
            if line:
                logg.warning("ERR: %s", line)
        raise subprocess.CalledProcessError(run.returncode, sh_command, output)
    else:
        for line in output.split("\n"):
            if line:
                logg.debug("OUT: %s", line)
        for line in errors.split("\n"):
            if line:
                logg.debug("ERR: %s", line)
    return Shell(run.returncode, output, errors, sh_command)

def testdir(testname):
    newdir = "tests/tmp."+testname
    if os.path.isdir(newdir):
        shutil.rmtree(newdir)
    os.makedirs(newdir)
    return newdir

def download(base_url, filename, into):
    if not os.path.isdir(into):
        os.makedirs(into)
    if not os.path.exists(os.path.join(into, filename)):
        shell("cd {into} && wget {base_url}/{filename}".format(**locals()))
def trycopy(srcdir, filename, into):
    if not os.path.isdir(into):
        os.makedirs(into)
    src_file = os.path.join(srcdir, filename)
    dst_file = os.path.join(into, filename)
    if os.path.isfile(src_file):
        shutil.copy(src_file, dst_file)

def output(cmd, shell=True):
    run = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE)
    out, err = run.communicate()
    return out
def grep(pattern, lines):
    if isinstance(lines, basestring):
        lines = lines.split("\n")
    for line in lines:
       if re.search(pattern, line.rstrip()):
           yield line.rstrip()
def greps(lines, pattern):
    return list(grep(pattern, lines))


class ZZipTest(unittest.TestCase):
  @property
  def t(self):
    if not os.path.isdir(testdatadir):
       os.makedirs(testdatadir)
    return testdatdir
  @property
  def s(self):
    return topsrcdir
  def src(self, name):
    return os.path.join(self.s, name)
  def readme(self):
     f = open(self.src(readme))
     text = f.read()
     f.close()
     return text
  def mkfile(self, name, content):
    b = os.path.dirname(name)
    if not os.path.isdir(b):
       os.makedirs(b)
    f = open(name, "w")
    f.write(content)
    f.close()
  def bins(self, name):
    if name == "unzip": return unzip
    if name == "mkzip": return mkzip
    exe = os.path.join("..", "bins", name)
    if exeext: exe += exeext
    return exe
  def gentext(self, size):
    random.seed(1234567891234567890)
    result = StringIO()
    old1 = ''
    old2 = ''
    for i in xrange(size):
       while True:
          x = random.choice("       abcdefghijklmnopqrstuvwxyz\n")
          if x == old1 or x == old2: continue
          old1 = old2
          old2 = x
          break
       result.write(x)
    return result.getvalue()
  ################################################################
  def test_100_make_test0_zip(self):
    """ create a test.zip for later tests using standard 'zip'
    It will fall back to a variant in the source code if 'zip'
    is not installed on the build host. The content is just
    the README file that we can check for equality later on. """
    zipfile="test0.zip"
    tmpdir="test0.tmp"
    exe=self.bins("mkzip")
    filename = os.path.join(tmpdir,"README")
    filetext = self.readme()
    self.mkfile(filename, filetext)
    shell("{exe} ../{zipfile} README".format(**locals()), cwd=tmpdir)
    self.assertGreater(os.path.getsize(zipfile), 10)
  def test_101_make_test1_zip(self):
    """ create a test1.zip for later tests using standard 'zip'
    It will fall back to a variant in the source code if 'zip'
    is not installed on the build host. The archive has 10
    generic files that we can check for their content later. """
    zipfile="test1.zip"
    tmpdir="test1.tmp"
    exe=self.bins("mkzip")
    for i in [1,2,3,4,5,6,7,8,9]:
       filename = os.path.join(tmpdir,"file.%i" % i)
       filetext = "file-%i\n" % i
       self.mkfile(filename, filetext)
    filename = os.path.join(tmpdir,"README")
    filetext = self.readme()
    self.mkfile(filename, filetext)
    shell("{exe} ../{zipfile} ??*.* README".format(**locals()), cwd=tmpdir)
    self.assertGreater(os.path.getsize(zipfile), 10)
  def test_102_make_test2_zip(self):
    """ create a test2.zip for later tests using standard 'zip'
    It will NOT fall back to a variant in the source code.
    The archive has 100 generic files with known content. """
    zipfile="test2.zip"
    tmpdir="test2.tmp"
    exe=self.bins("mkzip")
    for i in xrange(100):
       filename = os.path.join(tmpdir,"file.%02i" % i)
       filetext = "file-%02i\n" % i
       self.mkfile(filename, filetext)
    filename = os.path.join(tmpdir,"README")
    filetext = self.readme()
    self.mkfile(filename, filetext)
    shell("{exe} ../{zipfile} ??*.* README".format(**locals()), cwd=tmpdir)
    self.assertGreater(os.path.getsize(zipfile), 10)
  def test_103_make_test3_zip(self):
    """ create a test3.zip for later tests using standard 'zip'
    It will NOT fall back to a variant in the source code.
    The archive has 1000 generic files with known content. """
    zipfile="test3.zip"
    tmpdir="test3.tmp"
    exe=self.bins("mkzip")
    for i in xrange(1000):
       filename = os.path.join(tmpdir,"file.%03i" % i)
       filetext = "file-%03i\n" % i
       self.mkfile(filename, filetext)
    filename = os.path.join(tmpdir,"README")
    filetext = self.readme()
    self.mkfile(filename, filetext)
    shell("{exe} ../{zipfile} ??*.* README".format(**locals()), cwd=tmpdir)
    self.assertGreater(os.path.getsize(zipfile), 10)
  def test_104_make_test4_zip(self):
    """ create a test4.zip for later tests using standard 'zip'
    It will NOT fall back to a variant in the source code.
    The archive has 10000 generic files with known content
    and they are stored (NOT compressed) in the archive. """
    zipfile="test4.zip"
    tmpdir="test4.tmp"
    exe=self.bins("mkzip")
    for i in xrange(10000):
       filename = os.path.join(tmpdir,"file%04i.txt" % i)
       filetext = "file-%04i\n" % i
       self.mkfile(filename, filetext)
    filename = os.path.join(tmpdir,"README")
    filetext = self.readme()
    self.mkfile(filename, filetext)
    shell("{exe} -n README ../{zipfile} ??*.* README".format(**locals()), cwd=tmpdir)
    self.assertGreater(os.path.getsize(zipfile), 1000000)
  def test_105_make_test5_zip(self):
    """ create a test5.zip for later tests using standard 'zip'
    It will NOT fall back to a variant in the source code.
    The archive has files at multiple subdirectories depth
    and of varying sizes each. """
    zipfile="test5.zip"
    tmpdir="test5.tmp"
    exe=self.bins("mkzip")
    for depth in xrange(20):
      dirpath = ""
      for i in xrange(depth):
        if i:
          dirpath += "subdir%i/" % i
      for size in xrange(18):
        size = 2 ** size
        filetext = self.gentext(size)
        filepart = "file%i-%i.txt" % (depth, size)
        filename = os.path.join(tmpdir, dirpath + filepart )
        self.mkfile(filename, filetext)
    filename = os.path.join(tmpdir,"README")
    filetext = self.readme()
    self.mkfile(filename, filetext)
    shell("{exe} ../{zipfile} -r file* subdir* README".format(**locals()), cwd=tmpdir)
    self.assertGreater(os.path.getsize(zipfile), 1000000)
  def test_110_make_test0_dat(self):
    """ create test.dat from test.zip with xorcopy """
    zipfile = "test0.zip"
    datfile = "test0x.dat"
    exe = self.bins("zzxorcopy")
    shell("{exe} {zipfile} {datfile}".format(**locals()))
    self.assertGreater(os.path.getsize(datfile), 10)
    self.assertEqual(os.path.getsize(datfile), os.path.getsize(zipfile))
  def test_111_make_test1_dat(self):
    """ create test.dat from test.zip with xorcopy """
    zipfile = "test1.zip"
    datfile = "test1x.dat"
    exe = self.bins("zzxorcopy")
    shell("{exe} {zipfile} {datfile}".format(**locals()))
    self.assertGreater(os.path.getsize(datfile), 10)
    self.assertEqual(os.path.getsize(datfile), os.path.getsize(zipfile))
  def test_112_make_test2_dat(self):
    """ create test.dat from test.zip with xorcopy """
    zipfile = "test2.zip"
    datfile = "test2x.dat"
    exe = self.bins("zzxorcopy")
    shell("{exe} {zipfile} {datfile}".format(**locals()))
    self.assertGreater(os.path.getsize(datfile), 10)
    self.assertEqual(os.path.getsize(datfile), os.path.getsize(zipfile))
  def test_113_make_test3_dat(self):
    """ create test.dat from test.zip with xorcopy """
    zipfile = "test3.zip"
    datfile = "test3x.dat"
    exe = self.bins("zzxorcopy")
    shell("{exe} {zipfile} {datfile}".format(**locals()))
    self.assertGreater(os.path.getsize(datfile), 10)
    self.assertEqual(os.path.getsize(datfile), os.path.getsize(zipfile))
  def test_114_make_test4_dat(self):
    """ create test.dat from test.zip with xorcopy """
    zipfile = "test4.zip"
    datfile = "test4x.dat"
    exe = self.bins("zzxorcopy")
    shell("{exe} {zipfile} {datfile}".format(**locals()))
    self.assertGreater(os.path.getsize(datfile), 10)
    self.assertEqual(os.path.getsize(datfile), os.path.getsize(zipfile))
  def test_200_zziptest_test0_zip(self):
    """ run zziptest on test.zip """
    zipfile = "test0.zip"
    logfile = "test0.log"
    exe = self.bins("zziptest")
    shell("{exe} --quick {zipfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
  def test_201_zziptest_test1_zip(self):
    """ run zziptest on test.zip """
    zipfile = "test1.zip"
    logfile = "test1.log"
    exe = self.bins("zziptest")
    shell("{exe} --quick {zipfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
  def test_202_zziptest_test2_zip(self):
    """ run zziptest on test.zip """
    zipfile = "test2.zip"
    logfile = "test2.log"
    exe = self.bins("zziptest")
    shell("{exe} --quick {zipfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
  def test_203_zziptest_test3_zip(self):
    """ run zziptest on test.zip """
    zipfile = "test3.zip"
    logfile = "test3.log"
    exe = self.bins("zziptest")
    shell("{exe} --quick {zipfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
  def test_204_zziptest_test4_zip(self):
    """ run zziptest on test.zip """
    zipfile = "test4.zip"
    logfile = "test4.log"
    exe = self.bins("zziptest")
    shell("{exe} --quick {zipfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
  def test_210_zzcat_test0_zip(self):
    """ run zzcat on test.zip using just test/README """
    zipfile = "test0.zip"
    getfile = "test0/README"
    logfile = "test0.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
  def test_211_zzcat_test1_zip(self):
    """ run zzcat on test.zip using just test/README """
    zipfile = "test1.zip"
    getfile = "test1/README"
    logfile = "test1.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test1/file.1"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-1\n", run.output)
  def test_212_zzcat_test2_zip(self):
    """ run zzcat on test.zip using just test/README """
    zipfile = "test2.zip"
    getfile = "test2/README"
    logfile = "test2.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test2/file.22"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-22\n", run.output)
  def test_213_zzcat_test3_zip(self):
    """ run zzcat on test.zip using just test/README """
    zipfile = "test3.zip"
    getfile = "test3/README"
    logfile = "test3.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test3/file.999"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-999\n", run.output)
  def test_214_zzcat_test4_zip(self):
    """ run zzcat on test.zip using just test/README """
    zipfile = "test4.zip"
    getfile = "test4/README"
    logfile = "test4.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test4/file9999.txt"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-9999\n", run.output)
  def test_220_zzdir_test0_zip(self):
    """ run zzdir on test0.zip using just 'test0' """
    zipfile = "test0.zip"
    getfile = "test0"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertLess(len(run.output), 30)
  def test_221_zzdir_test1_zip(self):
    """ run zzdir on test1.zip using just 'test1' """
    zipfile = "test1.zip"
    getfile = "test1"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file.1\n', run.output)
    self.assertIn(' file.2\n', run.output)
    self.assertIn(' file.9\n', run.output)
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_222_zzdir_test2_zip(self):
    """ run zzdir on test2.zip using just 'test2' """
    zipfile = "test2.zip"
    getfile = "test2"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file.01\n', run.output)
    self.assertIn(' file.22\n', run.output)
    self.assertIn(' file.99\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_223_zzdir_test3_zip(self):
    """ run zzdir on test3.zip using just 'test3' """
    zipfile = "test3.zip"
    getfile = "test3"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file.001\n', run.output)
    self.assertIn(' file.222\n', run.output)
    self.assertIn(' file.999\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_224_zzdir_test4_zip(self):
    """ run zzdir on test4.zip using just 'test4' """
    zipfile = "test4.zip"
    getfile = "test4"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file0001.txt\n', run.output)
    self.assertIn(' file2222.txt\n', run.output)
    self.assertIn(' file9999.txt\n', run.output)
    self.assertNotIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_320_zzxordir_test0_dat(self):
    """ run zzxordir on test0x.dat """
    zipfile = "test0x.dat"
    getfile = "test0x.dat"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()), returncodes = [0,1])
    self.assertEqual(run.returncode, 1)
    self.assertEqual("", run.output)
    self.assertIn("did not open test", run.errors)
    exe = self.bins("zzxordir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertLess(len(run.output), 30)
  def test_321_zzxordir_test1_dat(self):
    """ run zzxordir on test1x.dat using just 'test1x' """
    zipfile = "test1x.dat"
    getfile = "test1x.dat"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()), returncodes = [0,1])
    self.assertEqual(run.returncode, 1)
    self.assertEqual("", run.output)
    self.assertIn("did not open test", run.errors)
    exe = self.bins("zzxordir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file.1\n', run.output)
    self.assertIn(' file.2\n', run.output)
    self.assertIn(' file.9\n', run.output)
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_322_zzxordir_test2_dat(self):
    """ run zzxordir on test2x.dat using just 'test2x' """
    zipfile = "test2x.dat"
    getfile = "test2x"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()), returncodes = [0,1])
    self.assertEqual(run.returncode, 1)
    self.assertEqual("", run.output)
    self.assertIn("did not open test", run.errors)
    exe = self.bins("zzxordir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file.01\n', run.output)
    self.assertIn(' file.22\n', run.output)
    self.assertIn(' file.99\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_323_zzxordir_test3_dat(self):
    """ run zzxordir on test3x.dat using just 'test3x' """
    zipfile = "test3x.dat"
    getfile = "test3x"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()), returncodes = [0,1])
    self.assertEqual(run.returncode, 1)
    self.assertEqual("", run.output)
    self.assertIn("did not open test", run.errors)
    exe = self.bins("zzxordir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file.001\n', run.output)
    self.assertIn(' file.222\n', run.output)
    self.assertIn(' file.999\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_324_zzxordir_test4_zip(self):
    """ run zzxordir on test4x.dat using just 'test4x' """
    zipfile = "test4x.dat"
    getfile = "test4x"
    exe = self.bins("zzdir")
    run = shell("{exe} {getfile} ".format(**locals()), returncodes = [0,1])
    self.assertEqual(run.returncode, 1)
    self.assertEqual("", run.output)
    self.assertIn("did not open test", run.errors)
    exe = self.bins("zzxordir")
    run = shell("{exe} {getfile} ".format(**locals()))
    self.assertIn(' file0001.txt\n', run.output)
    self.assertIn(' file2222.txt\n', run.output)
    self.assertIn(' file9999.txt\n', run.output)
    self.assertNotIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_340_zzxorcat_test0_zip(self):
    """ run zzxorcat on testx.zip using just testx/README """
    getfile = "test0x/README"
    logfile = "test0x.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} ".format(**locals()), lang="C")
    self.assertEqual("", run.output)
    self.assertIn("No such file or directory", run.errors)
    exe = self.bins("zzxorcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
  def test_341_zzxorcat_test1_zip(self):
    """ run zzxorcat on testx.zip using just testx/README """
    getfile = "test1x/README"
    logfile = "test1x.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} ".format(**locals()), lang="C")
    self.assertEqual("", run.output)
    self.assertIn("No such file or directory", run.errors)
    exe = self.bins("zzxorcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test1x/file.1"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-1\n", run.output)
  def test_342_zzxorcat_test2_zip(self):
    """ run zzxorcat on testx.zip using just testx/README """
    getfile = "test2x/README"
    logfile = "test2x.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} ".format(**locals()), lang="C")
    self.assertEqual("", run.output)
    self.assertIn("No such file or directory", run.errors)
    exe = self.bins("zzxorcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test2x/file.22"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-22\n", run.output)
  def test_343_zzxorcat_test3_zip(self):
    """ run zzxorcat on testx.zip using just testx/README """
    getfile = "test3x/README"
    logfile = "test3x.readme.txt"
    exe = self.bins("zzcat")
    run = shell("{exe} {getfile} ".format(**locals()), lang="C")
    self.assertEqual("", run.output)
    self.assertIn("No such file or directory", run.errors)
    exe = self.bins("zzxorcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test3x/file.999"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-999\n", run.output)
  def test_344_zzxorcat_test4_zip(self):
    """ run zzxorcat on testx.zip using just testx/README """
    getfile = "test4x/README"
    logfile = "test4x.readme.txt"
    exe = self.bins("zzxorcat")
    run = shell("{exe} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "test4x/file9999.txt"
    run = shell("{exe} {getfile}".format(**locals()))
    self.assertEqual("file-9999\n", run.output)
  #####################################################################
  # check unzzip
  #####################################################################
  def test_400_infozip_cat_test0_zip(self):
    """ run inzo-zip cat test.zip using just archive README """
    zipfile = "test0.zip"
    getfile = "README"
    logfile = "test0.readme.pk.txt"
    exe = self.bins("unzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
  def test_401_infozip_cat_test1_zip(self):
    """ run info-zip cat test.zip using just archive README """
    zipfile = "test1.zip"
    getfile = "README"
    logfile = "test1.readme.pk.txt"
    exe = self.bins("unzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.1"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-1\n", run.output)
  def test_402_infozip_cat_test2_zip(self):
    """ run info-zip cat test.zip using just archive README """
    zipfile = "test2.zip"
    getfile = "README"
    logfile = "test2.readme.pk.txt"
    exe = self.bins("unzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.22"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-22\n", run.output)
  def test_405_zzcat_big_test5_zip(self):
    """ run info-zip cat test.zip using archive README """
    zipfile = "test5.zip"
    getfile = "README"
    logfile = "test5.readme.pk.txt"
    exe = self.bins("unzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "subdir1/subdir2/subdir3/subdir4/subdir5/subdir6/file7-1024.txt"
    compare = self.gentext(1024)
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual(compare, run.output)
  def test_410_zzcat_big_test0_zip(self):
    """ run zzcat-big on test.zip using just archive README """
    zipfile = "test0.zip"
    getfile = "README"
    logfile = "test0.readme.big.txt"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
  def test_411_zzcat_big_test1_zip(self):
    """ run zzcat-big on test.zip using just archive README """
    zipfile = "test1.zip"
    getfile = "README"
    logfile = "test1.readme.big.txt"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.1"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-1\n", run.output)
  def test_412_zzcat_big_test2_zip(self):
    """ run zzcat-seeke on test.zip using just archive README """
    zipfile = "test2.zip"
    getfile = "README"
    logfile = "test2.readme.big.txt"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.22"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-22\n", run.output)
  def test_415_zzcat_big_test5_zip(self):
    """ run zzcat-big on test.zip using archive README """
    zipfile = "test5.zip"
    getfile = "README"
    logfile = "test5.readme.zap.txt"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "subdir1/subdir2/subdir3/subdir4/subdir5/subdir6/file7-1024.txt"
    compare = self.gentext(1024)
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual(compare, run.output)
  def test_420_zzcat_mem_test0_zip(self):
    """ run zzcat-mem on test.zip using just archive README """
    zipfile = "test0.zip"
    getfile = "README"
    logfile = "test0.readme.mem.txt"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
  def test_421_zzcat_mem_test1_zip(self):
    """ run zzcat-mem on test.zip using archive README """
    zipfile = "test1.zip"
    getfile = "README"
    logfile = "test1.readme.mem.txt"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -p {zipfile}  {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.1"
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertEqual("file-1\n", run.output)
  def test_422_zzcat_mem_test2_zip(self):
    """ run zzcat-mem on test.zip using archive README """
    zipfile = "test2.zip"
    getfile = "README"
    logfile = "test2.readme.mem.txt"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.22"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-22\n", run.output)
  def test_423_zzcat_mem_test3_zip(self):
    """ run zzcat-mem on test.zip using archive README """
    zipfile = "test3.zip"
    getfile = "README"
    logfile = "test3.readme.mem.txt"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.999"
    run = shell("{exe} -p {zipfile}  {getfile}".format(**locals()))
    self.assertEqual("file-999\n", run.output)
  def test_424_zzcat_mem_test4_zip(self):
    """ run zzcat-mem on test.zip using archive README """
    zipfile = "test4.zip"
    getfile = "README"
    logfile = "test4.readme.mem.txt"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file9999.txt"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-9999\n", run.output)
  def test_425_zzcat_mem_test5_zip(self):
    """ run zzcat-mem on test.zip using archive README """
    zipfile = "test5.zip"
    getfile = "README"
    logfile = "test5.readme.zap.txt"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "subdir1/subdir2/subdir3/subdir4/subdir5/subdir6/file7-1024.txt"
    compare = self.gentext(1024)
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual(compare, run.output)
  def test_430_zzcat_mix_test0_zip(self):
    """ run zzcat-mix on test.zip using just archive README """
    zipfile = "test0.zip"
    getfile = "README"
    logfile = "test0.readme.mix.txt"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
  def test_431_zzcat_mix_test1_zip(self):
    """ run zzcat-mix on test.zip using archive README """
    zipfile = "test1.zip"
    getfile = "README"
    logfile = "test1.readme.mix.txt"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -p {zipfile}  {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.1"
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertEqual("file-1\n", run.output)
  def test_432_zzcat_mix_test2_zip(self):
    """ run zzcat-mix on test.zip using archive README """
    zipfile = "test2.zip"
    getfile = "README"
    logfile = "test2.readme.mix.txt"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.22"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-22\n", run.output)
  def test_433_zzcat_mix_test3_zip(self):
    """ run zzcat-mix on test.zip using archive README """
    zipfile = "test3.zip"
    getfile = "README"
    logfile = "test3.readme.mix.txt"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.999"
    run = shell("{exe} -p {zipfile}  {getfile}".format(**locals()))
    self.assertEqual("file-999\n", run.output)
  def test_434_zzcat_mix_test4_zip(self):
    """ run zzcat-mix on test.zip using archive README """
    zipfile = "test4.zip"
    getfile = "README"
    logfile = "test4.readme.mix.txt"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file9999.txt"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-9999\n", run.output)
  def test_435_zzcat_mix_test5_zip(self):
    """ run zzcat-mix on test.zip using archive README """
    zipfile = "test5.zip"
    getfile = "README"
    logfile = "test5.readme.zap.txt"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "subdir1/subdir2/subdir3/subdir4/subdir5/subdir6/file7-1024.txt"
    compare = self.gentext(1024)
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual(compare, run.output)
  def test_440_zzcat_zap_test0_zip(self):
    """ run zzcat-zap on test.zip using just archive README """
    zipfile = "test0.zip"
    getfile = "README"
    logfile = "test0.readme.txt"
    exe = self.bins("unzzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
  def test_441_zzcat_zap_test1_zip(self):
    """ run zzcat-zap on test.zip using archive README """
    zipfile = "test1.zip"
    getfile = "README"
    logfile = "test1.readme.zap.txt"
    exe = self.bins("unzzip")
    run = shell("{exe} -p {zipfile}  {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.1"
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertEqual("file-1\n", run.output)
  def test_442_zzcat_zap_test2_zip(self):
    """ run zzcat-zap on test.zip using archive README """
    zipfile = "test2.zip"
    getfile = "README"
    logfile = "test2.readme.zap.txt"
    exe = self.bins("unzzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.22"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-22\n", run.output)
  def test_443_zzcat_zap_test3_zip(self):
    """ run zzcat-zap on test.zip using archive README """
    zipfile = "test3.zip"
    getfile = "README"
    logfile = "test3.readme.zap.txt"
    exe = self.bins("unzzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file.999"
    run = shell("{exe} -p {zipfile}  {getfile}".format(**locals()))
    self.assertEqual("file-999\n", run.output)
  def test_444_zzcat_zap_test4_zip(self):
    """ run zzcat-zap on test.zip using archive README """
    zipfile = "test4.zip"
    getfile = "README"
    logfile = "test4.readme.zap.txt"
    exe = self.bins("unzzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "file9999.txt"
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual("file-9999\n", run.output)
  def test_445_zzcat_zap_test5_zip(self):
    """ run zzcat-zap on test.zip using archive README """
    zipfile = "test5.zip"
    getfile = "README"
    logfile = "test5.readme.zap.txt"
    exe = self.bins("unzzip")
    run = shell("{exe} -p {zipfile} {getfile} | tee {logfile}".format(**locals()))
    self.assertGreater(os.path.getsize(logfile), 10)
    self.assertEqual(run.output.split("\n"), self.readme().split("\n"))
    getfile = "subdir1/subdir2/subdir3/subdir4/subdir5/subdir6/file7-1024.txt"
    compare = self.gentext(1024)
    run = shell("{exe} -p {zipfile} {getfile}".format(**locals()))
    self.assertEqual(compare, run.output)

  def test_500_infozipdir_test0_zip(self):
    """ run info-zip dir test0.zip  """
    zipfile = "test0.zip"
    getfile = "test0.zip"
    exe = self.bins("unzip")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' README\n', run.output)
    self.assertLess(len(run.output), 230)
  def test_501_infozipdir_test1_zip(self):
    """ run info-zip dir test1.zip  """
    zipfile = "test1.zip"
    getfile = "test1.zip"
    exe = self.bins("unzip")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file.1\n', run.output)
    self.assertIn(' file.2\n', run.output)
    self.assertIn(' file.9\n', run.output)
    self.assertIn(' README\n', run.output)
  def test_502_infozipdir_big_test2_zip(self):
    """ run info-zip dir test2.zip """
    zipfile = "test2.zip"
    getfile = "test2.zip"
    exe = self.bins("unzip")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file.01\n', run.output)
    self.assertIn(' file.22\n', run.output)
    self.assertIn(' file.99\n', run.output)
  def test_503_infozipdir_big_test3_zip(self):
    """ run info-zip dir test3.zip  """
    zipfile = "test3.zip"
    getfile = "test3.zip"
    exe = self.bins("unzip")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file.001\n', run.output)
    self.assertIn(' file.222\n', run.output)
    self.assertIn(' file.999\n', run.output)
  def test_504_infozipdir_big_test4_zip(self):
    """ run info-zip dir test4.zip """
    zipfile = "test4.zip"
    getfile = "test4.zip"
    exe = self.bins("unzip")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file0001.txt\n', run.output)
    self.assertIn(' file2222.txt\n', run.output)
    self.assertIn(' file9999.txt\n', run.output)
  def test_505_infozipdir_big_test5_zip(self):
    """ run info-zip dir on test5.zip """
    zipfile = "test5.zip"
    getfile = "test5.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn('/subdir14/file15-128.txt\n', run.output)
    self.assertIn('/subdir5/subdir6/', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_510_zzdir_big_test0_zip(self):
    """ run zzdir-big on test0.zip  """
    zipfile = "test0.zip"
    getfile = "test0.zip"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' README\n', run.output)
    self.assertLess(len(run.output), 30)
  def test_511_zzdir_big_test1_zip(self):
    """ run zzdir-big on test1.zip  """
    zipfile = "test1.zip"
    getfile = "test1.zip"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file.1\n', run.output)
    self.assertIn(' file.2\n', run.output)
    self.assertIn(' file.9\n', run.output)
    self.assertIn(' README\n', run.output)
  def test_512_zzdir_big_test2_zip(self):
    """ run zzdir-big on test2.zip """
    zipfile = "test2.zip"
    getfile = "test2.zip"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file.01\n', run.output)
    self.assertIn(' file.22\n', run.output)
    self.assertIn(' file.99\n', run.output)
  def test_513_zzdir_big_test3_zip(self):
    """ run zzdir-big on test3.zip  """
    zipfile = "test3.zip"
    getfile = "test3.zip"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file.001\n', run.output)
    self.assertIn(' file.222\n', run.output)
    self.assertIn(' file.999\n', run.output)
  def test_514_zzdir_big_test4_zip(self):
    """ run zzdir-big on test4.zip """
    zipfile = "test4.zip"
    getfile = "test4.zip"
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {getfile} ".format(**locals()))
    self.assertIn(' file0001.txt\n', run.output)
    self.assertIn(' file2222.txt\n', run.output)
    self.assertIn(' file9999.txt\n', run.output)
  def test_515_zzdir_big_test5_zip(self):
    """ run zzdir-big on test5.zip """
    zipfile = "test5.zip"
    getfile = "test5.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn('/subdir14/file15-128.txt\n', run.output)
    self.assertIn('/subdir5/subdir6/', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_520_zzdir_mem_test0_zip(self):
    """ run zzdir-mem on test0.zip  """
    zipfile = "test0.zip"
    getfile = "test0.zip"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertLess(len(run.output), 30)
  def test_521_zzdir_mem_test1_zip(self):
    """ run zzdir-mem on test1.zip  """
    zipfile = "test1.zip"
    getfile = "test1.zip"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.1\n', run.output)
    self.assertIn(' file.2\n', run.output)
    self.assertIn(' file.9\n', run.output)
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_522_zzdir_mem_test2_zip(self):
    """ run zzdir-mem on test2.zip """
    zipfile = "test2.zip"
    getfile = "test2.zip"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.01\n', run.output)
    self.assertIn(' file.22\n', run.output)
    self.assertIn(' file.99\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_523_zzdir_mem_test3_zip(self):
    """ run zzdir-mem on test3.zip  """
    zipfile = "test3.zip"
    getfile = "test3.zip"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.001\n', run.output)
    self.assertIn(' file.222\n', run.output)
    self.assertIn(' file.999\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_524_zzdir_mem_test4_zip(self):
    """ run zzdir-mem on test4.zip """
    zipfile = "test4.zip"
    getfile = "test4.zip"
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file0001.txt\n', run.output)
    self.assertIn(' file2222.txt\n', run.output)
    self.assertIn(' file9999.txt\n', run.output)
    self.assertNotIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_525_zzdir_mem_test5_zip(self):
    """ run zzdir-mem on test5.zip """
    zipfile = "test5.zip"
    getfile = "test5.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn('/subdir14/file15-128.txt\n', run.output)
    self.assertIn('/subdir5/subdir6/', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_530_zzdir_mix_test0_zip(self):
    """ run zzdir-mix on test0.zip  """
    # self.skipTest("todo")
    zipfile = "test0.zip"
    getfile = "test0.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertLess(len(run.output), 30)
  def test_531_zzdir_mix_test1_zip(self):
    """ run zzdir-mix on test1.zip  """
    zipfile = "test1.zip"
    getfile = "test1.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.1\n', run.output)
    self.assertIn(' file.2\n', run.output)
    self.assertIn(' file.9\n', run.output)
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_532_zzdir_mix_test2_zip(self):
    """ run zzdir-mix on test2.zip """
    zipfile = "test2.zip"
    getfile = "test2.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.01\n', run.output)
    self.assertIn(' file.22\n', run.output)
    self.assertIn(' file.99\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_533_zzdir_mix_test3_zip(self):
    """ run zzdir-mix on test3.zip  """
    zipfile = "test3.zip"
    getfile = "test3.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.001\n', run.output)
    self.assertIn(' file.222\n', run.output)
    self.assertIn(' file.999\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_534_zzdir_mix_test4_zip(self):
    """ run zzdir-mix on test4.zip """
    zipfile = "test4.zip"
    getfile = "test4.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file0001.txt\n', run.output)
    self.assertIn(' file2222.txt\n', run.output)
    self.assertIn(' file9999.txt\n', run.output)
    self.assertNotIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_535_zzdir_mix_test5_zip(self):
    """ run zzdir-mix on test5.zip """
    zipfile = "test5.zip"
    getfile = "test5.zip"
    exe = self.bins("unzzip-mix")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn('/subdir14/file15-128.txt\n', run.output)
    self.assertIn('/subdir5/subdir6/', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_540_zzdir_zap_test0_zip(self):
    """ run zzdir-zap on test0.zip  """
    zipfile = "test0.zip"
    getfile = "test0.zip"
    exe = self.bins("unzzip")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertLess(len(run.output), 30)
  def test_541_zzdir_zap_test1_zip(self):
    """ run zzdir-zap on test1.zip  """
    zipfile = "test1.zip"
    getfile = "test1.zip"
    exe = self.bins("unzzip")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.1\n', run.output)
    self.assertIn(' file.2\n', run.output)
    self.assertIn(' file.9\n', run.output)
    self.assertIn(' README\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_542_zzdir_zap_test2_zip(self):
    """ run zzdir-zap on test2.zip """
    zipfile = "test2.zip"
    getfile = "test2.zip"
    exe = self.bins("unzzip")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.01\n', run.output)
    self.assertIn(' file.22\n', run.output)
    self.assertIn(' file.99\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_543_zzdir_zap_test3_zip(self):
    """ run zzdir-zap on test3.zip  """
    zipfile = "test3.zip"
    getfile = "test3.zip"
    exe = self.bins("unzzip")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file.001\n', run.output)
    self.assertIn(' file.222\n', run.output)
    self.assertIn(' file.999\n', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_544_zzdir_zap_test4_zip(self):
    """ run zzdir-zap on test4.zip """
    zipfile = "test4.zip"
    getfile = "test4.zip"
    exe = self.bins("unzzip")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn(' file0001.txt\n', run.output)
    self.assertIn(' file2222.txt\n', run.output)
    self.assertIn(' file9999.txt\n', run.output)
    self.assertNotIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_545_zzdir_zap_test5_zip(self):
    """ run zzdir-zap on test5.zip """
    zipfile = "test5.zip"
    getfile = "test5.zip"
    exe = self.bins("unzzip")
    run = shell("{exe} -v {getfile} ".format(**locals()))
    self.assertIn('/subdir14/file15-128.txt\n', run.output)
    self.assertIn('/subdir5/subdir6/', run.output)
    self.assertIn(' defl:N ', run.output)
    self.assertIn(' stored ', run.output)
  def test_595_zzextract_zap_test5_zip(self):
    """ run zzextract-zap on test5.zip 
        => coughs up a SEGFAULT in zzip_dir_close() ?!?"""
    zipfile = "test5.zip"
    getfile = "test5.zip"
    tmpdir = "tmp.test_595"
    testdir(tmpdir)
    exe = self.bins("unzzip")
    run = shell("cd {tmpdir} && ../{exe} ../{getfile} ".format(**locals()))
    self.assertTrue(tmpdir+'/subdir1/subdir2/file3-1024.txt')

  url_CVE_2017_5977 = "https://raw.githubusercontent.com/asarubbo/poc/master/"
  zip_CVE_2017_5977 = "00153-zziplib-invalidread-zzip_mem_entry_extra_block"
  def test_600_infozipdir_CVE_2017_5977(self):
    """ run info-zip dir test0.zip  """
    tmpdir = "tmp.test_600"
    filename = self.zip_CVE_2017_5977
    file_url = self.url_CVE_2017_5977
    trycopy("tmp.test_601", filename, tmpdir)
    testdir(tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 2])
    self.assertIn(" didn't find end-of-central-dir signature at end of central dir", run.errors)
    self.assertIn(" 2 extra bytes at beginning or within zipfile", run.errors)
    self.assertLess(len(run.output), 280)
  def test_601_zzipdir_big_CVE_2017_5977(self):
    """ run info-zip -l $(CVE_2017_5977).zip  """
    tmpdir = "tmp.test_601"
    filename = self.zip_CVE_2017_5977
    file_url = self.url_CVE_2017_5977
    testdir(tmpdir)
    trycopy("tmp.test_600", filename, tmpdir)
    trycopy("tmp.test_602", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" stored test", run.output)
  def test_602_zzipdir_mem_CVE_2017_5977(self):
    """ run unzzip-mem -l $(CVE_2017_5977).zip  """
    tmpdir = "tmp.test_602"
    filename = self.zip_CVE_2017_5977
    file_url = self.url_CVE_2017_5977
    testdir(tmpdir)
    trycopy("tmp.test_601", filename, tmpdir)
    trycopy("tmp.test_603", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 test", run.output)
  def test_603_zzipdir_mem_CVE_2017_5977(self):
    """ run unzzip-mem -l $(CVE_2017_5977).zip  """
    tmpdir = "tmp.test_603"
    filename = self.zip_CVE_2017_5977
    file_url = self.url_CVE_2017_5977
    testdir(tmpdir)
    trycopy("tmp.test_602", filename, tmpdir)
    trycopy("tmp.test_604", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 test", run.output)
  def test_604_zzipdir_zap_CVE_2017_5977(self):
    """ run unzzip-mix -l $(CVE_2017_5977).zip  """
    tmpdir = "tmp.test_604"
    filename = self.zip_CVE_2017_5977
    file_url = self.url_CVE_2017_5977
    testdir(tmpdir)
    trycopy("tmp.test_603", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 255])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 test", run.output)

  url_CVE_2017_5978 = "https://raw.githubusercontent.com/asarubbo/poc/master/"
  zip_CVE_2017_5978 = "00156-zziplib-oobread-zzip_mem_entry_new"
  def test_610_infozipdir_CVE_2017_5978(self):
    """ run info-zip dir test0.zip  """
    tmpdir = "tmp.test_610"
    filename = self.zip_CVE_2017_5978
    file_url = self.url_CVE_2017_5978
    trycopy("tmp.test_611", filename, tmpdir)
    testdir(tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 3])
    self.assertIn(' missing 4608 bytes in zipfile', run.errors)
    self.assertIn(' attempt to seek before beginning of zipfile', run.errors)
    self.assertLess(len(run.output), 80)
    self.assertLess(len(run.errors), 430)
  def test_611_zzipdir_big_CVE_2017_5978(self):
    """ run info-zip -l $(CVE_2017_5978).zip  """
    tmpdir = "tmp.test_611"
    filename = self.zip_CVE_2017_5978
    file_url = self.url_CVE_2017_5978
    testdir(tmpdir)
    trycopy("tmp.test_610", filename, tmpdir)
    trycopy("tmp.test_612", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" stored (null)", run.output)
  def test_612_zzipdir_mem_CVE_2017_5978(self):
    """ run unzzip-mem -l $(CVE_2017_5978).zip  """
    tmpdir = "tmp.test_612"
    filename = self.zip_CVE_2017_5978
    file_url = self.url_CVE_2017_5978
    testdir(tmpdir)
    trycopy("tmp.test_611", filename, tmpdir)
    trycopy("tmp.test_613", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 1)
    self.assertLess(len(run.errors), 180)
    self.assertIn("zzip_mem_disk_load : unable to load entry", run.errors)
    self.assertIn("zzip_mem_disk_open : unable to load disk", run.errors)
  def test_613_zzipdir_mem_CVE_2017_5978(self):
    """ run unzzip-mem -l $(CVE_2017_5978).zip  """
    tmpdir = "tmp.test_613"
    filename = self.zip_CVE_2017_5978
    file_url = self.url_CVE_2017_5978
    testdir(tmpdir)
    trycopy("tmp.test_612", filename, tmpdir)
    trycopy("tmp.test_614", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 1)
    self.assertLess(len(run.errors), 180)
    self.assertIn("zzip_mem_disk_load : unable to load entry", run.errors)
    self.assertIn("zzip_mem_disk_open : unable to load disk", run.errors)
  @unittest.expectedFailure
  def test_614_zzipdir_zap_CVE_2017_5978(self):
    """ run unzzip-mix -l $(CVE_2017_5978).zip  """
    tmpdir = "tmp.test_614"
    filename = self.zip_CVE_2017_5978
    file_url = self.url_CVE_2017_5978
    testdir(tmpdir)
    trycopy("tmp.test_613", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 255])
    self.assertLess(len(run.output), 1)
    self.assertLess(len(run.errors), 180)
    self.assertIn("zzip_mem_disk_load : unable to load entry", run.errors)
    self.assertIn("zzip_mem_disk_open : unable to load disk", run.errors)

  url_CVE_2017_5979 = "https://raw.githubusercontent.com/asarubbo/poc/master/"
  zip_CVE_2017_5979 = "00157-zziplib-nullptr-prescan_entry"
  def test_620_infozipdir_CVE_2017_5979(self):
    """ run info-zip dir test0.zip  """
    tmpdir = "tmp.test_620"
    filename = self.zip_CVE_2017_5979
    file_url = self.url_CVE_2017_5979
    trycopy("tmp.test_621", filename, tmpdir)
    testdir(tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertIn(' 1 file', run.output)
    self.assertLess(len(run.output), 330)
    self.assertLess(len(run.errors), 1)
  def test_621_zzipdir_big_CVE_2017_5979(self):
    """ run info-zip -l $(CVE_2017_5979).zip  """
    tmpdir = "tmp.test_621"
    filename = self.zip_CVE_2017_5979
    file_url = self.url_CVE_2017_5979
    testdir(tmpdir)
    trycopy("tmp.test_620", filename, tmpdir)
    trycopy("tmp.test_622", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" stored a", run.output)
  def test_622_zzipdir_mem_CVE_2017_5979(self):
    """ run unzzip-mem -l $(CVE_2017_5979).zip  """
    tmpdir = "tmp.test_622"
    filename = self.zip_CVE_2017_5979
    file_url = self.url_CVE_2017_5979
    testdir(tmpdir)
    trycopy("tmp.test_621", filename, tmpdir)
    trycopy("tmp.test_623", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 a", run.output)
  def test_623_zzipdir_mem_CVE_2017_5979(self):
    """ run unzzip-mem -l $(CVE_2017_5979).zip  """
    tmpdir = "tmp.test_623"
    filename = self.zip_CVE_2017_5979
    file_url = self.url_CVE_2017_5979
    testdir(tmpdir)
    trycopy("tmp.test_622", filename, tmpdir)
    trycopy("tmp.test_624", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 a", run.output)
  def test_624_zzipdir_zap_CVE_2017_5979(self):
    """ run unzzip-mix -l $(CVE_2017_5979).zip  """
    tmpdir = "tmp.test_624"
    filename = self.zip_CVE_2017_5979
    file_url = self.url_CVE_2017_5979
    testdir(tmpdir)
    trycopy("tmp.test_623", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 255])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 a", run.output)

  url_CVE_2017_5974 = "https://raw.githubusercontent.com/asarubbo/poc/master/"
  zip_CVE_2017_5974 = "00150-zziplib-heapoverflow-__zzip_get32"
  def test_630_infozipdir_CVE_2017_5974(self):
    """ run info-zip dir test0.zip  """
    tmpdir = "tmp.test_630"
    filename = self.zip_CVE_2017_5974
    file_url = self.url_CVE_2017_5974
    trycopy("tmp.test_631", filename, tmpdir)
    testdir(tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 9])
    self.assertIn(' 1 file', run.output)
    self.assertLess(len(run.output), 330)
    self.assertLess(len(run.errors), 1)
  def test_631_zzipdir_big_CVE_2017_5974(self):
    """ run info-zip -l $(CVE_2017_5974).zip  """
    tmpdir = "tmp.test_631"
    filename = self.zip_CVE_2017_5974
    file_url = self.url_CVE_2017_5974
    testdir(tmpdir)
    trycopy("tmp.test_630", filename, tmpdir)
    trycopy("tmp.test_632", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" stored test", run.output)
  def test_632_zzipdir_mem_CVE_2017_5974(self):
    """ run unzzip-mem -l $(CVE_2017_5974).zip  """
    tmpdir = "tmp.test_632"
    filename = self.zip_CVE_2017_5974
    file_url = self.url_CVE_2017_5974
    testdir(tmpdir)
    trycopy("tmp.test_631", filename, tmpdir)
    trycopy("tmp.test_633", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 test", run.output)
  def test_633_zzipdir_mem_CVE_2017_5974(self):
    """ run unzzip-mem -l $(CVE_2017_5974).zip  """
    tmpdir = "tmp.test_633"
    filename = self.zip_CVE_2017_5974
    file_url = self.url_CVE_2017_5974
    testdir(tmpdir)
    trycopy("tmp.test_632", filename, tmpdir)
    trycopy("tmp.test_634", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 test", run.output)
  def test_634_zzipdir_zap_CVE_2017_5974(self):
    """ run unzzip-mix -l $(CVE_2017_5974).zip  """
    tmpdir = "tmp.test_634"
    filename = self.zip_CVE_2017_5974
    file_url = self.url_CVE_2017_5974
    testdir(tmpdir)
    trycopy("tmp.test_633", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 255])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" 3 test", run.output)

  url_CVE_2017_5975 = "https://raw.githubusercontent.com/asarubbo/poc/master/"
  zip_CVE_2017_5975 = "00151-zziplib-heapoverflow-__zzip_get64"
  def test_640_infozipdir_CVE_2017_5975(self):
    """ run info-zip dir test0.zip  """
    tmpdir = "tmp.test_640"
    filename = self.zip_CVE_2017_5975
    file_url = self.url_CVE_2017_5975
    trycopy("tmp.test_641", filename, tmpdir)
    testdir(tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 2])
    self.assertIn(' missing 10 bytes in zipfile', run.errors)
    self.assertIn("didn't find end-of-central-dir signature at end of central dir", run.errors)
    self.assertIn(' 1 file', run.output)
    self.assertLess(len(run.output), 330)
    self.assertLess(len(run.errors), 430)
  def test_641_zzipdir_big_CVE_2017_5975(self):
    """ run info-zip -l $(CVE_2017_5975).zip  """
    tmpdir = "tmp.test_641"
    filename = self.zip_CVE_2017_5975
    file_url = self.url_CVE_2017_5975
    testdir(tmpdir)
    trycopy("tmp.test_640", filename, tmpdir)
    trycopy("tmp.test_642", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" stored test", run.output)
  def test_642_zzipdir_mem_CVE_2017_5975(self):
    """ run unzzip-mem -l $(CVE_2017_5975).zip  """
    tmpdir = "tmp.test_642"
    filename = self.zip_CVE_2017_5975
    file_url = self.url_CVE_2017_5975
    testdir(tmpdir)
    trycopy("tmp.test_641", filename, tmpdir)
    trycopy("tmp.test_643", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 1)
    self.assertLess(len(run.errors), 180)
    self.assertIn("zzip_mem_disk_load : unable to load entry", run.errors)
    self.assertIn("zzip_mem_disk_open : unable to load disk", run.errors)
  def test_643_zzipdir_mem_CVE_2017_5975(self):
    """ run unzzip-mem -l $(CVE_2017_5975).zip  """
    tmpdir = "tmp.test_643"
    filename = self.zip_CVE_2017_5975
    file_url = self.url_CVE_2017_5975
    testdir(tmpdir)
    trycopy("tmp.test_642", filename, tmpdir)
    trycopy("tmp.test_644", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 1)
    self.assertLess(len(run.errors), 180)
    self.assertIn("zzip_mem_disk_load : unable to load entry", run.errors)
    self.assertIn("zzip_mem_disk_open : unable to load disk", run.errors)
  def test_644_zzipdir_zap_CVE_2017_5975(self):
    """ run unzzip-mix -l $(CVE_2017_5975).zip  """
    tmpdir = "tmp.test_644"
    filename = self.zip_CVE_2017_5975
    file_url = self.url_CVE_2017_5975
    testdir(tmpdir)
    trycopy("tmp.test_643", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 255])
    self.assertLess(len(run.output), 1)
    self.assertLess(len(run.errors), 180)
    self.assertIn(": Success", run.errors)

  url_CVE_2017_5976 = "https://raw.githubusercontent.com/asarubbo/poc/master/"
  zip_CVE_2017_5976 = "00152-zziplib-heapoverflow-zzip_mem_entry_extra_block"
  def test_650_infozipdir_CVE_2017_5976(self):
    """ run info-zip dir test0.zip  """
    tmpdir = "tmp.test_650"
    filename = self.zip_CVE_2017_5976
    file_url = self.url_CVE_2017_5976
    trycopy("tmp.test_651", filename, tmpdir)
    testdir(tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 2])
    self.assertIn(' 27 extra bytes at beginning or within zipfile', run.errors)
    self.assertIn("didn't find end-of-central-dir signature at end of central dir", run.errors)
    self.assertIn(' 1 file', run.output)
    self.assertLess(len(run.output), 330)
    self.assertLess(len(run.errors), 500)
  def test_651_zzipdir_big_CVE_2017_5976(self):
    """ run info-zip -l $(CVE_2017_5976).zip  """
    tmpdir = "tmp.test_651"
    filename = self.zip_CVE_2017_5976
    file_url = self.url_CVE_2017_5976
    testdir(tmpdir)
    trycopy("tmp.test_650", filename, tmpdir)
    trycopy("tmp.test_652", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-big")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn(" stored test", run.output)
  def test_652_zzipdir_mem_CVE_2017_5976(self):
    """ run unzzip-mem -l $(CVE_2017_5976).zip  """
    tmpdir = "tmp.test_652"
    filename = self.zip_CVE_2017_5976
    file_url = self.url_CVE_2017_5976
    testdir(tmpdir)
    trycopy("tmp.test_651", filename, tmpdir)
    trycopy("tmp.test_653", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn("3 test", run.output)
  def test_653_zzipdir_mem_CVE_2017_5976(self):
    """ run unzzip-mem -l $(CVE_2017_5976).zip  """
    tmpdir = "tmp.test_653"
    filename = self.zip_CVE_2017_5976
    file_url = self.url_CVE_2017_5976
    testdir(tmpdir)
    trycopy("tmp.test_652", filename, tmpdir)
    trycopy("tmp.test_654", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip-mem")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn("3 test", run.output)
  def test_654_zzipdir_zap_CVE_2017_5976(self):
    """ run unzzip-mix -l $(CVE_2017_5976).zip  """
    tmpdir = "tmp.test_654"
    filename = self.zip_CVE_2017_5976
    file_url = self.url_CVE_2017_5976
    testdir(tmpdir)
    trycopy("tmp.test_653", filename, tmpdir)
    download(file_url, filename, tmpdir)
    exe = self.bins("unzzip")
    run = shell("{exe} -l {tmpdir}/{filename} ".format(**locals()),
        returncodes = [0, 255])
    self.assertLess(len(run.output), 30)
    self.assertLess(len(run.errors), 1)
    self.assertIn("3 test", run.output)


  def test_800_zzshowme_check_sfx(self):
    """ create an *.exe that can extract its own zip content """
    exe=self.bins("mkzip")
    exefile = "tmp.zzshowme" + exeext
    libstub = ".libs/zzipself" + exeext
    txtfile_name = readme
    txtfile = self.src(readme)
    # add the extract-stub so we have reserved the size
    run = shell("{exe} -0 -j {exefile}.zip {libstub}".format(**locals()))
    self.assertFalse(run.returncode)
    # add the actual content which may now be compressed
    run = shell("{exe} -9 -j {exefile}.zip {txtfile}".format(**locals()))
    self.assertFalse(run.returncode)
    # rename .zip to .exe and put the extract-stub at the start
    shutil.copy(exefile+".zip", exefile)
    setstub="./zzipsetstub" + exeext
    run = shell("{setstub} {exefile} {libstub}".format(**locals()))
    self.assertFalse(run.returncode)
    os.chmod(exefile, 0755)
    # now ask the new .exe to show some of its own content
    run = shell("./{exefile} {txtfile_name}".format(**locals()))
    self.assertFalse(run.returncode)
    txt = open(txtfile).read()
    self.assertEqual(txt.split("\n"), run.output.split("\n"))
    
  def test_900_make_test1w_zip(self):
    """ create a test1w.zip using zzip/write functions. """
    exe=self.bins("zzip")
    run = shell("{exe} --version".format(**locals()))
    if "- NO -" in run.output:
        self.skipTest("- NO -D_ZZIP_ENABLE_WRITE")
        return
    zipfile="test1w.zip"
    tmpdir="test1w.tmp"
    exe=self.bins("zzip")
    for i in [1,2,3,4,5,6,7,8,9]:
       filename = os.path.join(tmpdir,"file.%i" % i)
       filetext = "file-%i\n" % i
       self.mkfile(filename, filetext)
    filename = os.path.join(tmpdir,"README")
    filetext = self.readme()
    self.mkfile(filename, filetext)
    try: os.remove(zipfile)
    except: pass
    shell("../{exe} ../{zipfile} ??*.* README".format(**locals()), cwd=tmpdir)
    self.assertGreater(os.path.getsize(zipfile), 10)




if __name__ == "__main__":
  import optparse
  _o = optparse.OptionParser("%prog [options] test_xxx")
  _o.add_option("-b", "--topsrcdir", metavar="DIR", default=topsrcdir,
    help="path to the top srcdir / unpack directory [%default]")
  _o.add_option("-t", "--testdatadir", metavar="DIR", default=testdatadir,
    help="path where temporary testdata is created [%default]")
  _o.add_option("-Z", "--mkzip", metavar="EXE", default=mkzip,
    help="name or path to zip.exe for *.zip creation [%default]")
  _o.add_option("-U", "--unzip", metavar="EXE", default=unzip,
    help="name or path to unzip.exe to unpack *.zip [%default]")
  _o.add_option("-E", "--exeext", metavar="EXT", default=exeext,
    help="the executable extension (automake $(EXEEXT)) [%default]")
  _o.add_option("--xmlresults", action="store_true", default=False,
    help="print output in junit xml testresult format [%default]")
  _o.add_option("-v", "--verbose", action="count", default=0,
    help="increase logging output [%default]")
  opt, args = _o.parse_args()
  logging.basicConfig(level = logging.WARNING - 10 * opt.verbose)
  topsrcdir = opt.topsrcdir
  testdatdir = opt.testdatadir
  mkzip = opt.mkzip
  unzip = opt.unzip
  exeext = opt.exeext
  if not args: args += [ "test_" ]
  suite = unittest.TestSuite()
  for arg in args:
    for classname in sorted(list(globals())):
      if not classname.endswith("Test"):
        continue
      testclass = globals()[classname]
      for method in sorted(dir(testclass)):
        if "*" not in arg: arg += "*"
        if arg.startswith("_"): arg = arg[1:]
        if matches(method, arg):
          suite.addTest(testclass(method))
  # TextTestRunner(verbosity=opt.verbose).run(suite)
  if opt.xmlresults:
    import xmlrunner
    Runner = xmlrunner.XMLTestRunner
    Runner(xmlresults).run(suite)
  else:
    Runner = unittest.TextTestRunner
    Runner(verbosity=opt.verbose).run(suite)
 
