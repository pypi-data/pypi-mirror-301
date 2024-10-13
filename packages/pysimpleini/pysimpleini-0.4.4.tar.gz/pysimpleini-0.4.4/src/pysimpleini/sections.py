#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PySimpleINI (c) by chacha
#
# PySimpleINI  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""Sections PySimpleINI module.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from abc import ABCMeta, abstractmethod

from .exceptions import KeyNotFoundError
from .walker import Walker
from .keys import KeyBase, KeyBlanck, KeyComment, Key

if TYPE_CHECKING:  # pragma: no cover  # Only imports the below statements during type checking
    from typing import List, Optional


class SectionBase(metaclass=ABCMeta):
    """Generic section base class."""

    def __init__(self, line: int) -> None:
        """create a Section Base object

        ///warning
        This object does not aim to be created
        ///

        Args:
            line: line where the key was read (-1 if generated)
        """
        self._ar_keys: List[KeyBase] = []
        self._line = line

    @property
    def keys(self):
        """keys getter"""
        return self._ar_keys

    @abstractmethod
    def format(self) -> str:
        """Output the formated Section's value.

        Example: [Section Name]

        Returns:
             formated string
        """

    def formatall(self, bBeautify: bool = False, bWipeComments: bool = False) -> str:
        """Output the full formated Section's.

        Example:
        ```console
        [Section Name]
        Key1Name = Key1Value
        Key2Name = Key2Value
        ...
        ```

        Args:
            bBeautify: enable space around '='
            bWipeComments: do not write comments
        Returns:
            formated string
        """
        result: str = ""
        for key in self.keys:
            if isinstance(key, Key):
                result = result + key.format(bBeautify) + "\n"
            elif isinstance(key, KeyComment) and (bWipeComments is False):
                result = result + key.format() + "\n"
            elif isinstance(key, KeyBlanck) and (bBeautify is False):
                result = result + "\n"
        if bBeautify is True:
            result = result + "\n"
        return result


class SectionBlanck(SectionBase):
    """Blank section class."""

    def append_blanckkey(self, line: int) -> KeyBlanck:
        """Append a blanck line to the section.

        Args:
            line: line where the key was read (-1 if generated)
        """
        key: KeyBlanck = KeyBlanck(line)
        self.keys.append(key)
        return key

    def format(self) -> str:
        """Output the formated Section's value.

        Returns:
             formated string
        """
        return ""


class SectionComment(SectionBase):
    """Comment section class."""

    def format(self) -> str:
        """Output the formated Section's value.

        Returns:
             formated string
        """
        return ""

    def append_commentkey(self, delimiter: str, value: str, line: int) -> KeyComment:
        """Append a comment key to the section.

        Args:
            delimiter: the comments delimiter
            value: Comment-line value
            line: line where the key was read (-1 if generated)
        """
        key: KeyComment = KeyComment(delimiter, value, line)
        self.keys.append(key)
        return key


