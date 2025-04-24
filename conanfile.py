#! /usr/bin/env python3
# type: ignore
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get
from conan.tools.gnu import PkgConfig
from conan.tools.system.package_manager import Apt, Zypper, Yum

class ZZipLibRecipe(ConanFile):
    # generators = "CMakeToolchain", "CMakeDeps"
    settings = "os", "compiler", "build_type", "arch"
    name = "zziplib"
    version = "0.13.79"
    URL = "https://github.com/gdraheim/zziplib/"
    license = "NA"


    def system_requirements(self) -> None:
        apt = Apt(self)
        apt.install(["zlib1g-dev"])
        yum = Yum(self)
        yum.install(["zlib-devel"])
        zypper = Zypper(self)
        zypper.install(["zlib-devel"])

    def package_info(self) -> None:
        zlib_config = PkgConfig(self, 'zlib')
        zlib_config.fill_cpp_info(self.cpp_info, is_system=True)
        self.output.error("LIBS:", self.cpp_info.libs)
        self.output.error("LIBS:", self.cpp_info.system_libs)

    def source(self) -> None:
        # Please, be aware that using the head of the branch instead of an immutable tag
        # or commit is a bad practice and not allowed by Conan
        get(self, F"https://github.com/gdraheim/zziplib/archive/refs/tags/v{self.version}.zip",
                  strip_root=True)

    def requirements(self) -> None:
        # self.requires("zlib/[>=1.2]")
        if self.settings.os == "Windows":  # pylint: disable=no-member
            self.requires("base64/0.4.0")
        self.output.error("REQUIRES:")

    def build_requirements(self) -> None:
        self.tool_requires("cmake/[>=3.10]") # pylint: disable=not-callable

    def layout(self) -> None:
        cmake_layout(self)

    def generate(self) -> None:
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        # tc.variables["MYVAR"] = "MYVAR_VALUE"
        tc.preprocessor_definitions["ZZIP_MANPAGES"] = "OFF"
        tc.preprocessor_definitions["ZZIP_INSTALL_BINS"] = "OFF"
        tc.preprocessor_definitions["ZZIP_TESTCVE"] = "OFF"
        tc.preprocessor_definitions["VERBOSE"] = "ON"
        tc.generate()

    def build(self) -> None:
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self) -> None:
        cmake = CMake(self)
        cmake.install()
