#! /usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,multiple-statements,line-too-long,too-many-lines
# pylint: disable=too-many-branches,too-many-statements,too-many-locals,too-many-arguments,too-many-positional-arguments,too-many-public-methods,no-else-return
# pylint: disable=consider-using-with,unspecified-encoding,consider-using-f-string
# pylint: disable=possibly-unused-variable,invalid-name,unused-variable,redefined-outer-name
""" Testcases for zziplib build system """

__copyright__ = "(C) Guido Draheim, all rights reserved"""
__version__ = "0.13.80"
__contact__ = "https://github.com/gdraheim/zziplib"

from typing import Union, Optional, Tuple, List, Iterator, NamedTuple, Mapping, Sequence
import subprocess
import os
import os.path
import unittest
import shutil
import inspect
import logging
import re
from collections import namedtuple
from fnmatch import fnmatchcase as fnmatch
import json
import sys

DONE = (logging.ERROR + logging.WARNING) // 2
NOTE = (logging.INFO + logging.WARNING) // 2
logging.addLevelName(DONE, "DONE")
logging.addLevelName(NOTE, "NOTE")

logg = logging.getLogger("TESTING")
_python = "/usr/bin/python"
NIX = ""
OK = True
TODO = False

SAVETO = "localhost:5000/zziplib"
IMAGES = "localhost:5000/zziplib/image"
CENTOS9 = "almalinux:9.4"
CENTOS7 = "centos:7.9.2009"
UBUNTU1 = "ubuntu:18.04"
UBUNTU2 = "ubuntu:20.04"
UBUNTU3 = "ubuntu:22.04"
UBUNTU4 = "ubuntu:24.04"
OPENSUSE5 = "opensuse/leap:15.6"
SOFTWARE = "../Software"

DOCKER_SOCKET = "/var/run/docker.sock"
DOCKER = "docker"
BUILDPROGRESS = 0
BUILDCENTOS7 = 0
KEEP = False
FORCE = False
NOCACHE = False
MAKECHECK = False
GIT = "git"

MAINDIR = os.path.dirname(sys.argv[0]) or "."
MIRROR = os.path.join(MAINDIR, "docker_mirror.py")
NONLOCAL = 0
LOCAL = 0
OLDER = 0

def decodes(text: Union[bytes, str]) -> str:
    if text is None: return None
    if isinstance(text, bytes):
        encoded = sys.getdefaultencoding()
        if encoded in ["ascii"]:
            encoded = "utf-8"
        try:
            return text.decode(encoded)
        except UnicodeDecodeError:
            return text.decode("latin-1")
    return text
def sh____(cmd: Union[str, List[str]], shell: bool = True) -> int:
    if isinstance(cmd, str):
        logg.info(": %s", cmd)
    else:
        logg.info(": %s", " ".join(["'%s'" % item for item in cmd]))
    return subprocess.check_call(cmd, shell=shell)
def sx____(cmd: Union[str, List[str]], shell: bool = True) -> int:
    if isinstance(cmd, str):
        logg.info(": %s", cmd)
    else:
        logg.info(": %s", " ".join(["'%s'" % item for item in cmd]))
    return subprocess.call(cmd, shell=shell)

class Run(NamedTuple):
    out: str
    err: str
    code: int
def sh(cmd: Union[str, List[str]], cwd: Optional[str] = None, shell: Optional[bool] = None,
       input: Optional[str] = None, env: Optional[Mapping[str, str]] = None, # pylint: disable=redefined-builtin
       returncodes: Optional[Sequence[Optional[int]]] = None) -> Run:
    env = env if env is not None else {"LANG": "C"}
    std = run(cmd, cwd, shell, input, env)
    if std.code:
        if not returncodes or std.code not in returncodes:
            raise subprocess.CalledProcessError(std.code, cmd, std.out, std.err)
    return std
def run(cmd: Union[str, List[str]], cwd: Optional[str] = None, shell: Optional[bool] = None,
        input: Optional[str] = None, env: Optional[Mapping[str, str]] = None) -> Run: # pylint: disable=redefined-builtin
    env = env if env is not None else {"LANG": "C"}
    if isinstance(cmd, str):
        logg.info(": %s", cmd)
        shell = True if shell is None else shell
    else:
        logg.info(": %s", " ".join(["'%s'" % item for item in cmd]))
        shell = False if shell is None else shell
    if input is not None:
        run = subprocess.Popen(cmd, cwd=cwd, shell=shell, env=env,  # ..
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = run.communicate(input.encode("utf-8"))
    else:
        run = subprocess.Popen(cmd, cwd=cwd, shell=shell, env=env,  # ..
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = run.communicate()
    text_out = decodes(out)
    text_err = decodes(err)
    logg.debug("stdout = %s", text_out.splitlines())
    if text_err:
        logg.debug(" stderr = %s", text_err.splitlines())
    if run.returncode:
        logg.debug(" return = %s", run.returncode)
    return Run(text_out, text_err, run.returncode)


def output(cmd: Union[str, List[str]], shell: bool = True) -> str:
    if isinstance(cmd, str):
        logg.info(": %s", cmd)
    else:
        logg.info(": %s", " ".join(["'%s'" % item for item in cmd]))
    run = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE)
    out, err = run.communicate()
    return decodes(out)
def output2(cmd: Union[str, List[str]], shell: bool = True) -> Tuple[str, int]:
    if isinstance(cmd, str):
        logg.info(": %s", cmd)
    else:
        logg.info(": %s", " ".join(["'%s'" % item for item in cmd]))
    run = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE)
    out, err = run.communicate()
    return decodes(out), run.returncode
def output3(cmd: Union[str, List[str]], shell: bool = True) -> Tuple[str, str, int]:
    if isinstance(cmd, str):
        logg.info(": %s", cmd)
    else:
        logg.info(": %s", " ".join(["'%s'" % item for item in cmd]))
    run = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = run.communicate()
    return decodes(out), decodes(err), run.returncode

BackgroundProcess = namedtuple("BackgroundProcess", ["pid", "run", "log"])
def background(cmd: List[str], shell: bool = True) -> BackgroundProcess:
    log = open(os.devnull, "wb")
    run = subprocess.Popen(cmd, shell=shell, stdout=log, stderr=log)
    pid = run.pid
    logg.info("PID %s = %s", pid, cmd)
    return BackgroundProcess(pid, run, log)


def _lines(lines: Union[str, List[str]]) -> List[str]:
    if isinstance(lines, str):
        xlines = lines.split("\n")
        if len(xlines) and xlines[-1] == "":
            xlines = xlines[:-1]
        return xlines
    return lines
def lines(text: Union[str, List[str]]) -> List[str]:
    lines = []
    for line in _lines(text):
        lines.append(line.rstrip())
    return lines
def grep(pattern: str, lines: Union[str, List[str]]) -> Iterator[str]:
    for line in _lines(lines):
        if re.search(pattern, line.rstrip()):
            yield line.rstrip()
def greps(lines: Union[str, List[str]], pattern: str) -> List[str]:
    return list(grep(pattern, lines))

def download(base_url: str, filename: str, into: str) -> None:
    if not os.path.isdir(into):
        os.makedirs(into)
    if not os.path.exists(os.path.join(into, filename)):
        sh____(F"cd {into} && wget {base_url}/{filename}")
