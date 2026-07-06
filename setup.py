"""Builds the Cython extension; all other packaging configuration is in pyproject.toml."""

import os
from pathlib import Path

import Cython.Compiler.Options
from Cython.Build import cythonize
from setuptools import Extension, setup

Cython.Compiler.Options.annotate = True

# Set to True if the library can still function when extensions fail to compile
# (e.g. slower, python fallback). Don't allow failure if cibuildwheel is running.
# allowed_to_fail = os.environ.get("CIBUILDWHEEL", "0") != "1"
allowed_to_fail = False

if os.name == "nt":  # Windows
    extra_compile_args = [
        "/O2",
    ]
else:  # UNIX-based systems
    extra_compile_args = [
        "-O3",
        "-Werror",
        "-Wno-unreachable-code-fallthrough",
        "-Wno-deprecated-declarations",
        "-Wno-parentheses-equality",
    ]
extra_compile_args.append("-UNDEBUG")  # Cython disables asserts by default.

# Relative to project root directory
include_dirs = [
    "pythontemplate/",
    "pythontemplate/_c_src",
]

c_files = [str(x) for x in Path("pythontemplate/_c_src").rglob("*.c")]

extensions = [
    Extension(
        # Your .pyx file will be available to cpython at this location.
        "pythontemplate._c_extension",
        [
            # ".c" and ".pyx" source file paths
            "pythontemplate/_c_extension.pyx",
            *c_files,
        ],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
        language="c",
        optional=allowed_to_fail,
    ),
]

setup(
    ext_modules=cythonize(extensions, include_path=include_dirs, language_level=3, annotate=True),
)
