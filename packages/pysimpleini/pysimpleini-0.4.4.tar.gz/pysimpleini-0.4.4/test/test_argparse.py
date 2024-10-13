import unittest
from unittest import mock
from pathlib import Path
import glob
import os
from io import StringIO 
from contextlib import redirect_stdout,redirect_stderr

from src.pysimpleini import CLI


testdir_path = Path(__file__).parent.resolve()


class Test_PySimpleINI_ArgParse(unittest.TestCase):
    def tearDown(self)->None:
        self.CleanTmp()
        
    def setUp(self) -> None:
        self.CleanTmp()
        
    def CleanTmp(self) -> None:
        # */ remove any file in tmp dir, except .keep
        [
            Path(f).unlink()
            for f in list(set(glob.glob(str(testdir_path / "tmp" / "*"))) - set(glob.glob(str(testdir_path / "tmp" / ".keep"))))
        ]

    def test_addkey(self):
        srcfile = str(testdir_path  / "testfiles/test_simpleread.ini")
        ofile   = str(testdir_path  / "tmp/tmp_simpleread.ini")
        
        # 1/ Make a copy of the ini file
        self._test_copy_file(srcfile, ofile)
        
        # 2/ inject key/value in the new ini file
        with mock.patch("sys.argv" , \
        ["-f",ofile,\
         "setaddkeyvalue","testsection","NewKey","NewValue"]):
            CLI()
            
        # 3/ Check if original file wasn't modified
        self._test_read_file_gen(str(testdir_path   / "testfiles/test_simpleread.ini"))

        # 4/ Check if keys are present in sections
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
        ["-f",ofile,"getallkeynames","testsection"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual( \
                ["key1",\
                "key2", \
                "key3", \
                "key4", \
                "NewKey"] \
                , stdout.split())
            
        # 5/ Check if key value is correct
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
        ["-f",ofile,"getkeyvalue","testsection","NewKey"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual(["NewValue"], stdout.split())
        
    def test_read_file_origin(self):
        self._test_read_file_gen(str(testdir_path   / "testfiles/test_simpleread.ini"))
        
    def test_rewrite_file(self):
        self._test_copy_file(str(testdir_path       / "testfiles/test_simpleread.ini"),\
                             str(testdir_path       / "tmp/tmp_simpleread.ini"))
        self._test_read_file_gen(str(testdir_path   / "testfiles/test_simpleread.ini"))
        self._test_read_file_gen(str(testdir_path   / "tmp/tmp_simpleread.ini"))
        
    def _test_copy_file(self,src_filepath:str,dst_filepath:str):
        with mock.patch("sys.argv" , \
        ["-f",src_filepath,\
         "-of",dst_filepath,\
         "rewrite"]):
            CLI()
            
    def _test_read_file_gen(self,filepath:str):
        # 1/ Check if section is present
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
    	["-f",filepath,"getallsectionnames"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual(["testsection"], stdout.split())
            
        # 2/ Check if keys are present in sections
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
        ["-f",filepath,"getallkeynames","testsection"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual( \
                ["key1",\
                "key2", \
                "key3", \
                "key4"] \
                , stdout.split())
            
        # 3/ Check if key value is correct
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
        ["-f",filepath,"getkeyvalue","testsection","key1"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual(["test"], stdout.split())
            
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
        ["-f",filepath,"getkeyvalue","testsection","key2"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual(["2"], stdout.split())
            
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
        ["-f",filepath,"getkeyvalue","testsection","key3"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual(["43"], stdout.split())
            
        with redirect_stdout(StringIO()) as capted_stdout, \
             mock.patch("sys.argv" , \
        ["-f",filepath,"getkeyvalue","testsection","key4"]):
            CLI()
            stdout=capted_stdout.getvalue()
            self.assertEqual(["0.54"], stdout.split())