def text_file(filename: str, content: str) -> None:
    filedir = os.path.dirname(filename)
    if not os.path.isdir(filedir):
        os.makedirs(filedir)
    f = open(filename, "w")
    if content.startswith("\n"):
        x = re.match("(?s)\n( *)", content)
        assert x is not None
        indent = x.group(1)
        for line in content[1:].split("\n"):
            if line.startswith(indent):
                line = line[len(indent):]
            f.write(line + "\n")
    else:
        f.write(content)
    f.close()
def shell_file(filename: str, content: str) -> None:
    text_file(filename, content)
    os.chmod(filename, 0o770)
def copy_file(filename: str, target: str) -> None:
    targetdir = os.path.dirname(target)
    if not os.path.isdir(targetdir):
        os.makedirs(targetdir)
    shutil.copyfile(filename, target)
def copy_tool(filename: str, target: str) -> None:
    copy_file(filename, target)
    os.chmod(target, 0o750)

def get_caller_name() -> str:
    frame = inspect.currentframe().f_back.f_back  # type: ignore[union-attr]
    return frame.f_code.co_name  # type: ignore[union-attr]
def get_caller_caller_name() -> str:
    frame = inspect.currentframe().f_back.f_back.f_back  # type: ignore[union-attr]
    return frame.f_code.co_name  # type: ignore[union-attr]
def os_path(root: Optional[str], path: str) -> str:
    if not root:
        return path
    if not path:
        return path
    while path.startswith(os.path.sep):
        path = path[1:]
    return os.path.join(root, path)
def docname(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]

def link_software(software: str, parts: str) -> None:
    software = software or "Software"
    shelf = SOFTWARE
    for part in parts.split(","):
        item = os.path.join(shelf, part)
        if os.path.isdir(item):
            for dirpath, dirnames, filenames in os.walk(item):
                basepath = dirpath.replace(shelf + "/", "")
                for filename in filenames:
                    intofile = os.path.join(software, basepath, filename)
                    fromfile = os.path.join(dirpath, filename)
                    intodir = os.path.dirname(intofile)
                    if not os.path.isdir(intodir):
                        os.makedirs(intodir)
                    if not os.path.isfile(intofile):
                        os.link(fromfile, intofile)
def unlink_software(software: str, parts: str) -> None:
    software = software or "Software"
    shelf = SOFTWARE
    for part in parts.split(","):
        item = os.path.join(shelf, part)
        if os.path.isdir(item):
            for dirpath, dirnames, filenames in os.walk(item):
                basepath = dirpath.replace(shelf + "/", "")
                for filename in filenames:
                    intofile = os.path.join(software, basepath, filename)
                    if os.path.isfile(intofile):
                        os.unlink(intofile)

