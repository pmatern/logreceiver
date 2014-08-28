# -*- coding: utf8 -*-

import unittest
from views.logreceive import parse_log_entries
import json
import struct


class TestParsing(unittest.TestCase):
    def setUp(self):
        txt = '{ "hello" : "world" }'
        self.parsed = [json.loads(txt)]
        self.wire = struct.pack("!I", len(txt)) + txt

    def test_simple_parse(self):
        self.assertEqual(self.parsed, parse_log_entries(self.wire))

    def test_double_parse(self):
        self.assertEqual(self.parsed * 2, parse_log_entries(self.wire * 2))

    # These tests are good for boundary checking, but it turns out that moving around 2-4gb chunks of memory is a little on the slower side.
    # Feel free to uncomment and run – they take ~15s each on my 2.3ghz machine.
    # def test_large_parse(self):
    #     self.assertEqual([json.loads("{}")], parse_log_entries("\x7f\xff\xff\xff{" + ' '*(2**31-3) +  "}"))
    #
    # def test_largest_parse(self):
    #     self.assertEqual([json.loads("{}")], parse_log_entries("\xff\xff\xff\xff{" + ' '*(2**32-3) +  "}"))

    def test_out_of_bounds_large(self):
        with self.assertRaises(IndexError):
            parse_log_entries('\x7f\xff\xff\xff{}')

    def test_out_of_bounds_is_unsigned(self):
        with self.assertRaises(IndexError):
            parse_log_entries('\xff\xff\xff\xff{}')

if __name__ == '__main__':
    unittest.main()
