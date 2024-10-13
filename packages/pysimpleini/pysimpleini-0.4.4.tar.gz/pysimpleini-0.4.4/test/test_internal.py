from pprint import pprint
from pathlib import Path

import unittest

import sys
import io
import os
from pathlib import Path
import glob

from src.pysimpleini import PySimpleINI

from src.pysimpleini import (
    PySimpleINIBaseError,
    KeyNotFoundError,
    SectionNotFoundError,
    WrongFormatError,
)


testdir_path = Path(__file__).parent.resolve()


class Test_PySimpleINI_base(unittest.TestCase):
    def setUp(self):
        # remove any file in tmp dir, except .keep
        [
            Path(f).unlink()
            for f in list(set(glob.glob(str(testdir_path / "tmp" / "*"))) - set(glob.glob(str(testdir_path / "tmp" / ".keep"))))
        ]
        print("======================")

    def test_simpleread_value(self):
        testini = PySimpleINI(testdir_path / "testfiles/test_simpleread.ini")
        self.assertEqual(testini.getkeyvalue("testsection", "key1"), "test")
        self.assertEqual(testini.getkeyvalue("testsection", "key2"), "2")
        self.assertEqual(testini.getkeyvalue("testsection", "key3"), "43")
        self.assertEqual(testini.getkeyvalue("testsection", "key4"), "0.54")

    def test_simpleread_value__bForceAlwaysOutputArrays(self):
        testini = PySimpleINI(testdir_path / "testfiles/test_simpleread.ini", True)
        self.assertEqual(testini.getkeyvalue("testsection", "key1"), ["test"])
        self.assertEqual(testini.getkeyvalue("testsection", "key2"), ["2"])
        self.assertEqual(testini.getkeyvalue("testsection", "key3"), ["43"])
        self.assertEqual(testini.getkeyvalue("testsection", "key4"), ["0.54"])

    def test_complexread1_value(self):
        testini = PySimpleINI(testdir_path / "testfiles/test_complexread1.ini")
        self.assertEqual(testini.getkeyvalue("testsection1", "key1"), "test1")
        self.assertEqual(testini.getkeyvalue("testsection1", "key2"), "test2")
        self.assertEqual(testini.getkeyvalue("testsection1", "key3"), "test3")
        self.assertEqual(testini.getkeyvalue("testsection1", "key4"), "test4")

        self.assertEqual(testini.getkeyvalue("testsection2", "key1"), "test1")
        self.assertEqual(testini.getkeyvalue("testsection2", "key2"), ["test2", "test3"])
        self.assertEqual(testini.getkeyvalue("testsection2", "keya"), "0")

        self.assertEqual(testini.getkeyvalue("test section 4", "test key two"), "test value two")

    def test_simpleread_section_comment(self):
        testini = PySimpleINI(testdir_path / "testfiles/test_comment.ini")
        self.assertEqual(testini.getkeyvalue("testsection1", "key1"), "test1")
        testini.filepath = testdir_path / "tmp/out3.ini"
        testini.writefile(False)
        testinitmp = PySimpleINI(testdir_path / "tmp/out3.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection1", "key1"), "test1")

        print("==============")
        print(io.open(testdir_path / "testfiles/test_comment.ini").read())
        print("==============")
        print(io.open(testdir_path / "tmp/out3.ini").read())
        print("==============")

        self.assertListEqual(list(io.open(testdir_path / "testfiles/test_comment.ini")), list(io.open(testdir_path / "tmp/out3.ini")))

    def test_complexread1_value__bForceAlwaysOutputArrays(self):
        testini = PySimpleINI(testdir_path / "testfiles/test_complexread1.ini", True)
        self.assertEqual(testini.getkeyvalue("testsection1", "key1"), ["test1"])
        self.assertEqual(testini.getkeyvalue("testsection1", "key2"), ["test2"])
        self.assertEqual(testini.getkeyvalue("testsection1", "key3"), ["test3"])
        self.assertEqual(testini.getkeyvalue("testsection1", "key4"), ["test4"])

        self.assertEqual(testini.getkeyvalue("testsection2", "key1"), ["test1"])
        self.assertEqual(testini.getkeyvalue("testsection2", "key2"), ["test2", "test3"])
        self.assertEqual(testini.getkeyvalue("testsection2", "keya"), ["0"])

        self.assertEqual(testini.getkeyvalue("test section 4", "test key two"), ["test value two"])

    def test_complexreadwrite_value(self):
        testini = PySimpleINI(testdir_path / "testfiles/test_complexreadwrite.ini")
        self.assertEqual(testini.getkeyvalue("testsection", "key"), ["test1", "test2", "test3"])
        testini.filepath = testdir_path / "tmp/out.ini"
        testini.writefile(False)
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection", "key"), ["test1", "test2", "test3"])

        testini.setaddkeyvalue("testsection", "key", "test4", True)
        testini.filepath = testdir_path / "tmp/out2.ini"
        testini.writefile(False)
        testinitmp = PySimpleINI(testdir_path / "tmp/out2.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection", "key"), ["test1", "test2", "test3", "test4"])

        testini.setaddkeyvalue("testsection", "key", "test4", True, True)
        testini.filepath = testdir_path / "tmp/out3.ini"
        testini.writefile(True)
        testinitmp = PySimpleINI(testdir_path / "tmp/out3.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection", "key"), ["test1", "test2", "test3", "test4", "test4"])

    def test_deletekey(self):
        # create copy of the file
        testini = PySimpleINI(testdir_path / "testfiles/test_deleteKey.ini")
        testini.filepath = testdir_path / "tmp/out.ini"
        testini.writefile(False)

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        section = testinitmp.getsection("testsection2")
        section[0].delkey("key1")
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        with self.assertRaises(KeyNotFoundError):
            testinitmp.getkeyvalue("testsection2", "key1")

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        section = testinitmp.getsection("testsection2")
        section[0].delkey("key2", 2)
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection2", "key2"), ["test2", "test3"])

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        section = testinitmp.getsection("testsection2")
        section[0].delkey("key2", None, "test3")
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection2", "key2"), "test2")

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        section = testinitmp.getsection("testsection1")
        with self.assertRaises(KeyNotFoundError):
            section[0].delkey("key2", 1, "test2")

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        section = testinitmp.getsection("testsection1")
        section[0].delkey("key2", 1, "test3")
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection1", "key2"), "test2")

    def test_deletesection(self):
        # create copy of the file
        testini = PySimpleINI(testdir_path / "testfiles/test_deleteSection.ini")
        testini.filepath = testdir_path / "tmp/out.ini"
        testini.writefile(False)

        # remove a section
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.delsection("testsection1")
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        with self.assertRaises(SectionNotFoundError):
            testinitmp.getsection("testsection1")

        # remove a section
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.delsection("testsection2", 1)
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.getsection("testsection2")

        # remove a section
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.delsection("testsection2", 0)
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        with self.assertRaises(SectionNotFoundError):
            testinitmp.getsection("testsection2")

        # remove a section
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        with self.assertRaises(SectionNotFoundError):
            testinitmp.delsection("testsection2", 0)

    def test_deletekey_fromfile(self):

        # create copy of the file
        testini = PySimpleINI(testdir_path / "testfiles/test_deleteSection.ini")
        testini.filepath = testdir_path / "tmp/out.ini"
        testini.writefile(False)

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.delkey("testsection2", "key1")
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        with self.assertRaises(KeyNotFoundError):
            testinitmp.getkeyvalue("testsection2", "key1")

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.delkey_ex("testsection2", "key2", 2)
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection2", "key2"), ["test2", "test3"])

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.delkey_ex("testsection2", "key2", None, "test3")
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection2", "key2"), "test2")

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        with self.assertRaises(KeyNotFoundError):
            testinitmp.delkey_ex("testsection1", "key2", 1, "test2")

        # create copy of the file
        testini = PySimpleINI(testdir_path / "testfiles/test_deleteSection.ini")
        testini.filepath = testdir_path / "tmp/out.ini"
        testini.writefile(False)

        # remove an item
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        testinitmp.delkey_ex("testsection1", "key2", 1, "test3")
        testinitmp.writefile(True)
        # verify
        testinitmp = PySimpleINI(testdir_path / "tmp/out.ini")
        self.assertEqual(testinitmp.getkeyvalue("testsection1", "key2"), "test2")

    def test_strict_mode(self):
        with self.assertRaises(WrongFormatError):
            PySimpleINI(testdir_path / "testfiles/test_strict.ini", False, True)

        PySimpleINI(testdir_path / "testfiles/test_strict.ini", False, False)

    def test_samba(self):
        testini = PySimpleINI(testdir_path / "testfiles/test_smb.conf")
        testini.filepath = testdir_path / "tmp/test_smb.ini"
        testini.writefile(False, False)
        testini.filepath = testdir_path / "tmp/test_smb_wiped.ini"
        testini.writefile(False, True)
        testini = None

    def Gen_test_inputstring(self, inputstring):
        testini = PySimpleINI().parse(inputstring)
        testini.filepath = testdir_path / "tmp/out.ini"
        testini.writefile(False)
        with open(testdir_path / "tmp/out.ini") as ini_file:
            self.assertEqual(ini_file.read(), inputstring)

    def test_inputstring(self):
        inputstring = (
            "[test_section]\n"
            "testkey1=valuetestkey1\n"
            "testkey2=valuetestkey2\n"
            "testkey3=valuetestkey3.1\n"
            "testkey3=valuetestkey3.2\n"
        )
        self.Gen_test_inputstring(inputstring)

    def test_inputForeighKeys(self):
        inputstring = "testkey1=valuetestkey1\n" "testkey2=valuetestkey2\n" "testkey3=valuetestkey3.1\n" "testkey3=valuetestkey3.2\n"
        self.Gen_test_inputstring(inputstring)

    def test_doc_usage(self):
        inputstring = "[testsection]\n" "key1=test1\n" "key2=test2\n" "key3=test3\n" "key3=test31\n" "[testsection2]\n" "key10=test10\n"
        myini = PySimpleINI().parse(inputstring)
        print(myini.getkeyvalue("testsection", "key1"))
        print(myini.getkeyvalue("testsection", "key2"))
        print(myini.getkeyvalue("testsection", "key3"))
        print(myini.getkeyvalue_ex("testsection", "key3", 0))
        print(myini.getkeyvalue_ex("testsection", "key3", 1))
        print(myini.getallkeynames("testsection"))
        print(myini.getallsectionnames())
        myini.setaddkeyvalue("testsection2", "key11", "test11")
        print(myini.format())
        myini.setaddkeyvalue("testsection2", "key11", "test13")
        print(myini.format())
        myini.setaddkeyvalue("testsection2", "key11", "test14", True)
        print(myini.format())
        myini.addsection("testsection3")
        print(myini.format())
