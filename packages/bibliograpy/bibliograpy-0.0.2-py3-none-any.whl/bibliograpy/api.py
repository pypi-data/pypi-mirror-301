"""Bibliograpy API module."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, repr=False)
class Reference:
    """A bibliography reference."""
    key: str
    title: str

    def to_source_bib(self):
        """Serialization of the reference in processed python code."""
        return f"{self.key.upper()} = {type(self).__name__}(key='{self.key}', title='{self.title}')"

    def to_pydoc(self):
        """Serialization of the reference in docstring."""
        return f"{self.title} [{self.key}]"

    @classmethod
    def from_dict(cls, source: dict):
        """Builds a Configuration from a configuration dict."""
        return cls(
            key=source['key'],
            title=source['title'])


@dataclass(frozen=True)
class ReferenceBuilder:
    """A builder of reference decorators."""

    reference_wrapper: Callable[[list[Reference]], str]

    @staticmethod
    def _default_lambda(refs: list[Reference]) -> str:

        if len(refs) == 1:
            return f"\n\nBibliography: {refs[0].to_pydoc()}\n"

        result = "\n\nBibliography:\n\n"
        for r in refs:
            result += f"* {r.to_pydoc()}\n"
        return result

    @staticmethod
    def default():
        """The default reference decorator"""
        return ReferenceBuilder(reference_wrapper=ReferenceBuilder._default_lambda)

    def __call__(self, *refs):
        """The reference decorator."""

        def internal(obj):
            if len(refs) == 1:
                ref0 = refs[0]
                if isinstance(ref0, Reference):
                    obj.__doc__ += self.reference_wrapper([ref0])
                elif isinstance(ref0, list):
                    obj.__doc__ += self.reference_wrapper(ref0)
            else:
                obj.__doc__ += self.reference_wrapper([*refs])
            return obj

        return internal

reference = ReferenceBuilder.default()

_bibtex_com = reference(Reference(key='bibtex_com', title='www.bibtex.com'))

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Article(Reference):
    """any article published in a periodical like a journal article or magazine article"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Book(Reference):
    """a book"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Booklet(Reference):
    """like a book but without a designated publisher"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Conference(Reference):
    """a conference paper"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Inbook(Reference):
    """a section or chapter in a book"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Incollection(Reference):
    """an article in a collection"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Inproceedings(Reference):
    """a conference paper (same as the conference entry type)"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Manual(Reference):
    """a technical manual"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Masterthesis(Reference):
    """a Masters thesis"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Misc(Reference):
    """used if nothing else fits"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Phdthesis(Reference):
    """a PhD thesis"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Proceedings(Reference):
    """the whole conference proceedings"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class TechReport(Reference):
    """a technical report, government report or white paper"""

@_bibtex_com
@dataclass(frozen=True, repr=False)
class Unpublished(Reference):
    """a work that has not yet been officially published"""
