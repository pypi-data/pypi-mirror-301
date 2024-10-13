#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PySimpleINI (c) by chacha
#
# PySimpleINI  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""Main PySimpleINI module.

///note
Contain the first level user accessible methods.
///
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from pathlib import Path

from .document import DocumentParser, DocumentFormater
from .walker import Walker
from .sections import Section, SectionBase
from .keys import Key
from .exceptions import SectionNotFoundError, KeyNotFoundError

if TYPE_CHECKING:  # pragma: no cover  # Only imports the below statements during type checking
    from typing import List, Optional


class PySimpleINI(DocumentParser, DocumentFormater):
    """Main user class"""

    def __init__(self, filepath: Optional[Path | str] = None, bForceAlwaysOutputArrays: bool = False, bStrict: bool = False) -> None:
        """Create a new PySimpleINI object.

        This is the object representing an INI file.

        Args:
            filepath: INI file path
            bForceAlwaysOutputArrays: Force API to always return an array even with one single Key/Section
            bStrict: raise exception if unsupported formated line found
        """
        super().__init__(bStrict)
        self._bForceAlwaysOutputArrays: bool = bForceAlwaysOutputArrays

        self._filepath: Optional[Path] = None
        if isinstance(filepath, (str, Path)):
            self._filepath = Path(filepath)
            self.parsefile(self._filepath)

    @property
    def filepath(self) -> Optional[Path]:
        """filepath getter

        Returns:
            the current filepath
        """
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: Optional[Path | str]) -> None:
        """Change / Set the INI file path.

        ///example
        Use this method to save your (possibly modified) INI file elsewhere.
        ///

        Args:
            filepath: The (new) file path
        """

        if isinstance(filepath, (str, Path)):
            self._filepath = Path(filepath)

    def parsefile(self, filepath: Optional[Path | str]) -> PySimpleINI:
        """Parse a file.

        Args:
            filepath: path of the file to parse
        Returns:
            self for convinience
        """
        self._filepath = None
        if isinstance(filepath, (str, Path)):
            self._filepath = Path(filepath)
            with open(self._filepath, encoding="utf-8") as file:
                self.parse(file.read())
        return self

    def writefile(self, bBeautify: bool = False, bWipeComments: bool = False) -> None:
        """Actually write the INI object to the file.

        Args:
            bBeautify: enable beautify mode (more spaces and newlines)
            bWipeComments: do not write comments
        """
        if isinstance(self._filepath, Path):
            with open(self._filepath, "w", encoding="utf-8") as file:
                file.write(self.format(bBeautify, bWipeComments))

    def getallkeynames(self, sectionName: str) -> list[str]:
        """Get a list of Keys in a defined Section.

        ///Note
        An exception will be raised if the Key or Section isn't found.
        ///

        ///Note
        All section with given name will be considered.
        ///

        Args:
            sectionName: The Section name
        Returns:
            list of Keys names
        """
        result = []

        walker = Walker[SectionBase](targetname=sectionName, targettypes=Section)
        walker.walk(self.sections, lambda x: result.extend(x.getallkeynames()))

        return result

    def delkey(self, sectionName: str, keyName: str) -> int:
        """Delete an existing Key from Section.

        ///warning
        An exception will be raised if the Key or Section isn't found.
        ///

        ///Note
        All section with given name will be considered.
        ///

        Args:
            sectionName: The Section name
            keyName: The Key name
        Returns:
            Number of deleted keys
        """
        return self.delkey_ex(sectionName, keyName, None, None)

    def delkey_ex(self, sectionName: str, keyName: str, index: Optional[int] = None, value: Optional[str] = None) -> int:
        """Delete an existing Key from Section.

        - If value is set, this filter will be applied.
        - If index is set, this filter will be applied.
        - Both filter can be enabled together (value appyed first)

        ///warning
        An exception will be raised if the Key or Section isn't found.
        ///

        ///Note
        index only apply to keys index, not to section. All section with given name will be considered.
        ///

        Args:
            sectionName: The Section name
            keyName: The Key name
            index: The Key instance index (in case of multiple Key with same name)
            value: The Key value to delete (in case of multiple Key with same name)
        Returns:
            Number of deleted keys
        """

        walkersection = Walker[SectionBase](targetname=sectionName, targettypes=Section)

        class CallbackWalkerSection:
            """temporary class to wrap ndeleted"""

            ndeleted: int = 0

            @classmethod
            def callbackwalker(cls, section):
                """Walker callback"""
                try:
                    cls.ndeleted = cls.ndeleted + section.delkey(keyName, index, value)
                except KeyNotFoundError:
                    pass

        walkersection.walk(self.sections, CallbackWalkerSection.callbackwalker)

        if CallbackWalkerSection.ndeleted == 0:
            raise KeyNotFoundError()

        return CallbackWalkerSection.ndeleted

    def getkey(self, sectionName: str, keyName: str) -> Key | List[Key]:
        """Get one or more Key from Section.

        ///warning
        An exception will be raised if the Key or Section isn't found.
        ///

        ///Note
        All section with given name will be considered.
        ///

        Args:
            sectionName: The Section name
            keyName: The Key name
        Returns:
            Found Keys
        """
        return self.getkey_ex(sectionName, keyName, None, None)

    def getkey_ex(self, sectionName: str, keyName: str, index: Optional[int] = None, value: Optional[str] = None) -> Key | List[Key]:
        """Get one or more Key from Section (Extended).

        - If value is set, this filter will be applied.
        - If index is set, this filter will be applied.
        - Both filter can be enabled together (value appyed first)

        ///warning
        An exception will be raised if the Key or Section isn't found.
        ///

        ///Note
        index only apply to keys index, not to section. All section with given name will be considered.
        ///

        ///Note
        If this Lib is not initialized with bForceAlwaysOutputArrays set,
        this function will output a single object on single match (not a list).
        ///

        Args:
            sectionName: The Section name
            keyName: The Key name
            index: The Key instance index (in case of multiple Key with same name)
            value: The Key value to delete (in case of multiple Key with same name)
        Returns:
            Found Keys
        """

        walkersection = Walker[SectionBase](targetname=sectionName, targettypes=Section)

        class CallbackWalkerSection:
            """temporary class to wrap result"""

            result: List[Key] = []
            bForceAlwaysOutputArrays: bool = self._bForceAlwaysOutputArrays

            @classmethod
            def callbackwalker(cls, section):
                """Walker callback"""
                try:
                    keys = section.getkey_ex(keyName, index, value, cls.bForceAlwaysOutputArrays)
                    if isinstance(keys, Key):
                        cls.result.append(keys)
                    else:  # array
                        cls.result.extend(keys)
                except KeyNotFoundError:
                    pass

        walkersection.walk(self.sections, CallbackWalkerSection.callbackwalker)

        if len(CallbackWalkerSection.result) == 0:
            raise KeyNotFoundError()

        if len(CallbackWalkerSection.result) == 1 and (not self._bForceAlwaysOutputArrays):
            return CallbackWalkerSection.result[0]
        return CallbackWalkerSection.result

    def getkeyvalue(self, sectionName: str, keyName: str) -> str | list[str]:
        """Get one or more Key's values from Section.

        ///warning
        An exception will be raised if the Key or Section isn't found.
        ///

        ///Note
        All section with given name will be considered.
        ///

        Args:
            sectionName: The Section name
            keyName: The Key name
        Returns:
            Found Key's values
        """
        return self.getkeyvalue_ex(sectionName, keyName, None, None)

    def getkeyvalue_ex(self, sectionName: str, keyName: str, index: Optional[int] = None, value: Optional[str] = None) -> str | list[str]:
        """Get one or more Key's values from Section (Extended).

        - If value is set, this filter will be applied.
        - If index is set, this filter will be applied.
        - Both filter can be enabled together (value appyed first)

        ///warning
        An exception will be raised if the Key or Section isn't found.
        ///

        ///Note
        index only apply to keys index, not to section. All section with given name will be considered.
        ///

        Args:
            sectionName: The Section name
            keyName: The Key name
            index: The Key instance index (in case of multiple Key with same name)
            value: The Key value to delete (in case of multiple Key with same name)
        Returns:
            Found Key's values
        """

        keys: Key | List[Key] = self.getkey_ex(sectionName, keyName, index, value)
        if isinstance(keys, Key):
            return keys.getvalue()
        return [_.getvalue() for _ in keys]

    def setaddkeyvalue(
        self, sectionName: str, keyName: str, keyValue: str, bForceAddKey: bool = False, bForceAddSection: bool = False
    ) -> None:
        """Set or Add a new key with value.

        ///warning
        In case of multiple section with the same name, only the last one will be considered.
        ///

        Args:
            sectionName: The Section name
            keyName: Key's name
            keyValue: Key's value
            bForceAddKey: Force to add a new Key, even if the name already exists
            bForceAddSection: Force to add a new Section, even if the name already exists
        """
        sections: List[Section]
        if bForceAddSection is True:
            sections = [self.addsection(sectionName)]
        else:
            try:
                sections = self.getsection(sectionName)
            except SectionNotFoundError:
                sections = [self.addsection(sectionName)]

        sections[-1].setaddkeyvalue(keyName, keyValue, bForceAddKey)
