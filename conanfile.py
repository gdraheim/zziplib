#! /usr/bin/env python3
# type: ignore
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get

class ZZipLibRecipe(ConanFile):
    # generators = "CMakeToolchain", "CMakeDeps"
    settings = "os", "compiler", "build_type", "arch"
    name = "zziplib"
    version = "0.13.79"

    def source(self) -> None:
        # Please, be aware that using the head of the branch instead of an immutable tag
        # or commit is a bad practice and not allowed by Conan
        get(self, F"https://github.com/gdraheim/zziplib/archive/refs/tags/v{self.version}.zip",
                  strip_root=True)

    def requirements(self) -> None:
        self.requires("zlib/[>=1.2.10 <1.3]")
        if self.settings.os == "Windows":  # pylint: disable=no-member
            self.requires("base64/0.4.0")

    def build_requirements(self) -> None:
        self.tool_requires("cmake/[>=3.10]") # pylint: disable=not-callable

    def layout(self) -> None:
        cmake_layout(self)

    def generate(self) -> None:
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self) -> None:
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self) -> None:
        cmake = CMake(self)
        cmake.install()

    def package_info(self) -> None:
        self.cpp_info.libs = ["zziplib"]