class ZZiplibBuildTest(unittest.TestCase):
    def caller_testname(self) -> str:
        name = get_caller_caller_name()
        x1 = name.find("_")
        if x1 < 0: return name
        x2 = name.find("_", x1 + 1)
        if x2 < 0: return name
        return name[:x2]
    def testname(self, suffix: Optional[str] = None) -> str:
        name = self.caller_testname()
        if suffix:
            return name + "_" + suffix
        return name
    def testdir(self, testname: Optional[str] = None) -> str:
        testname = testname or self.caller_testname()
        newdir = "tmp/tmp." + testname
        if os.path.isdir(newdir):
            shutil.rmtree(newdir)
        os.makedirs(newdir)
        return newdir
    def rm_old(self, testname: Optional[str] = None) -> None:
        testname = testname or self.caller_testname()
        for subdir in ("docs/man3", "docs/html"):
            if os.path.isdir(subdir):
                logg.info("rm -rf %s", subdir)
                shutil.rmtree(subdir)
        for filename in ("tmp.local.tgz", "docs/htmpages.tar", "docs/manpages.tar", "docs/zziplib.xml", "docs/zzipmmapped.xml", "docs/zzipfseeko.xml"):
            if os.path.isfile(filename):
                logg.info("rm %s", filename)
                os.remove(filename)
    def rm_testdir(self, testname: Optional[str] = None) -> str:
        testname = testname or self.caller_testname()
        newdir = "tmp/tmp." + testname
        if os.path.isdir(newdir):
            shutil.rmtree(newdir)
        return newdir
    def makedirs(self, path: str) -> None:
        if not os.path.isdir(path):
            os.makedirs(path)
    def user(self) -> str:
        import getpass # pylint: disable=import-outside-toplevel
        return getpass.getuser()
    def ip_container(self, name: str) -> str:
        docker = DOCKER
        cmd = F"{docker} inspect {name}"
        values = output(cmd)
        values = json.loads(values)
        if not values or "NetworkSettings" not in values[0]:
            logg.critical(" %s inspect %s => %s ", docker, name, values)
        return values[0]["NetworkSettings"]["IPAddress"]  # type: ignore[index]
    def local_image(self, image: str) -> str:
        """ attach local centos-repo / opensuse-repo to docker-start enviroment.
            Effectivly when it is required to 'docker start centos:x.y' then do
            'docker start centos-repo:x.y' before and extend the original to 
            'docker start --add-host mirror...:centos-repo centos:x.y'. """
        if os.environ.get("NONLOCAL", ""):
            return image
        add_hosts = self.start_mirror(image)
        if add_hosts:
            return F"{add_hosts} {image}"
        return image
    def local_addhosts(self, dockerfile: str, extras: Optional[str] = None) -> str:
        image = ""
        for line in open(dockerfile):
            m = re.match('[Ff][Rr][Oo][Mm] *"([^"]*)"', line)
            if m:
                image = m.group(1)
                break
            m = re.match("[Ff][Rr][Oo][Mm] *(\\w[^ ]*)", line)
            if m:
                image = m.group(1).strip()
                break
        logg.debug("--\n-- '%s' FROM '%s'", dockerfile, image)
        if image:
            return self.start_mirror(image, extras)
        return ""
    def start_mirror(self, image: str, extras: Optional[str] = None) -> str:
        extras = extras or ""
        docker = DOCKER
        mirror = MIRROR
        if NONLOCAL:
            return ""
        if LOCAL:
            mirror += " --local"
        cmd = F"{mirror} start {image} --add-hosts {extras}"
        out, rc = output2(cmd)
        if LOCAL and rc:
            raise SystemError("--local docker-mirror-packages-repo not found")
        return decodes(out).strip()
    def nocache(self) -> str:
        if FORCE or NOCACHE:
            return " --no-cache"
        return ""
    def no_check(self) -> str:
        if not MAKECHECK:
            return " --build-arg=no_check=true"
        return ""
    def buildprogress(self) -> str:
        if BUILDPROGRESS:
            return " --progress=plain"
        return ""
    def pull_baseimage(self, dockerfile: str, extras: Optional[str] = None) -> str:
        image = ""
        for line in open(dockerfile):
            m = re.match('[Ff][Rr][Oo][Mm] *"([^"]*)"', line)
            if m:
                image = m.group(1)
                break
            m = re.match("[Ff][Rr][Oo][Mm] *(\\w[^ ]*)", line)
            if m:
                image = m.group(1).strip()
                break
        logg.debug("--\n-- '%s' FROM '%s'", dockerfile, image)
        if image:
            return self.pull_image(image, extras)
        return ""
    def pull_image(self, image: str, extras: Optional[str] = None) -> str:
        extras = extras or ""
        docker = DOCKER
        cmd = F"{docker} pull {image}"
        out, rc = output2(cmd)
        if rc:
            logg.error("could not pull %s", image)
        return decodes(out).strip()
    def latest(self, previous: int = 0, latest: str = "latest") -> str:
        if not previous:
            return latest
        ret = sh([GIT, "tag", "-l"])
        logg.info("ret.out = %s", ret.out)
        if previous < 0:
            return ret.out.splitlines()[previous]
        else:
            last = ret.out.splitlines()[-1]
            part = last.split(".")
            part[-1] = str(int(part[-1]) + previous)
            return ".".join(part)
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    def test_90101_docker_mirror_ubuntu1(self) -> None:
        logg.info("\n  UBUNTU1 = '%s'", UBUNTU1)
        self.start_mirror(UBUNTU1, "--update")
    def test_90102_docker_mirror_ubuntu2(self) -> None:
        logg.info("\n  UBUNTU2 = '%s'", UBUNTU2)
        self.start_mirror(UBUNTU2, "--update")
    def test_90103_docker_mirror_ubuntu3(self) -> None:
        logg.info("\n  UBUNTU3 = '%s'", UBUNTU3)
        if LOCAL:
            self.start_mirror(UBUNTU3)
        else:
            self.start_mirror(UBUNTU3, "--universe")
    def test_90104_docker_mirror_ubuntu3(self) -> None:
        logg.info("\n  UBUNTU4 = '%s'", UBUNTU4)
        self.start_mirror(UBUNTU4, "--universe")
    def test_90105_docker_mirror_opensuse5(self) -> None:
        logg.info("\n  OPENSUSE5 = '%s'", OPENSUSE5)
        self.start_mirror(OPENSUSE5)
    def test_90107_docker_mirror_centos7(self) -> None:
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        logg.info("\n  CENTOS7 = '%s'", CENTOS7)
        self.start_mirror(CENTOS7, "--epel")
    def test_90109_docker_mirror_centos9(self) -> None:
        logg.info("\n  CENTOS9 = '%s'", CENTOS9)
        self.start_mirror(CENTOS9)
    def test_90218_ubuntu18_cmake_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-cm-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90219_ubuntu18_automake_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-am-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cat /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCONFIG=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90220_ubuntu20_cmake_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu20-cm-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90221_ubuntu20_automake_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu20-am-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cat /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCONFIG=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90222_ubuntu22_cmake_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu22-cm-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90223_ubuntu22_automake_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu22-am-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cat /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCONFIG=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90224_ubuntu24_cmake_build_dockerfile(self) -> None:
        # no universe yet (in February 2024)
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-cm-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90225_ubuntu24_automake_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-am-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cat /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCONFIG=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90234_ubuntu24_conan_build_dockerfile(self) -> None:
        # no universe yet (in February 2024)
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-conan-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90235_ubuntu24_vcpkg_build_dockerfile(self) -> None:
        # no universe yet (in February 2024)
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-vcpkg-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/x86_64-linux-gnu/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()

    def test_90242_ubuntu18_cmake_32bit_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-cm32-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/i386-linux-gnu/pkgconfig/zlib.pc"  # !!
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} /src/build/zzipwrap/zzipwrap /src/test/test.zip"
        ret = run(cmd.format(**locals()))
        logg.info("[%s] ERR %s", ret.code, ret.err)
        self.assertEqual(0, ret.code)
        self.assertNotIn("largefile mismatch", ret.err)
        #
        logg.info("____________________ /external")
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON -DLARGEFILE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        ret = run(cmd.format(**locals()))
        logg.info("[%i] ERR %s", ret.code, ret.err)
        self.assertIn("undefined reference", ret.err)
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxorcat/d -e /add_exe.*zzxorcat/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxordir/d -e /add_exe.*zzxordir/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzobfuscated/d -e /add_exe.*zzobfuscated/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e s/zzxorcat// -e s/zzxordir// -e s/zzobfuscated// /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        logg.info("try again...")
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON -DLARGEFILE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        ret = run(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        logg.info("____________________ /external32")
        cmd = "{docker} exec {testname} cp -r /src/bins /external32"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external32/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i  -e /CodeCoverage/d -e /unzzip/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external32/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90243_ubuntu18_automake_32bit_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-am32-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/i386-linux-gnu/pkgconfig/zlib.pc"  # !!
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} /src/build/zzipwrap/zzipwrap /src/test/test.zip"
        ret = run(cmd.format(**locals()))
        logg.info("[%s] ERR %s", ret.code, ret.err)
        self.assertEqual(0, ret.code)
        self.assertNotIn("largefile mismatch", ret.err)
        #
        logg.info("____________________ /external")
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCONFIG=ON -DLARGEFILE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        ret = run(cmd.format(**locals()))
        logg.info("[%i] ERR %s", ret.code, ret.err)
        self.assertIn("undefined reference", ret.err)
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxorcat/d -e /add_exe.*zzxorcat/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxordir/d -e /add_exe.*zzxordir/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzobfuscated/d -e /add_exe.*zzobfuscated/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e s/zzxorcat// -e s/zzxordir// -e s/zzobfuscated// /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        logg.info("try again...")
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCONFIG=ON -DLARGEFILE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        ret = run(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        logg.info("____________________ /external32")
        cmd = "{docker} exec {testname} cp -r /src/bins /external32"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external32/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i  -e /CodeCoverage/d -e /unzzip/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external32/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && cmake .. -DFINDPKGCONFIG=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90244_ubuntu18_cmake_32bit_largefile64_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-cm3264-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/i386-linux-gnu/pkgconfig/zlib.pc"  # !!
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} /src/build/zzipwrap/zzipwrap /src/test/test.zip"
        ret = run(cmd.format(**locals()))
        logg.info("[%s] ERR %s", ret.code, ret.err)
        self.assertEqual(os.EX_SOFTWARE, ret.code)
        self.assertIn("largefile mismatch", ret.err)
        #
        logg.info("____________________ /external")
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON -DLARGEFILE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        logg.info("____________________ /external32")
        cmd = "{docker} exec {testname} cp -r /src/bins /external32"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external32/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external32/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && make VERBOSE=1'"
        ret = run(cmd.format(**locals()))
        logg.info("[%i] ERR %s", ret.code, ret.err)
        self.assertIn("undefined reference", ret.err)
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxorcat/d -e /add_exe.*zzxorcat/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxordir/d -e /add_exe.*zzxordir/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzobfuscated/d -e /add_exe.*zzobfuscated/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e s/zzxorcat// -e s/zzxordir// -e s/zzobfuscated// /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        logg.info("try again...")
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && cmake ..  -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90245_ubuntu18_automake_32bit_largefile64_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-am3264-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} dpkg -S /usr/lib/i386-linux-gnu/pkgconfig/zlib.pc"  # !!
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual("-lz", zlib.strip())
        cmd = "{docker} exec {testname} pkg-config --libs zziplib"
        zziplib = output(cmd.format(**locals()))
        logg.info("zziplib --libs = %s", zziplib)
        self.assertEqual("-L/usr/local/lib -lzzip -lz", zziplib.strip())
        #
        cmd = "{docker} exec {testname} /src/build/zzipwrap/zzipwrap /src/test/test.zip"
        ret = run(cmd.format(**locals()))
        logg.info("[%s] ERR %s", ret.code, ret.err)
        # self.assertEqual(EX_SOFTWARE, ret.code)
        # self.assertIn("largefile mismatch", ret.err)
        self.assertEqual(0, ret.code)  # automake puts the LARGEFILE_CFLAGS into all modules
        #
        logg.info("____________________ /external")
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCONFIG=ON -DLARGEFILE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        logg.info("____________________ /external32")
        cmd = "{docker} exec {testname} cp -r /src/bins /external32"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} cp -r /src/CMakeScripts /external32/"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external32/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && cmake .. -DFINDPKGCONFIG=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && make VERBOSE=1'"
        ret = run(cmd.format(**locals()))
        logg.info("[%i] ERR %s", ret.code, ret.err)
        self.assertIn("undefined reference", ret.err)
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxorcat/d -e /add_exe.*zzxorcat/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzxordir/d -e /add_exe.*zzxordir/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /target.*zzobfuscated/d -e /add_exe.*zzobfuscated/d /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e s/zzxorcat// -e s/zzxordir// -e s/zzobfuscated// /external32/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        logg.info("try again...")
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && cmake ..  -DFINDPKGCONFIG=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external32/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzdir /src/test/test.zip"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} /external32/build/zzcat /src/test/test/README"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90250_opensuse15_cmake_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-cm-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} rpm -q --whatprovides /usr/lib64/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual(zlib.strip(), "-lz")
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90251_opensuse15_cmake_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-cm-build-afl.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()

    def test_90264_windows_static_x64_dockerfile(self) -> None:
        logg.warning("     windows-static-x64 compiles fine but segfaults on linking an .exe")
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/windows-static-x64.dockerfile"
        baseimage = self.pull_baseimage(dockerfile)
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        #
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90265_windows_shared_x64_dockerfile(self) -> None:
        logg.warning("     windows-shared-x64 compiles fine but segfaults on linking an .exe")
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/windows-shared-x64.dockerfile"
        baseimage = self.pull_baseimage(dockerfile)
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        #
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90270_centos7_automake_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/centos7-am-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile, "--epel")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} rpm -q --whatprovides /usr/lib64/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual(zlib.strip(), "-lz")
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90271_centos7_cmake_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/centos7-cm-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} rpm -q --whatprovides /usr/lib64/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual(zlib.strip(), "-lz")
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake3 .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90290_almalinux9_automake_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-am-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} rpm -q --whatprovides /usr/lib64/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual(zlib.strip(), "-lz")
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90291_almalinux9_cmake_build_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-cm-build.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} rpm -q --whatprovides /usr/lib64/pkgconfig/zlib.pc"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} pkg-config --libs zlib"
        zlib = output(cmd.format(**locals()))
        self.assertEqual(zlib.strip(), "-lz")
        #
        cmd = "{docker} exec {testname} cp -r /src/bins /external"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} sed -i -e /CodeCoverage/d -e /unzzip/d /external/CMakeLists.txt"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} mkdir -v /external/build"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && cmake3 .. -DFINDPKGCMAKE=ON'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c  'cd /external/build && make VERBOSE=1'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90318_ubuntu18_cmake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-cm-sdl2.dockerfile"
        if LOCAL: self.skipTest("no universe for ubuntu:18.04 in local tests")
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90319_ubuntu18_automake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu18-am-sdl2.dockerfile"
        if LOCAL: self.skipTest("no universe for ubuntu:18.04 in local tests")
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90320_ubuntu20_cmake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu20-cm-sdl2.dockerfile"
        if LOCAL: self.skipTest("no universe for ubuntu:20.04 in local tests")
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90321_ubuntu20_automake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu20-am-sdl2.dockerfile"
        if LOCAL: self.skipTest("no universe for ubuntu:20.04 in local tests")
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90322_ubuntu22_cmake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu22-cm-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90323_ubuntu22_automake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu22-am-sdl2.dockerfile"
        if LOCAL: self.skipTest("no universe for ubuntu:22.04 in local tests")
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90324_ubuntu24_cmake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-cm-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90325_ubuntu24_automake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-am-sdl2.dockerfile"
        if LOCAL: self.skipTest("no universe for ubuntu:24.04 in local tests")
        addhosts = self.local_addhosts(dockerfile, "--universe")
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90329_ubuntu24_use_gcc09_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-use-gcc09.dockerfile"
        # addhosts = self.local_addhosts(dockerfile, "--universe")
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-9 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90330_ubuntu24_use_gcc10_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-use-gcc10.dockerfile"
        # addhosts = self.local_addhosts(dockerfile, "--universe")
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-10 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90331_ubuntu24_use_gcc11_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-use-gcc11.dockerfile"
        # addhosts = self.local_addhosts(dockerfile, "--universe")
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-11 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90332_ubuntu24_use_gcc12_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-use-gcc12.dockerfile"
        # addhosts = self.local_addhosts(dockerfile, "--universe")
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-12 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90333_ubuntu24_use_gcc13_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-use-gcc13.dockerfile"
        # addhosts = self.local_addhosts(dockerfile, "--universe")
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-13 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90334_ubuntu24_use_gcc14_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-use-gcc14.dockerfile"
        # addhosts = self.local_addhosts(dockerfile, "--universe")
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-14 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90350_opensuse15_cmake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-cm-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90357_opensuse15_cmake_use_gcc7_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-use-gcc7.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-7 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90358_opensuse15_cmake_use_gcc8_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-use-gcc8.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-8 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90359_opensuse15_cmake_use_gcc9_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-use-gcc9.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-9 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90360_opensuse15_cmake_use_gcc10_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-use-gcc10.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-10 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90361_opensuse15_cmake_use_gcc11_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-use-gcc11.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-11 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90362_opensuse15_cmake_use_gcc12_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-use-gcc12.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-12 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90363_opensuse15_cmake_use_gcc13_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-use-gcc13.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc --version'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'gcc-13 --version'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90370_centos7_automake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/centos7-am-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90390_almalinux9_automake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-am-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90371_centos7_cmake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/centos7-cm-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90391_almalinux9_cmake_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-cm-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90398_almalinux9_cmake_sdl2_previous(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-cm-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        repo = os.path.abspath(".")
        latest = self.latest(-2 - OLDER)
        cmd = "cd {testdir} && git clone --branch {latest} {repo} ."
        sh____(cmd.format(**locals()))
        if latest in ["v0.13.71", "v0.13.72"]:
            cmd = "cp testbuilds/almalinux9-cm-sdl2.dockerfile {testdir}/testbuilds/"
            sh____(cmd.format(**locals()))
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "cd {testdir} && {docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:{latest}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:{latest}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90399_almalinux9_cmake_sdl2_previous(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-cm-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        repo = os.path.abspath(".")
        latest = self.latest(-1 - OLDER)
        cmd = "cd {testdir} && git clone --branch {latest} {repo} ."
        sh____(cmd.format(**locals()))
        if latest in ["v0.13.71", "v0.13.72"]:
            cmd = "cp testbuilds/almalinux9-cm-sdl2.dockerfile {testdir}/testbuilds/"
            sh____(cmd.format(**locals()))
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "cd {testdir} && {docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:{latest}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:{latest}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90407_centos7_automake_docs_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/centos7-am-docs.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build --build-arg=no_build=true" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/zzip/types.h'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/share/doc/zziplib'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/doc/zziplib/zziplib.html'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/man/man3/zzip_opendir.3'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90417_centos7_cmake_docs_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/centos7-cm-docs.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build --build-arg=no_build=true" + self.buildprogress() + self.no_check() + self.nocache()
        build += self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/zzip/types.h'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/share/doc/zziplib'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/doc/zziplib/zziplib.html'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/man/man3/zzip_opendir.3'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90424_ubuntu24_cmake_docs_dockerfile(self) -> None:
        # no universe yet (in February 2024)
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/ubuntu24-cm-docs.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test ! -d /usr/local/include/zzip/types.h'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/share/doc/zziplib'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/doc/zziplib/zziplib.html'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/man/man3/zzip_opendir.3'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()

    def test_90450_opensuse15_ninja_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-nj-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90451_opensuse15_cm_htmpages_nonparallel_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-cm-htmpages.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build --build-arg=no_parallel=true" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        ## cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        # sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90452_opensuse15_cm_htmpages_parallel_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/opensuse15-cm-htmpages.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        ## cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/include/SDL_rwops_zzip'"
        # sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90471_centos7_cmake_sdl2_destdir_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/centos7-cm-destdir-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /new/usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /new/usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /new/usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /new/usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90491_almalinux9_cmake_sdl2_destdir_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname = self.testname()
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-cm-destdir-sdl2.dockerfile"
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build" + self.buildprogress() + self.no_check() + self.nocache()
        cmd = "{docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 60"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        cmd = "{docker} exec {testname} ls -l /new/usr/local/bin"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} find /new/usr/local/include -type f"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'ls -l /new/usr/local/lib64/libzz*'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /new/usr/local/include/SDL_rwops_zzip'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_90515_opensuse15_mk_docs_pip311_user_dockerfile(self) -> None:
        """ here pip 22 works fine for pyproject.toml - based on python3.11 (python3-pip fails)"""
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        testname = self.testname()
        dockerfile = "testbuilds/opensuse15-mk-docs-pip311-user.dockerfile"
        self.mk_docs_pipx_dockerfile(testname, dockerfile)
    @unittest.expectedFailure
    def test_90522_ubuntu24_mk_docs_pip3_user_dockerfile(self) -> None:
        """ here pip 22 finds UNKNOWN package from pyproject.toml - need atleast pip 24"""
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        testname = self.testname()
        dockerfile = "testbuilds/ubuntu22-mk-docs-pip3-user.dockerfile"
        self.mk_docs_pipx_dockerfile(testname, dockerfile)
    def test_90524_ubuntu24_mk_docs_pip3_user_dockerfile(self) -> None:
        """ runs pip 24 under python 3.12 -- good enough for pyproject.toml --use-pep517"""
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        testname = self.testname()
        dockerfile = "testbuilds/ubuntu24-mk-docs-pip3-user.dockerfile"
        self.mk_docs_pipx_dockerfile(testname, dockerfile)
    def test_90525_ubuntu24_mk_docs_pipx_dockerfile(self, testname: str = NIX, dockerfile: str = NIX) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        testname = self.testname()
        dockerfile = "testbuilds/ubuntu24-mk-docs-pip3-user.dockerfile"
        self.mk_docs_pipx_dockerfile(testname, dockerfile)
    def mk_docs_pipx_dockerfile(self, testname: str, dockerfile: str) -> None:
        self.rm_old(testname)
        self.rm_testdir(testname)
        testdir = self.testdir(testname)
        docker = DOCKER
        addhosts = self.local_addhosts(dockerfile)
        savename = docname(dockerfile)
        saveto = SAVETO
        images = IMAGES
        build = "build --build-arg=no_build=true" + self.buildprogress() + self.no_check() + self.nocache()
        build += self.nocache()
        cmd = "NO_COLOR=1 {docker} {build} . -f {dockerfile} {addhosts} --tag {images}:{testname}"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname} {images}:{testname} sleep 600"
        sh____(cmd.format(**locals()))
        #:# container = self.ip_container(testname)
        #
        cmd = "{docker} exec {testname} bash -c 'test -d /usr/local/share/doc/zziplib'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/doc/zziplib/man/zziplib.html'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname} bash -c 'test -f /usr/local/share/man/man3/zzip_opendir.3'"
        sh____(cmd.format(**locals()))
        #
        if not KEEP:
            cmd = "{docker} rm --force {testname}"
            sx____(cmd.format(**locals()))
        cmd = "{docker} rmi {saveto}/{savename}:latest"
        sx____(cmd.format(**locals()))
        cmd = "{docker} tag {images}:{testname} {saveto}/{savename}:latest"
        sh____(cmd.format(**locals()))
        cmd = "{docker} rmi {images}:{testname}"
        sx____(cmd.format(**locals()))
        self.rm_testdir(testname)
    def test_91218_ubuntu18_am_cm_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu18-am-build.dockerfile"  # make st_219
        dockerfile2 = "testbuilds/ubuntu18-cm-build.dockerfile"  # make st_218
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91220_ubuntu20_am_cm_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu20-am-build.dockerfile"  # make st_221
        dockerfile2 = "testbuilds/ubuntu20-cm-build.dockerfile"  # make st_220
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91222_ubuntu22_am_cm_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu22-am-build.dockerfile"  # make st_223
        dockerfile2 = "testbuilds/ubuntu22-cm-build.dockerfile"  # make st_222
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91224_ubuntu24_am_cm_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu24-am-build.dockerfile"  # make st_225
        dockerfile2 = "testbuilds/ubuntu24-cm-build.dockerfile"  # make st_224
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91318_ubuntu18_am_cm_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu18-am-sdl2.dockerfile"  # make st_319
        dockerfile2 = "testbuilds/ubuntu18-cm-sdl2.dockerfile"  # make st_318
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91320_ubuntu20_am_cm_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu20-am-sdl2.dockerfile"  # make st_321
        dockerfile2 = "testbuilds/ubuntu20-cm-sdl2.dockerfile"  # make st_320
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91322_ubuntu22_am_cm_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu22-am-sdl2.dockerfile"  # make st_323
        dockerfile2 = "testbuilds/ubuntu22-cm-sdl2.dockerfile"  # make st_322
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h --exclude .uuid"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91324_ubuntu24_am_cm_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu24-am-sdl2.dockerfile"  # make st_325
        dockerfile2 = "testbuilds/ubuntu24-cm-sdl2.dockerfile"  # make st_324
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91242_ubuntu18_am_cm_32bit_largefile64_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu18-am32-build.dockerfile"  # make st_243
        dockerfile2 = "testbuilds/ubuntu18-cm32-build.dockerfile"  # make st_242
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91244_ubuntu18_am_cm_32bit_largefile64_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu18-am3264-build.dockerfile"  # make st_245
        dockerfile2 = "testbuilds/ubuntu18-cm3264-build.dockerfile"  # make st_244
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        ### self.assertFalse(greps(out, "Only"))
        out_no_lib = [line for line in lines(out) if "/local/lib:" not in line]
        self.assertFalse(greps(out_no_lib, "Only"))
        logg.info("automake has renamed the largefile libs to 'libzzip-0-64.so'")
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91270_centos7_am_cm_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/centos7-am-build.dockerfile"  # make st_270
        dockerfile2 = "testbuilds/centos7-cm-build.dockerfile"  # make st_271
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91290_almalinux9_am_cm_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/almalinux9-am-build.dockerfile"  # make st_290
        dockerfile2 = "testbuilds/almalinux9-cm-build.dockerfile"  # make st_291
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91370_centos7_am_cm_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/centos7-am-sdl2.dockerfile"  # make st_370
        dockerfile2 = "testbuilds/centos7-cm-sdl2.dockerfile"  # make st_371
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91390_almalinux9_am_cm_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/almalinux9-am-sdl2.dockerfile"  # make st_390
        dockerfile2 = "testbuilds/almalinux9-cm-sdl2.dockerfile"  # make st_391
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        A = '"s:zzip-zlib-config:zlib:"'
        B = '"s:=/usr/local/:=\\${prefix}/:"'
        C1 = '"/^exec_prefix=/d"'
        C2 = '"/^datarootdir=/d"'
        C3 = '"/^datadir=/d"'
        C4 = '"/^sysconfdir=/d"'
        C5 = '"/^bindir=/d"'
        G = '"/ generated by configure /d"'
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.pc -exec sed -i -e {A} -e {B} -e {C1} -e {C2} -e {C3} -e {C4} -e {C5} -e {G} {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name zzip-zlib-config.pc -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /usr/local -name *.la -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *-0.so -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name *.cmake -exec rm -v {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'find /new/local -name cmake -prune -exec rmdir -v {item}/zziplib {item} {end}'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -uw /usr/local/include/zzip/_config.h /new/local/include/zzip/_config.h"
        sx____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local --exclude _config.h"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91407_centos7_am_cm_docs_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/centos7-am-docs.dockerfile" # 407
        dockerfile2 = "testbuilds/centos7-cm-docs.dockerfile" # 417
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname1} bash -c 'cd /usr/local/share/doc/zziplib && mv man/html .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /usr/local/share/doc/zziplib && rm -rf man'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /usr/local/share/doc/zziplib && mv html man'"
        sh____(cmd.format(**locals()))
        item = "{}"
        end = "\\;"
        cmd = "{docker} exec {testname1} diff -urw --no-dereference --brief /usr/local /new/local"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local"
        sx____(cmd.format(**locals()))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91424_ubuntu24_pip_cm_docs_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_am"
        testname2 = self.testname() + "_cm"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/ubuntu24-cm-docs.dockerfile" # 424
        dockerfile2 = "testbuilds/ubuntu24-mk-docs-pip3-user.docckerfile" # 524
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname1}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname2}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} mkdir -p /old/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /old/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname2} bash -c 'find /old/local -name aclocal -prune -exec rm -rfv {{}} \\;'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'find /old/local -name pkgconfig -prune -exec rm -rfv {{}} \\;'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'find /old/local/share/doc/zziplib -type f -maxdepth 1 -exec rm -v {{}} \\;'"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname2} bash -c 'find /old/local/share/doc -type f'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'find /usr/local/share/doc -type f'"
        sh____(cmd.format(**locals()))
        if not TODO:
            # the dockerfile does not run zzipmakedocs for zzipfseeko and zzipmapped
            cmd = "{docker} exec {testname2} bash -c 'find /old/local -name \"zzip_entry_*\" -prune -exec rm -rfv {{}} \\;'"
            sh____(cmd.format(**locals()))
            cmd = "{docker} exec {testname2} bash -c 'rm /old/local/share/doc/zziplib/man/index.html'"
            sh____(cmd.format(**locals()))
            cmd = "{docker} exec {testname2} bash -c 'rm /old/local/share/doc/zziplib/man/zzipfseeko.html'"
            sh____(cmd.format(**locals()))
            cmd = "{docker} exec {testname2} bash -c 'rm /old/local/share/doc/zziplib/man/zzipmmapped.html'"
            sh____(cmd.format(**locals()))
            cmd = "{docker} exec {testname2} bash -c 'rm /old/local/share/doc/zziplib/index.html'"
            sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        cmd = "{docker} exec {testname2} diff -urw --no-dereference --brief /old/local/share /usr/local/share"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} exec {testname2} diff -urw --no-dereference /old/local/share /usr/local/share"
        sx____(cmd.format(**locals()))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91450_opensuse_cm_or_nj_sdl2_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_cm"
        testname2 = self.testname() + "_nj"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/opensuse15-cm-sdl2.dockerfile"  # make st_350
        dockerfile2 = "testbuilds/opensuse15-nj-sdl2.dockerfile"  # make st_450
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        item = "{}"
        end = "\\;"
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91471_centos7_cm_sdl2_or_destdir_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        if not BUILDCENTOS7: self.skipTest("end of life - centos7")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_usr"
        testname2 = self.testname() + "_new"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/centos7-cm-sdl2.dockerfile"          # make st_371
        dockerfile2 = "testbuilds/centos7-cm-destdir-sdl2.dockerfile"  # make st_471
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /new/usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        DIRS = "etc lib libexec sbin games src share/info share/applications share/man/mann"
        for i in range(1, 10):
            DIRS += " share/man/man%i share/man/man%ix" % (i, i)
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && (for u in {DIRS}; do mkdir -pv $u; done)'"
        sh____(cmd.format(**locals()))
        item = "{}"
        end = "\\;"
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_91491_almalinux9_cm_sdl2_or_destdir_dockerfile(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        testname1 = self.testname() + "_usr"
        testname2 = self.testname() + "_new"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile1 = "testbuilds/almalinux9-cm-sdl2.dockerfile"          # make st_391
        dockerfile2 = "testbuilds/almalinux9-cm-destdir-sdl2.dockerfile"  # make st_491
        addhosts = self.local_addhosts(dockerfile1)
        savename1 = docname(dockerfile1)
        savename2 = docname(dockerfile2)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename2} sleep 600"
        #
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname2} bash -c 'cd /new/usr/local && tar czvf /local.tgz .'"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp {testname2}:/local.tgz tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} cp tmp.local.tgz {testname1}:/local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "rm tmp.local.tgz"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} mkdir -p /new/local"
        sh____(cmd.format(**locals()))
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && tar xzvf /local.tgz'"
        sh____(cmd.format(**locals()))
        #
        DIRS = "etc lib libexec sbin games src share/info share/applications share/man/mann lib64/bpf"
        for i in range(1, 10):
            DIRS += " share/man/man%i share/man/man%ix" % (i, i)
        cmd = "{docker} exec {testname1} bash -c 'cd /new/local && (for u in {DIRS}; do mkdir -pv $u; done)'"
        sh____(cmd.format(**locals()))
        item = "{}"
        end = "\\;"
        cmd = "{docker} exec {testname1} diff -urw --no-dereference /usr/local /new/local"
        sx____(cmd.format(**locals()))
        out = output(cmd.format(**locals()))
        if "---" in out or "Only" in out:
            logg.warning("out>>\n%s", out)
        self.assertFalse(greps(out, "---"))
        self.assertFalse(greps(out, "Only"))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_92390_almalinux9_objdump_symbols(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        latest1 = self.latest(-1 - OLDER)
        latest2 = self.latest(-2 - OLDER)
        testname1 = self.testname() + "_1"
        testname2 = self.testname() + "_2"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-cm-sdl2.dockerfile" # 391
        savename = docname(dockerfile)
        addhosts = self.local_addhosts(dockerfile)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename}:{latest1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename}:{latest2} sleep 600"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname1} bash -c 'objdump -T /usr/local/lib64/libzzipmmapped-0.so'"
        objdump1 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest1, objdump1.out)
        libzzipmmapped1 = [line.split("Base")[1].strip() for line in objdump1.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest1, sorted(libzzipmmapped1))
        #
        cmd = "{docker} exec {testname2} bash -c 'objdump -T /usr/local/lib64/libzzipmmapped-0.so'"
        objdump2 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest2, objdump2.out)
        libzzipmmapped2 = [line.split("Base")[1].strip() for line in objdump2.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest2, sorted(libzzipmmapped2))
        #
        cmd = "{docker} exec {testname1} bash -c 'objdump -T /usr/local/lib64/libzzipfseeko-0.so'"
        objdump1 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest1, objdump1.out)
        libzzipfseeko1 = [line.split("Base")[1].strip() for line in objdump1.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest1, sorted(libzzipfseeko1))
        #
        cmd = "{docker} exec {testname2} bash -c 'objdump -T /usr/local/lib64/libzzipfseeko-0.so'"
        objdump2 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest2, objdump2.out)
        libzzipfseeko2 = [line.split("Base")[1].strip() for line in objdump2.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest2, sorted(libzzipfseeko2))
        #
        cmd = "{docker} exec {testname1} bash -c 'objdump -T /usr/local/lib64/libzzip-0.so'"
        objdump1 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest1, objdump1.out)
        libzzip1 = [line.split("Base")[1].strip() for line in objdump1.out.splitlines() if "Base" in line]
        logg.info("libzzip:%s = %s", latest1, sorted(libzzip1))
        #
        cmd = "{docker} exec {testname2} bash -c 'objdump -T /usr/local/lib64/libzzip-0.so'"
        objdump2 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest2, objdump2.out)
        libzzip2 = [line.split("Base")[1].strip() for line in objdump2.out.splitlines() if "Base" in line]
        logg.info("libzzip:%s = %s", latest2, sorted(libzzip2))
        #
        extras2 = [name for name in libzzipmmapped2 if name not in libzzipmmapped1]
        extras1 = [name for name in libzzipmmapped1 if name not in libzzipmmapped2]
        logg.info("libzzipmmapped:extras:%s = %s", latest2, extras2)
        logg.info("libzzipmmapped:extras:%s = %s", latest1, extras1)
        #
        extras2 = [name for name in libzzipfseeko2 if name not in libzzipfseeko1]
        extras1 = [name for name in libzzipfseeko1 if name not in libzzipfseeko2]
        logg.info("libzzipfseeko:extras:%s = %s", latest2, extras2)
        logg.info("libzzipfseeko:extras:%s = %s", latest1, extras1)
        #
        extras2 = [name for name in libzzip2 if name not in libzzip1]
        extras1 = [name for name in libzzip1 if name not in libzzip2]
        logg.info("libzzip:extras:%s = %s", latest2, extras2)
        logg.info("libzzip:extras:%s = %s", latest1, extras1)
        extras = {"v0.13.79": ['zzip_io_size_off_t', 'zzip_filesize32'], "v0.13.72": ['zzip_pread']}
        # self.assertEqual(extras2, extras.get(latest2, []))
        self.assertEqual(extras1, extras.get(latest1, []))
        self.assertEqual(sorted(libzzip2 + extras1), sorted(libzzip1 + extras2))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()
    def test_92391_almalinux9_objdump_symbols(self) -> None:
        if not os.path.exists(DOCKER_SOCKET): self.skipTest("docker-based test")
        self.rm_old()
        self.rm_testdir()
        future1 = self.latest(+1)
        latest1 = self.latest(0)
        latest2 = self.latest(-1 - OLDER)
        testname1 = self.testname() + "_1"
        testname2 = self.testname() + "_2"
        testdir = self.testdir()
        docker = DOCKER
        dockerfile = "testbuilds/almalinux9-cm-sdl2.dockerfile" # 391
        savename = docname(dockerfile)
        addhosts = self.local_addhosts(dockerfile)
        saveto = SAVETO
        images = IMAGES
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname1} {addhosts} {saveto}/{savename}:{latest1} sleep 600"
        sh____(cmd.format(**locals()))
        cmd = "{docker} run -d --name {testname2} {addhosts} {saveto}/{savename}:{latest2} sleep 600"
        sh____(cmd.format(**locals()))
        #
        cmd = "{docker} exec {testname1} bash -c 'objdump -T /usr/local/lib64/libzzipmmapped-0.so'"
        objdump1 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest1, objdump1.out)
        libzzipmmapped1 = [line.split("Base")[1].strip() for line in objdump1.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest1, sorted(libzzipmmapped1))
        #
        cmd = "{docker} exec {testname2} bash -c 'objdump -T /usr/local/lib64/libzzipmmapped-0.so'"
        objdump2 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest2, objdump2.out)
        libzzipmmapped2 = [line.split("Base")[1].strip() for line in objdump2.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest2, sorted(libzzipmmapped2))
        #
        cmd = "{docker} exec {testname1} bash -c 'objdump -T /usr/local/lib64/libzzipfseeko-0.so'"
        objdump1 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest1, objdump1.out)
        libzzipfseeko1 = [line.split("Base")[1].strip() for line in objdump1.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest1, sorted(libzzipfseeko1))
        #
        cmd = "{docker} exec {testname2} bash -c 'objdump -T /usr/local/lib64/libzzipfseeko-0.so'"
        objdump2 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest2, objdump2.out)
        libzzipfseeko2 = [line.split("Base")[1].strip() for line in objdump2.out.splitlines() if "Base" in line]
        logg.info("libzzipfseeko:%s = %s", latest2, sorted(libzzipfseeko2))
        #
        cmd = "{docker} exec {testname1} bash -c 'objdump -T /usr/local/lib64/libzzip-0.so'"
        objdump1 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest1, objdump1.out)
        libzzip1 = [line.split("Base")[1].strip() for line in objdump1.out.splitlines() if "Base" in line]
        logg.info("libzzip:%s = %s", latest1, sorted(libzzip1))
        #
        cmd = "{docker} exec {testname2} bash -c 'objdump -T /usr/local/lib64/libzzip-0.so'"
        objdump2 = sh(cmd.format(**locals()))
        logg.debug("objdump:%s\n%s", latest2, objdump2.out)
        libzzip2 = [line.split("Base")[1].strip() for line in objdump2.out.splitlines() if "Base" in line]
        logg.info("libzzip:%s = %s", latest2, sorted(libzzip2))
        #
        extras2 = [name for name in libzzipmmapped2 if name not in libzzipmmapped1]
        extras1 = [name for name in libzzipmmapped1 if name not in libzzipmmapped2]
        logg.info("libzzipmmapped:extras:%s = %s", latest2, extras2)
        logg.info("libzzipmmapped:extras:%s = %s", latest1, extras1)
        #
        extras2 = [name for name in libzzipfseeko2 if name not in libzzipfseeko1]
        extras1 = [name for name in libzzipfseeko1 if name not in libzzipfseeko2]
        logg.info("libzzipfseeko:extras:%s = %s", latest2, extras2)
        logg.info("libzzipfseeko:extras:%s = %s", latest1, extras1)
        #
        extras2 = [name for name in libzzip2 if name not in libzzip1]
        extras1 = [name for name in libzzip1 if name not in libzzip2]
        logg.info("libzzip:extras:%s = %s", latest2, extras2)
        logg.info("libzzip:extras:%s = %s # latest", future1, extras1)
        extras = {"v0.13.79": ['zzip_io_size_off_t', 'zzip_filesize32'], "v0.13.72": ['zzip_pread']}
        # self.assertEqual(extras2, extras.get(latest2, []))
        self.assertEqual(extras1, extras.get(future1, []))
        self.assertEqual(sorted(libzzip2 + extras1), sorted(libzzip1 + extras2))
        #
        cmd = "{docker} rm --force {testname1}"
        sx____(cmd.format(**locals()))
        cmd = "{docker} rm --force {testname2}"
        sx____(cmd.format(**locals()))
        self.rm_testdir()