class Section(SectionComment, SectionBlanck):
    """normal section class"""

    def __init__(self, name: str, line: int) -> None:
        """Create a new Section object.

        Args:
            name: Key's name
            line: line where the key was read (-1 if generated)
        """
        super().__init__(line)
        self._name: str = name

    def getname(self) -> str:
        """return section name"""
        return self._name

    def formatall(self, bBeautify: bool = False, bWipeComments: bool = False) -> str:
        """Output the full formated Section's.

        Example:
        ```console
        [Section Name]
        Key1Name = Key1Value
        Key2Name = Key2Value
        ...
        ```

        Args:
            bBeautify: enable space around '='
            bWipeComments: do not write comments
        Returns:
            formated string
        """
        # Anonymous root key case
        result = ""
        if self.getname() != "[]":
            result = self.format()
        result = result + super().formatall(bBeautify, bWipeComments)
        return result

    def format(self) -> str:
        """Output the formated Section's value.

        Example: [Section Name]

        Returns:
             formated string
        """
        return f"[{self.getname()}]\n"

    def append_key(self, name: str, value: str, line: int) -> Key:
        """Create and Add a new Key to the Section.

        Args:
            name: Name of the new Key
            value: Value of the new Key
            line: line number
        """
        key: Key = Key(name, value, line)
        self.keys.append(key)
        return key

    def getallkeynames(self) -> list[str]:
        """Return all Key names of the current Section.

        Returns:
            List of Key's name
        """
        result = []

        walker = Walker[KeyBase](targettypes=Key)
        walker.walk(self.keys, lambda x: result.append(x.getname()))

        return result

    def delkey(self, name: str, index: Optional[int] = None, value: Optional[str] = None) -> int:
        """Delete an existing Key from section.

        - If value is set, this filter will be applied.
        - If index is set, this filter will be applied.
        - Both filter can be enabled together (value appyed first)

        ///Note
        An exception will be raised if the Key isn't found.
        ///

        Args:
            name: The Key name
            index: The Key instance index (in case of multiple Key with same name)
            value: The Key value to delete (in case of multiple Key with same name)
        Returns:
            Number of deleted keys
        """

        walker = Walker[KeyBase](targetname=name, targetindex=index, targetvalue=value, targettypes=Key)
        walker.walk(self.keys, self.keys.remove)
        ndeleted: int = walker.num_matched

        if ndeleted == 0:
            raise KeyNotFoundError()

        return ndeleted

    def getkey_ex(
        self, name: str, index: Optional[int] = None, value: Optional[str] = None, bForceAlwaysOutputArrays: Optional[bool] = False
    ) -> Key | List[Key]:
        """Get one or more Key from Section (Extended).

        - If value is set, this filter will be applied.
        - If index is set, this filter will be applied.
        - Both filter can be enabled together (value appyed first)

        ///Note
        An exception will be raised if the Key isn't found.
        ///

        ///warning
        By default, this function return a single object if only one key is found.
        Use bForceAlwaysOutputArrays to force outputing array in any situation
        ///

        Args:
            name: The Key name
            index: The Key instance index (in case of multiple Key with same name)
            value: The Key value to delete (in case of multiple Key with same name)
            bForceAlwaysOutputArrays: force to output array even if only 1 element found
        Returns:
            Found Keys
        """

        result: List[Key] = []

        walker = Walker[KeyBase](targetname=name, targetindex=index, targetvalue=value, targettypes=Key)
        walker.walk(self.keys, result.append)

        if len(result) == 0:
            raise KeyNotFoundError()

        if (not bForceAlwaysOutputArrays) and (len(result) == 1):
            return result[0]

        return result

    def getkey(self, name: str) -> Key | List[Key]:
        """Get one or more Key from Section.

        An exception will be raised if the Key isn't found.

        Args:
            name: The key name
        Returns:
            Found Keys
        """
        return self.getkey_ex(name, None, None)

    def getkeyvalue_ex(self, name: str, index: Optional[int] = None, value: Optional[str] = None) -> str | list[str]:
        """Get one or more Key's values from Section (Extended).

        - If value is set, this filter will be applied.
        - If index is set, this filter will be applied.
        - Both filter can be enabled together (value appyed first)

        ///Note
        An exception will be raised if the Key isn't found.
        ///

        Args:
            name: The Key name
            index: The Key instance index (in case of multiple Key with same name)
            value: The Key value to delete (in case of multiple Key with same name)
        Returns:
            Found Key's values
        """
        result = []

        walker = Walker[KeyBase](targetname=name, targetindex=index, targetvalue=value, targettypes=Key)
        walker.walk(self.keys, lambda x: result.append(x.getvalue()))

        return result

    def getkeyvalue(self, name: str) -> str | list[str]:
        """Get one or more Key's values from Section.

        ///Note
        An exception will be raised if the Key isn't found.
        ///

        Args:
            name: The Key name
        Returns:
            Found Key's values

        """
        return self.getkeyvalue_ex(name, None, None)

    def setaddkeyvalue(self, name: str, value: str, bForceAddKey: Optional[bool] = False) -> None:
        """Set or Add a new key with value.

        Args:
            name: Key's name
            value: Key's value
            bForceAddKey: Force to add a new Key, even if the name already exists
        """
        keys: Key | List[Key]
        if bForceAddKey is True:
            keys = self.append_key(name, "", -1)
        else:
            try:
                keys = self.getkey(name)
            except KeyNotFoundError:
                keys = self.append_key(name, "", -1)

        if isinstance(keys, Key):
            keys.setvalue(value)
        elif isinstance(keys, list):  # array: in this case we set value of the last key
            keys[-1].setvalue(value)


class SectionRoot(Section):
    """Section root base class"""

    def __init__(self) -> None:
        """ini a root base class

        Args:
            bForceAlwaysOutputArrays: Force API to always return an array even with one single Key/Section
        """
        super().__init__("[]", 0)
