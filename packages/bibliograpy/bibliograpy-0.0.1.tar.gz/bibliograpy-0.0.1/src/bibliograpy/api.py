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

@dataclass(frozen=True, repr=False)
class Institution(Reference):
    """A reference to an institution."""

@dataclass(frozen=True, repr=False)
class TechReport(Reference):
    """A reference to a tech report."""
    institution: Institution | None = None

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
