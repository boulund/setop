#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import tempfile
import os
import subprocess

SETOP = ["./setop.py"]


def mockfile_paths(*mockfiles):
    return map(lambda mockfile: mockfile.path, mockfiles)


def sorted_output(*lines):
    return "\n".join(sorted(lines))


def call_setop(*args, input_=""):
    p = subprocess.Popen(SETOP + list(args),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    p.stdin.write(input_.encode("ascii"))
    p.stdin.close()
    p.wait()
    output = p.stdout.read().decode("ascii").rstrip("\n")
    p.stdout.close()
    return p.returncode, output


def call_setop_raw(*args, input_=b""):
    p = subprocess.Popen(SETOP + list(args),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    p.stdin.write(input_)
    p.stdin.close()
    p.wait()
    output = p.stdout.read()
    p.stdout.close()
    return p.returncode, output
    

class MockupFile:
    def __init__(self, *lines):
        self.content = "\n".join(lines)
        fp = tempfile.NamedTemporaryFile("w", delete=False)
        self.path = fp.name
        fp.write(self.content)
        fp.close()
    
    def __del__(self):
        os.remove(self.path)


class MockupFileRaw:
    def __init__(self, *lines, EOL=None):
        self.content = EOL.join(lines)
        fp = tempfile.NamedTemporaryFile("wb", delete=False)
        self.path = fp.name
        fp.write(self.content)
        fp.close()
    
    def __del__(self):
        os.remove(self.path)


class Test(unittest.TestCase):
    
    def setUp(self):
        self.a = MockupFile("foo", "bar", "baz")
        self.b = MockupFile("bar", "baz")
        self.c = MockupFile("bar", "quux")
        self.x = MockupFile("a", "a", "b", "b", "b", "c")
        self.y = MockupFile("a", "a", "a", "b", "b", "b", "b")

    def test_union(self):
        retcode, output = call_setop("-u", *mockfile_paths(self.a, self.b, self.c))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo", "bar", "baz", "quux"))
        
        retcode, output = call_setop("-u", *mockfile_paths(self.a, self.b))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo", "bar", "baz"))
        
        retcode, output = call_setop("-u", "-", *mockfile_paths(self.a, self.b),
                                     input_="spam\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo", "bar", "baz", "spam"))
        
        retcode, output = call_setop("-u")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
    
    def test_multiset_union(self):
        retcode, output = call_setop("-m", "-u", *mockfile_paths(self.a, self.b, self.c))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo", "bar", "baz", "quux"))
        
        retcode, output = call_setop("-m", "-u", *mockfile_paths(self.x, self.y))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("a", "a", "a", "b", "b", "b", "b", "c"))
        
        retcode, output = call_setop("-m", "-u")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
    
    def test_intersection(self):
        retcode, output = call_setop("-i", *mockfile_paths(self.a, self.b, self.c))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("bar"))
        
        retcode, output = call_setop("-i", *mockfile_paths(self.a, self.b))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("bar", "baz"))
        
        retcode, output = call_setop("-i", "-", *mockfile_paths(self.a, self.b),
                                     input_="spam\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
        
        retcode, output = call_setop("-i")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
    
    def test_multiset_intersection(self):
        retcode, output = call_setop("-m", "-i", *mockfile_paths(self.a, self.b, self.c))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("bar"))
        
        retcode, output = call_setop("-m", "-i", *mockfile_paths(self.x, self.y))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("a", "a", "b", "b", "b"))
        
        retcode, output = call_setop("-m", "-i", "-", *mockfile_paths(self.a, self.b),
                                     input_="spam\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
        
        retcode, output = call_setop("-m", "-i")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
    
    def test_difference(self):
        retcode, output = call_setop("-d", *mockfile_paths(self.a, self.b, self.c))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo"))
        
        retcode, output = call_setop("-d", *mockfile_paths(self.a, self.b))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo"))
        
        retcode, output = call_setop("-d", "-", *mockfile_paths(self.a, self.b),
                                     input_="spam\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("spam"))
        
        retcode, output = call_setop("-d")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
    
    def test_multiset_difference(self):
        retcode, output = call_setop("-m", "-d", *mockfile_paths(self.y, self.x))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("a", "b"))
        
        retcode, output = call_setop("-m", "-d", "-", *mockfile_paths(self.a, self.b),
                                     input_="spam\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("spam"))
        
        retcode, output = call_setop("-m", "-d")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
    
    def test_product(self):
        retcode, output = call_setop("-p", self.a.path,
                                     input_="spam\nham\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo", "bar", "baz"))
        
        retcode, output = call_setop("-p", self.a.path, "-",
                                     input_="spam\nham\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo\tspam",
                                               "foo\tham",
                                               "bar\tspam",
                                               "bar\tham",
                                               "baz\tspam",
                                               "baz\tham"))
        
        retcode, output = call_setop("-p", "-D", ":", self.a.path, "-",
                                     input_="spam\nham\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo:spam",
                                               "foo:ham",
                                               "bar:spam",
                                               "bar:ham",
                                               "baz:spam",
                                               "baz:ham"))
        
        retcode, output = call_setop("-p")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, "")
    
    def test_multiset_product(self):
        retcode, output = call_setop("-m", "-p", self.a.path, "-",
                                     input_="spam\nspam\nham\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo\tspam",
                                               "foo\tspam",
                                               "foo\tham",
                                               "bar\tspam",
                                               "bar\tspam",
                                               "bar\tham",
                                               "baz\tspam",
                                               "baz\tspam",
                                               "baz\tham"))
        
        retcode, output = call_setop("-m", "-p", self.a.path, "-",
                                     input_="spam\nham\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo\tspam",
                                               "foo\tham",
                                               "bar\tspam",
                                               "bar\tham",
                                               "baz\tspam",
                                               "baz\tham"))
        
        retcode, output = call_setop("-m", "-p", "-D", ":", self.a.path, "-",
                                     input_="spam\nham\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo:spam",
                                               "foo:ham",
                                               "bar:spam",
                                               "bar:ham",
                                               "baz:spam",
                                               "baz:ham"))
        
        retcode, output = call_setop("-m", "-p", self.a.path,
                                     input_="spam\nham\n")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo", "bar", "baz"))
        
        
    def test_multiset_sum(self):
        retcode, output = call_setop("-m", "-s", *mockfile_paths(self.x, self.y))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("a", "a", "a", "a", "a",
                                               "b", "b", "b", "b", "b", "b", "b",
                                               "c"))
        
        retcode, output = call_setop("-m", "-s", *mockfile_paths(self.y, self.x))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("a", "a", "a", "a", "a",
                                               "b", "b", "b", "b", "b", "b", "b",
                                               "c"))
        
        retcode, output = call_setop("-m", "-s", *mockfile_paths(self.a, self.b, self.c))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output("foo", "bar", "baz",
                                               "bar", "baz",
                                               "bar", "quux"))
        
        retcode, output = call_setop("-m", "-s")
        self.assertEqual(retcode, 0)
        self.assertEqual(output, sorted_output())
    
    def test_newlines(self):
        a = MockupFileRaw(b"AAA", b"BBB", b"CCC", EOL=b"\n")
        b = MockupFileRaw(b"XXX", b"YYY", EOL=b"\n")
        
        retcode, output = call_setop_raw("-p", "--newlines", "unix", "-D", ",", *mockfile_paths(a, b))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, b"AAA,XXX\nAAA,YYY\nBBB,XXX\nBBB,YYY\nCCC,XXX\nCCC,YYY\n")
        
        a = MockupFileRaw(b"AAA", b"BBB", b"CCC", EOL=b"\r\n")
        b = MockupFileRaw(b"XXX", b"YYY", EOL=b"\r\n")
        
        retcode, output = call_setop_raw("-p", "--newlines", "windows", "-D", ",", *mockfile_paths(a, b))
        self.assertEqual(retcode, 0)
        self.assertEqual(output, b"AAA,XXX\r\nAAA,YYY\r\nBBB,XXX\r\nBBB,YYY\r\nCCC,XXX\r\nCCC,YYY\r\n")
    
    def test_failure(self):
        retcode, _ = call_setop("-p", "-u")
        self.assertGreater(retcode, 0)
        
        retcode, _ = call_setop(*mockfile_paths(self.a, self.b, self.c))
        self.assertGreater(retcode, 0)
        
        retcode, _ = call_setop("-p", "-n", "not-unix-nor-windows", *mockfile_paths(self.a, self.b, self.c))
        self.assertGreater(retcode, 0)
        
        retcode, _ = call_setop("--sum", *mockfile_paths(self.a, self.b, self.c))
        self.assertGreater(retcode, 0)

if __name__ == "__main__":
    unittest.main()
