#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PySimpleINI (c) by chacha
#
# PySimpleINI  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""Exceptions PySimpleINI module.
"""


class PySimpleINIBaseError(RuntimeError):
    """Generic base PySimpleINI exception class."""


class KeyNotFoundError(PySimpleINIBaseError):
    """Key not found generic exception."""


class SectionNotFoundError(PySimpleINIBaseError):
    """Section not found generic exception."""


class WrongFormatError(PySimpleINIBaseError):
    """Wrong format generic exception."""
