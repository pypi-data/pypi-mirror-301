from setuptools import setup

name = "types-psutil"
description = "Typing stubs for psutil"
long_description = '''
## Typing stubs for psutil

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`psutil`](https://github.com/giampaolo/psutil) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`psutil`.

This version of `types-psutil` aims to provide accurate annotations
for `psutil==6.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/psutil. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`17d2e5a862aba2df0566fef1c3bfbb67df2a6dbb`](https://github.com/python/typeshed/commit/17d2e5a862aba2df0566fef1c3bfbb67df2a6dbb) and was tested
with mypy 1.11.2, pyright 1.1.383, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="6.0.0.20241011",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/psutil.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['psutil-stubs'],
      package_data={'psutil-stubs': ['__init__.pyi', '_common.pyi', '_compat.pyi', '_psaix.pyi', '_psbsd.pyi', '_pslinux.pyi', '_psosx.pyi', '_psposix.pyi', '_pssunos.pyi', '_psutil_linux.pyi', '_psutil_osx.pyi', '_psutil_posix.pyi', '_psutil_windows.pyi', '_pswindows.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