def run_clean() -> None:
    docker = DOCKER
    saveto = SAVETO
    pattern = docname("*.dockerfile")
    logg.log(NOTE, "  docker rmi %s/%s", saveto, pattern)
    for line in output(docker + " images --format '{{.ID}} # {{.Repository}}:{{.Tag}}'").splitlines():
        check = "* # {saveto}/{pattern}".format(**locals())
        if fnmatch(line, check):
            logg.info("  docker rmi -f %s", line)
            sh____("{docker} rmi -f {line}".format(**locals()))
def run_help() -> None:
    for line in open(__file__):
        if line.strip().startswith("def test_"):
            x, y = line.split("def test_")
            if "_" in y:
                testname, extra = y.split("_", 1)
            else:
                testname, extra = y, ""
            if "(" in extra:
                title, parameters = extra.split("(", 1)
            else:
                title = extra.rstrip()
            print(" test_{:10}: {:}".format(testname, title))
        if line.strip().startswith("def run_"):
            x, y = line.split("def run_")
            if "#" in line:
                func, extra = y.split("#")
            else:
                func, extra = y.rstrip(), ""
            testname = func.replace("()", "").replace(" None", "").rstrip()
            print(" {:10} {:}".format(testname, extra.strip()))


def main() -> int:
    global _python, GIT, BUILDPROGRESS, BUILDCENTOS7, DOCKER, MIRROR, LOCAL, NONLOCAL, OLDER, KEEP, FORCE, NOCACHE, MAKECHECK # pylint: disable=global-statement
    import optparse # pylint: disable=deprecated-module,import-outside-toplevel
    cmdline = optparse.OptionParser("%prog [options] test*",
                                    epilog=__doc__.strip().split("\n", 1)[0])
    cmdline.formatter.max_help_position = 29
    cmdline.add_option("-v", "--verbose", action="count", default=0, help="more logging")
    cmdline.add_option("-^", "--quiet", action="count", default=0, help="less logging")
    cmdline.add_option("-?", "--version", action="count", default=0, help="author info")
    cmdline.add_option("-p", "--python", metavar="EXE", default=_python,
                       help="use another python [%default]")
    cmdline.add_option("-G", "--git", metavar="EXE", default=GIT,
                       help="use another git client [%default]")
    cmdline.add_option("-D", "--docker", metavar="EXE", default=DOCKER,
                       help="use another docker execution engine [%default]")
    cmdline.add_option("-M", "--mirror", metavar="EXE", default=MIRROR,
                       help="use another docker_mirror.py script [%default]")
    cmdline.add_option("-N", "--nolocal", "--nonlocal", action="count", default=0,
                       help="disable local docker mirror [%default]")
    cmdline.add_option("-L", "--local", action="count", default=0,
                       help="fail if not local docker mirror found [%default]")
    cmdline.add_option("-o", "--older", action="count", default=0,
                       help="symbol comparis with even older version [%default]")
    cmdline.add_option("-k", "--keep", action="count", default=0,
                       help="keep docker build container [%default]")
    cmdline.add_option("-K", "--makecheck", action="count", default=0,
                       help="make checks in every testbuild [%default]")
    cmdline.add_option("--buildprogress", action="count", default=0,
                       help="show intermediate steps of build [%default]")
    cmdline.add_option("--buildcentos7", action="count", default=0,
                       help="do not skip centos7 builds [%default]")
    cmdline.add_option("-f", "--force", action="count", default=0,
                       help="force the rebuild steps [%default]")
    cmdline.add_option("-x", "--no-cache", action="count", default=0,
                       help="force docker build --no-cache [%default]")
    cmdline.add_option("-l", "--logfile", metavar="FILE", default="",
                       help="additionally save the output log to a file [%default]")
    cmdline.add_option("--failfast", action="store_true", default=False,
                       help="Stop the test run on the first error or failure.")
    cmdline.add_option("--xmlresults", metavar="FILE", default=None,
                       help="capture results as a junit xml file [%default]")
    opt, args = cmdline.parse_args()
    logging.basicConfig(level=logging.WARNING - 5 * opt.verbose + 10 * opt.quiet)
    if opt.version:
        print("version:", __version__)
        print("contact:", __contact__)
        print("authors:", __copyright__)
        return os.EX_OK
    #
    _python = opt.python
    GIT = opt.git
    BUILDPROGRESS = opt.buildprogress
    BUILDCENTOS7 = opt.buildcentos7
    DOCKER = opt.docker
    MIRROR = opt.mirror
    LOCAL = opt.local
    NONLOCAL = opt.nolocal
    OLDER = int(opt.older)
    KEEP = opt.keep
    FORCE = opt.force
    NOCACHE = opt.no_cache
    MAKECHECK = opt.makecheck
    #
    logfile = None
    if opt.logfile:
        if os.path.exists(opt.logfile):
            os.remove(opt.logfile)
        logfile = logging.FileHandler(opt.logfile)
        logfile.setFormatter(logging.Formatter("%(levelname)s:%(relativeCreated)d:%(message)s"))
        logging.getLogger().addHandler(logfile)
        logg.info("log diverted to %s", opt.logfile)
    xmlresults = None
    if opt.xmlresults:
        if os.path.exists(opt.xmlresults):
            os.remove(opt.xmlresults)
        xmlresults = open(opt.xmlresults, "w")
        logg.info("xml results into %s", opt.xmlresults)
    #
    # unittest.main()
    suite = unittest.TestSuite()
    if not args:
        args = ["test_*"]
    for arg in args:
        run_function = F"run_{arg}"
        if run_function in globals():
            globals()[run_function]()
            continue
        for classname in sorted(globals()):
            if not classname.endswith("Test"):
                continue
            testclass = globals()[classname]
            for method in sorted(dir(testclass)):
                if arg.endswith("/"):
                    arg = arg[:-1]
                if "*" not in arg:
                    arg += "*"
                if len(arg) > 2 and arg[1] == "_":
                    arg = "test" + arg[1:]
                if fnmatch(method, arg):
                    suite.addTest(testclass(method))
    # select runner
    xmlresults = None
    if opt.xmlresults:
        if os.path.exists(opt.xmlresults):
            os.remove(opt.xmlresults)
        xmlresults = open(opt.xmlresults, "wb")  # type: ignore[assignment]
        logg.info("xml results into %s", opt.xmlresults)
    if xmlresults:
        import xmlrunner  # type: ignore # pylint: disable=import-error,import-outside-toplevel
        Runner = xmlrunner.XMLTestRunner
        result = Runner(xmlresults).run(suite)
    else:
        Runner = unittest.TextTestRunner
        result = Runner(verbosity=opt.verbose, failfast=opt.failfast).run(suite)
    if not result.wasSuccessful():
        return os.EX_DATAERR
    if not KEEP and result.testsRun and args == ["test_*"]:
        run_clean()
    logg.log(DONE, "OK - ran %s tests", result.testsRun)
    return os.EX_OK

if __name__ == "__main__":
    sys.exit(main())
