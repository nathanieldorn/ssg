import unittest

from page import extract_title

class TestPages(unittest.TestCase):

    def test_md_heading_extract(self):

        heading = extract_title("../ssg/src/sample_md.md")
        self.assertEqual(heading, "This is a heading 1")
