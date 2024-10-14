from setuptools import setup

name = "types-peewee"
description = "Typing stubs for peewee"
long_description = '''
## Typing stubs for peewee

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`peewee`](https://github.com/coleifer/peewee) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`peewee`.

This version of `types-peewee` aims to provide accurate annotations
for `peewee==3.17.6`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/peewee. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`407eeaa133356862639cd92f3d98e6b9a697c1ee`](https://github.com/python/typeshed/commit/407eeaa133356862639cd92f3d98e6b9a697c1ee) and was tested
with mypy 1.11.2, pyright 1.1.383, and
pytype 2024.10.11.
'''.lstrip()

setup(name=name,
      version="3.17.6.20241014",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/peewee.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['playhouse-stubs', 'peewee-stubs'],
      package_data={'playhouse-stubs': ['__init__.pyi', 'flask_utils.pyi', 'METADATA.toml', 'py.typed'], 'peewee-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
