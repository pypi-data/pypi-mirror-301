#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PySimpleINI (c) by chacha
#
# PySimpleINI  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""CLI interface module"""
from __future__ import annotations
from typing import cast

from argparse import ArgumentParser, RawTextHelpFormatter
from os import linesep
import sys
from pathlib import Path

from . import __Summuary__, __Name__, PySimpleINI


class CLI:
    """CLI interface definition"""

    def __init__(self) -> None:
        """CLI interface initialization"""
        self.parser: ArgumentParser = ArgumentParser(description=__Summuary__, prog=__Name__, formatter_class=RawTextHelpFormatter)
        self.parser.add_argument("-f", "--file", type=Path, help="INI file to parse", required=True)
        self.parser.add_argument("-of", "--output-file", type=Path, help="Output INI file (in place if not set)")
        self.parser.add_argument("--beautify", help="output a prettier ini file", action="store_true", default=False)
        self.parser.add_argument("--wipe-comments", help="wipe all comments", action="store_true", default=False)
        self.parser.add_argument("--strict", help="do not ignore line with non-parsable content", action="store_true", default=False)
        self.createsubparsers()

        self.args = self.parser.parse_args(sys.argv)

        self.inifile: PySimpleINI = PySimpleINI(self.args.file, True, self.args.strict)

        self.args.func()

    def createsubparsers(self) -> None:
        """create subparsers"""
        self.subparsers = self.parser.add_subparsers(help="command to be executed")

        subparsers_list = []

        parser_getkeyvalue = self.subparsers.add_parser("getkeyvalue", help="getkeyvalue help")
        parser_getkeyvalue.set_defaults(func=self.cmd_getkeyvalue)
        subparsers_list.append(parser_getkeyvalue)
        parser_getkeyvalue.add_argument("sectionName", type=str)
        parser_getkeyvalue.add_argument("keyName", type=str)
        parser_getkeyvalue.add_argument("--index", type=int, action="store", default=None)
        parser_getkeyvalue.add_argument("--value", type=str, action="store", default=None)

        parser_setaddkeyvalue = self.subparsers.add_parser("setaddkeyvalue", help="setaddkeyvalue help")
        parser_setaddkeyvalue.set_defaults(func=self.cmd_setaddkeyvalue)
        subparsers_list.append(parser_setaddkeyvalue)
        parser_setaddkeyvalue.add_argument("sectionName", type=str)
        parser_setaddkeyvalue.add_argument("keyName", type=str)
        parser_setaddkeyvalue.add_argument("keyValue", type=str)
        parser_setaddkeyvalue.add_argument("--force-add-key", action="store_true", default=False)
        parser_setaddkeyvalue.add_argument("--force-add-section", action="store_true", default=False)

        parser_delkey = self.subparsers.add_parser("delkey", help="delkey help")
        parser_delkey.set_defaults(func=self.cmd_delkey)
        subparsers_list.append(parser_delkey)
        parser_delkey.add_argument("sectionName", type=str)
        parser_delkey.add_argument("keyName", type=str)
        parser_delkey.add_argument("--index", type=int, action="store", default=None)
        parser_delkey.add_argument("--value", type=str, action="store", default=None)

        parser_getallkeynames = self.subparsers.add_parser("getallkeynames", help="getallkeynames help")
        parser_getallkeynames.set_defaults(func=self.cmd_getallkeynames)
        subparsers_list.append(parser_getallkeynames)
        parser_getallkeynames.add_argument("sectionName", type=str)

        parser_getallsectionnames = self.subparsers.add_parser("getallsectionnames", help="getallsectionnames help")
        parser_getallsectionnames.set_defaults(func=self.cmd_getallsectionnames)
        subparsers_list.append(parser_getallsectionnames)

        parser_rewrite = self.subparsers.add_parser("rewrite", help="rewrite help")
        parser_rewrite.set_defaults(func=self.cmd_rewrite)
        subparsers_list.append(parser_rewrite)

        parser_delsection = self.subparsers.add_parser("delsection", help="delsection help")
        parser_delsection.set_defaults(func=self.cmd_delsection)
        subparsers_list.append(parser_delsection)
        parser_delsection.add_argument("sectionName", type=str)
        parser_delsection.add_argument("--index", type=int, action="store", default=None)

        self.parser.epilog = "commands usage:" + linesep
        for subparser in subparsers_list:
            self.parser.epilog = self.parser.epilog + subparser.format_usage()

    def writefile(self) -> None:
        """write file helper"""
        if self.args.output_file:
            self.inifile.filepath = self.args.output_file
        self.inifile.writefile(self.args.beautify, self.args.wipe_comments)

    def cmd_getkeyvalue(self) -> None:
        """getkeyvalue cmd implementation"""
        res: list[str] = cast(
            list[str], self.inifile.getkeyvalue_ex(self.args.sectionName, self.args.keyName, self.args.index, self.args.value)
        )
        print(linesep.join(res))

    def cmd_setaddkeyvalue(self) -> None:
        """setaddkeyvalue cmd implementation"""
        self.inifile.setaddkeyvalue(
            self.args.sectionName, self.args.keyName, self.args.keyValue, self.args.force_add_key, self.args.force_add_section
        )
        self.writefile()

    def cmd_delkey(self) -> None:
        """delkey cmd implementation"""
        self.inifile.delkey_ex(self.args.sectionName, self.args.keyName, self.args.index, self.args.value)
        self.writefile()

    def cmd_getallkeynames(self) -> None:
        """getallkeynames cmd implementation"""
        res: list[str] = cast(list[str], self.inifile.getallkeynames(self.args.sectionName))
        print(linesep.join(res))

    def cmd_getallsectionnames(self) -> None:
        """getallsectionnames cmd implementation"""
        res: list[str] = cast(list[str], self.inifile.getallsectionnames())
        print(linesep.join(res))

    def cmd_rewrite(self) -> None:
        """rewrite cmd implementation"""
        self.writefile()

    def cmd_delsection(self) -> None:
        """delsection cmd implementation"""
        self.inifile.delsection(self.args.sectionName, self.args.index)
        self.writefile()

if __name__=="__main__":
    CLI()
