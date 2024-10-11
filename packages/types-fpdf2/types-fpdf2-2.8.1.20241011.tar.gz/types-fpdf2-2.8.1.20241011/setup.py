from setuptools import setup

name = "types-fpdf2"
description = "Typing stubs for fpdf2"
long_description = '''
## Typing stubs for fpdf2

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`fpdf2`](https://github.com/PyFPDF/fpdf2) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`fpdf2`.

This version of `types-fpdf2` aims to provide accurate annotations
for `fpdf2==2.8.1`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/fpdf2. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`17d2e5a862aba2df0566fef1c3bfbb67df2a6dbb`](https://github.com/python/typeshed/commit/17d2e5a862aba2df0566fef1c3bfbb67df2a6dbb) and was tested
with mypy 1.11.2, pyright 1.1.383, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="2.8.1.20241011",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/fpdf2.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['Pillow>=10.3.0'],
      packages=['fpdf-stubs'],
      package_data={'fpdf-stubs': ['__init__.pyi', '_fonttools_shims.pyi', 'actions.pyi', 'annotations.pyi', 'bidi.pyi', 'deprecation.pyi', 'drawing.pyi', 'encryption.pyi', 'enums.pyi', 'errors.pyi', 'fonts.pyi', 'fpdf.pyi', 'graphics_state.pyi', 'html.pyi', 'image_datastructures.pyi', 'image_parsing.pyi', 'line_break.pyi', 'linearization.pyi', 'outline.pyi', 'output.pyi', 'prefs.pyi', 'recorder.pyi', 'sign.pyi', 'structure_tree.pyi', 'svg.pyi', 'syntax.pyi', 'table.pyi', 'template.pyi', 'text_region.pyi', 'transitions.pyi', 'unicode_script.pyi', 'util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
