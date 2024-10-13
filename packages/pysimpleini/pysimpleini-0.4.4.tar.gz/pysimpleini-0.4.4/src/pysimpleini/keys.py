#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PySimpleINI (c) by chacha
#
# PySimpleINI  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""Keys PySimpleINI module.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod


class KeyBase(metaclass=ABCMeta):
    """Generic Key base class."""

    def __init__(self, line: int) -> None:
        """Generic Key base class.

        ///warning
        This object does not aim to be created
        ///

        Args:
            line: line where the key was read (-1 if generated)
        """
        self._line = line

    @abstractmethod
    def getvalue(self) -> str:
        """Key value getter

        Returns:
            requested value
        """

    def format(self) -> str:
        """Key value formater (renderer)

        Returns:
            requested formated value
        """
        return self.getvalue()


class KeyBlanck(KeyBase):
    """Blank Key base class."""

    def getvalue(self) -> str:
        """Key value getter

        Returns:
            requested value
        """
        return ""


class KeyValue(KeyBase):
    """Generic Key base class with a value."""

    def __init__(self, value: str, line: int):
        """Create a new Key-Comment object.

        Args:
            delimiter: the comments delimiter
            value: Comment-line value
            line: line where the key was read (-1 if generated)
        """
        super().__init__(line)
        self._value = value

    def getvalue(self) -> str:
        """Return key value

        Returns:
            requested value
        """
        return self._value


class KeyComment(KeyValue):
    """Comment Key base class"""

    def __init__(self, delimiter: str, value: str, line: int):
        """Create a new Key-Comment object.

        Args:
            delimiter: the comments delimiter
            value: Comment-line value
            line: line where the key was read (-1 if generated)
        """
        super().__init__(value, line)
        self._delimiter: str = delimiter

    def getdelimiter(self) -> str:
        """Get the delimiter.

        Returns:
            the delimiter
        """
        return self._delimiter

    def format(self) -> str:
        """Format a comment (render).

        Returns:
            rendered string
        """
        return self.getdelimiter() + self.getvalue()


class Key(KeyValue):
    """Normal key class"""

    def __init__(self, name: str, value: str, line: int):
        """Create a new Key object.

        Args:
            name: Key's name
            value: Key's value
            line: line where the key was read (-1 if generated)
        """
        super().__init__(value, line)
        self._name = name

    def getname(self) -> str:
        """Return key name

        Returns:
            requested key name
        """
        return self._name

    def setvalue(self, value: str) -> None:
        """Set key value

        Args:
            value: value to set
        """
        self._value = value

    def format(self, bBeautify: bool = False) -> str:
        """Output the formated Key's value.

        ///example
        KeyName = KeyValue
        ///

        Args:
            bBeautify: enable space arround '='
        Returns:
            formated string
        """
        if bBeautify is True:
            return f"{self.getname()} = {self.getvalue()}"
        return f"{self.getname()}={self.getvalue()}"
