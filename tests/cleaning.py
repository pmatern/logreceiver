import unittest
from views.logreceive import remove_dots_from_keys

class TestCleaning(unittest.TestCase):

    def test_fix_keys(self):
        log_entry = {}
        log_entry["blah"] = "meh"
        log_entry["foo.bar"] = "fleuh"
        sub_entry = {}
        sub_entry["a"] = "2"
        sub_entry["b.n"] = "54y"
        log_entry["sub"] = sub_entry

        remove_dots_from_keys(log_entry)


        self.assertTrue("foo_bar" in log_entry)
        self.assertEqual("fleuh", log_entry["foo_bar"])
        self.assertTrue("sub" in log_entry)
        self.assertTrue("b_n" in log_entry["sub"])
        self.assertEqual("54y", log_entry["sub"]["b_n"])

if __name__ == '__main__':
    unittest.main()

