#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PySimpleINI (c) by chacha
#
# PySimpleINI  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""Document PySimpleINI module.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from re import search as RE_search

from .walker import Walker
from .exceptions import SectionNotFoundError

from .sections import (
    SectionBase,
    Section,
    SectionRoot,
    SectionBlanck,
    SectionComment,
)

from .exceptions import WrongFormatError

if TYPE_CHECKING:  # pragma: no cover  # Only imports the below statements during type checking
    from typing import List, Optional


class Document:
    """Document description class

    Attributes:
        sectioncomment_tags: supported comments tags
    """

    sectioncomment_tags: List[str] = [";", "#"]

    def __init__(self) -> None:
        self._sections: List[SectionBase] = []

    @property
    def sections(self):
        """sections getter"""
        return self._sections

    def reset_sections(self):
        """reset sections list"""
        self._sections = []

    def addsection(self, name: str) -> Section:
        """Create and Add a new Section.

        Args:
            name: The new section name
        Returns:
            The new section
        """
        section = Section(name, -1)
        self.sections.append(section)
        return section

    def addcommentsection(self, value: str) -> SectionComment:
        """Create and Add a new Comment Section.

        Args:
            value: Comment value
        Returns:
            The new section
        """
        section = SectionComment(-1)
        section.append_commentkey(self.sectioncomment_tags[0], value, -1)
        self.sections.append(section)
        return section

    def addblanksection(self) -> SectionBlanck:
        """Create and Add a new Blank Section (newline).

        Returns:
            The new section
        """
        section = SectionBlanck(-1)
        section.append_blanckkey(-1)
        self.sections.append(section)
        return section

    def delsection(self, sectionName: str, index: Optional[int] = None) -> int:
        """Delete an existing Section.

        - If index is set, this filter will be applied.

        ///warning
        An exception will be raised if the Section isn't found.
        ///

        Args:
            sectionName:     The Section name
            index:    The Section instance index (in case of multiple section with same name)
        Returns:
            Number of deleted sections
        """

        walker = Walker[SectionBase](targetname=sectionName, targetindex=index, targettypes=Section)
        walker.walk(self.sections, self.sections.remove)
        ndeleted: int = walker.num_matched

        if ndeleted == 0:
            raise SectionNotFoundError()

        return ndeleted

    def getallsectionnames(self) -> list[str]:
        """Retrieve a list of sections names.

        Returns:
            List of section names.
        """
        result = []

        walker = Walker[SectionBase](targettypes=Section)
        walker.walk(self.sections, lambda x: result.append(x.getname()))

        return result

    def getsection(self, name: str, index: Optional[int] = None) -> list[Section]:
        """Get one or more sections objects.

        ///Note
        An exception will be raised if the Section isn't found.
        ///

        Args:
            name: Name of the section to retrieve.
            index:    The Section instance index (in case of multiple section with same name)
        Returns:
            The section object or a list of section object
        """

        result: List[Section] = []

        walker = Walker[SectionBase](targetname=name, targetindex=index, targettypes=Section)
        walker.walk(self.sections, result.append)

        if len(result) == 0:
            raise SectionNotFoundError()

        return result


class DocumentParser(Document):
    """Document Parser class"""

    def __init__(self, bStrict: bool = False) -> None:
        super().__init__()
        self._lastsection: Optional[Section] = None
        self._bStrict: bool = bStrict

    def parse(self, raw: str) -> Document:
        """Parse a raw test.

        Args:
            raw: text to parse
        Returns:
            self for convinience
        """
        self.reset_sections()
        self._lastsection = None

        lineIndex: int = 0
        for _line in raw.splitlines():
            lineIndex = lineIndex + 1
            self._parseline(_line, lineIndex)

        return self

    def _getlatestsection(self) -> Section:
        if self._lastsection is None:
            self._lastsection = SectionRoot()
            self.sections.append(self._lastsection)
        return self._lastsection

    def _insertblanckline(self, line_number: int) -> None:
        latestsection = self._getlatestsection()
        if isinstance(latestsection, SectionRoot):
            section = SectionBlanck(line_number)
            section.append_blanckkey(line_number)
            self.sections.append(section)
        else:
            latestsection.append_blanckkey(line_number)

    def _insertsectionline(self, name: str, line_number: int) -> None:
        self._lastsection = Section(name, line_number)
        self.sections.append(self._lastsection)

    def _insertkeyline(self, name: str, value: str, line_number: int) -> None:
        latestsection = self._getlatestsection()
        latestsection.append_key(name, value, line_number)

    def _insertcommentline(self, delimiter: str, value: str, line_number: int) -> None:
        latestsection = self._getlatestsection()
        if isinstance(latestsection, SectionRoot):
            section = SectionComment(line_number)
            section.append_commentkey(delimiter, value, line_number)
            self.sections.append(section)
        else:
            latestsection.append_commentkey(delimiter, value, line_number)

    def _parseline(self, raw_line: str, line_number: int) -> None:
        """Internal function that parse one line.

        Args:
            raw_line: the raw line string
            line_number: the line number in the data-set
        """
        if RE_search(r"^\s*$", raw_line):
            self._insertblanckline(line_number)
            return

        if result := RE_search(r"^\s*\[(?P<section_name>.*)\]\s*$", raw_line):
            self._insertsectionline(result.group("section_name").strip(), line_number)
            return

        if result := RE_search(r"^\s*(?P<key_name>[^=]*)=(?P<key_value>.*)", raw_line):
            self._insertkeyline(result.group("key_name").strip(), result.group("key_value").strip(), line_number)
            return

        for _commentpatern in self.sectioncomment_tags:
            if result := RE_search(rf"^\s*{_commentpatern}(?P<section_comment>.*)", raw_line):
                self._insertcommentline(_commentpatern, result.group("section_comment").strip(), line_number)
                return

        if self._bStrict is True:
            raise WrongFormatError(f"Found on line: {line_number}")


class DocumentFormater(Document):
    """Document formater class"""

    def format(self, bBeautify: bool = False, bWipeComments: bool = False) -> str:
        """Generate the full formated output.

        Args:
            bBeautify: enable space arround '='
            bWipeComments: do not write comments
        Returns:
            formated string
        """
        result = ""
        for section in self.sections:
            if isinstance(section, Section):
                _result = section.formatall(bBeautify, bWipeComments)
                if _result:
                    if bBeautify is True:
                        _result = _result + "\n"
                result = result + _result
            elif isinstance(section, SectionComment) and (bWipeComments is False):
                _result = section.formatall()
                if _result:
                    if bBeautify is True:
                        _result = _result + "\n"
                result = result + _result
            elif isinstance(section, SectionBlanck) and (bBeautify is False):
                result = result + "\n"

        return result
