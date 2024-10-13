# pysimpleini (c) by chacha
#
# pysimpleini  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""
Main module __init__ file.
"""

from importlib.metadata import distribution, version, PackageNotFoundError
import warnings

try:  # pragma: no cover
    __version__ = version("pysimpleini")
except PackageNotFoundError:  # pragma: no cover
    warnings.warn("can not read __version__, assuming local test context, setting it to ?.?.?")
    __version__ = "?.?.?"

try:  # pragma: no cover
    dist = distribution("pysimpleini")
    __Summuary__ = dist.metadata["Summary"]
except PackageNotFoundError:  # pragma: no cover
    warnings.warn('can not read dist.metadata["Summary"], assuming local test context, setting it to <pysimpleini description>')
    __Summuary__ = "pysimpleini description"

try:  # pragma: no cover
    dist = distribution("pysimpleini")
    __Name__ = dist.metadata["Name"]
except PackageNotFoundError:  # pragma: no cover
    warnings.warn('can not read dist.metadata["Name"], assuming local test context, setting it to <pysimpleini>')
    __Name__ = "pysimpleini"

from .exceptions import (
    PySimpleINIBaseError,
    KeyNotFoundError,
    SectionNotFoundError,
    WrongFormatError,
)

from .keys import KeyBase, KeyBlanck, KeyComment, Key

from .sections import (
    SectionBase,
    SectionBlanck,
    SectionComment,
    Section,
    SectionRoot,
)

from .simpleini import PySimpleINI

from .__main__ import CLI


