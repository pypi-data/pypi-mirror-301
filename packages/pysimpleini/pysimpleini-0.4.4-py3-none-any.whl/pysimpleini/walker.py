#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PySimpleINI (c) by chacha
#
# PySimpleINI  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""Tools module

Attributes:
    T_Elem: generic type to customize the walker
"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Generic, Protocol, runtime_checkable

from abc import abstractmethod

if TYPE_CHECKING:  # pragma: no cover  # Only imports the below statements during type checking
    from typing import Optional, Callable, List


@runtime_checkable
class ProtoGetVal(Protocol):
    """generic getvalue protocol definition"""

    @abstractmethod
    def getvalue(self) -> str:
        """generic getvalue protocol method

        Returns:
            the obj value
        """


@runtime_checkable
class ProtoGetName(Protocol):
    """generic getname protocol definition"""

    @abstractmethod
    def getname(self) -> str:
        """generic getname protocol method

        Returns:
            the obj name
        """


T_Elem = TypeVar("T_Elem")


class Walker(Generic[T_Elem]):
    """Generic walker class to search key or section in a list"""

    def __init__(self, **kwargs) -> None:
        self.targetname: Optional[str] = None
        if "targetname" in kwargs:
            self.targetname = kwargs["targetname"]

        self.targetvalue: Optional[str] = None
        if "targetvalue" in kwargs:
            self.targetvalue = kwargs["targetvalue"]

        self.targetindex: Optional[str] = None
        if "targetindex" in kwargs:
            self.targetindex = kwargs["targetindex"]

        self.targettypes: List[type[T_Elem]] = []
        if "targettypes" in kwargs:
            if isinstance(kwargs["targettypes"], list):
                self.targettypes = kwargs["targettypes"]
            else:
                self.targettypes = [kwargs["targettypes"]]

        self.index: int = 0
        self.num_matched = 0

    def reset(self) -> None:
        """Reset walker class context"""
        self.index = 0
        self.num_matched = 0

    def _checkname(self, elem: T_Elem) -> bool:
        if isinstance(elem, ProtoGetName):
            return bool((self.targetname is None) or (elem.getname() == self.targetname))
        return True

    def _checkindex(self) -> bool:
        if self.targetindex is not None:
            self.index = self.index + 1
            return bool(self.targetindex == (self.index - 1))
        return True

    def _checkvalue(self, elem: T_Elem) -> bool:
        if isinstance(elem, ProtoGetVal):
            return bool((self.targetvalue is None) or (elem.getvalue() == self.targetvalue))
        return True

    def walk(self, walklist: List[T_Elem], action: Callable) -> None:
        """walk a list using defined criteria

        Args:
            walklist: the list to walk on
            action: a callable applied to the found elements
        """
        self.reset()
        for elem in walklist:
            # checking elem type
            if len(self.targettypes) != 0:
                bFound = False
                for targettype in self.targettypes:
                    if isinstance(elem, targettype):
                        bFound = True
                        break
                if not bFound:
                    continue

            if not self._checkname(elem):
                continue

            if not self._checkindex():
                continue

            if not self._checkvalue(elem):
                continue

            action(elem)
            self.num_matched = self.num_matched + 1
            if self.targetindex is not None:
                return
