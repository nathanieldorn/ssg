import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):

    def test_split(self):

        test_nodes_good = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("Here's a node with **BOLD** text",TextType.TEXT),
            TextNode("An example ending in `code`", TextType.TEXT),
            TextNode("_Italics_ are last but not least", TextType.TEXT)
        ]

        test_nodes_bad = [
            TextNode("This is a bad `code block string", TextType.TEXT),
            TextNode("This one is just normal text", TextType.TEXT),
            TextNode("**BAD bold formatting on this one", TextType.TEXT),
            TextNode("Here are bad italics_", TextType.TEXT)

        ]

        expected_code_results = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]

        expected_code_results2 = [
            TextNode("An example ending in ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]

        expected_bold_results = [
            TextNode("Here's a node with ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]

        expected_italics_results = [
            TextNode("Italics", TextType.ITALIC),
            TextNode(" are last but not least", TextType.TEXT)
        ]

        #test first valid code sample
        nodes_code = split_nodes_delimiter([test_nodes_good[0]], "`", TextType.CODE)
        self.assertListEqual(nodes_code, expected_code_results)

        #test first valid bold sample
        nodes_bold = split_nodes_delimiter([test_nodes_good[1]], "**", TextType.BOLD)
        self.assertListEqual(nodes_bold, expected_bold_results)

        #test second valid code sample
        nodes_code2 = split_nodes_delimiter([test_nodes_good[2]], "`", TextType.CODE)
        self.assertListEqual(nodes_code2, expected_code_results2)

        #test first italic sample
        nodes_italic = split_nodes_delimiter([test_nodes_good[3]], "_", TextType.ITALIC)
        self.assertListEqual(nodes_italic, expected_italics_results)

        #test bad code sample
        self.assertRaises(Exception, lambda: split_nodes_delimiter([test_nodes_bad[0]], "`", TextType.CODE))

        #test normal sample (no formatting)
        bad_nodes_text = split_nodes_delimiter([test_nodes_bad[1]], None, TextType.TEXT)
        self.assertEqual(bad_nodes_text[0], TextNode("This one is just normal text", TextType.TEXT, None))

        #test bad bold sample
        self.assertRaises(Exception, lambda: split_nodes_delimiter([test_nodes_bad[2]], "`", TextType.CODE))

        #test bad italic sample
        self.assertRaises(Exception, lambda: split_nodes_delimiter([test_nodes_bad[3]], "`", TextType.CODE))

        #test non-text nodes pass through with correct and incorrect parameters
        non_text_node = [TextNode("This is some code", TextType.CODE)]
        self.assertEqual(split_nodes_delimiter(non_text_node, "`", TextType.CODE), non_text_node)
        self.assertEqual(split_nodes_delimiter(non_text_node, None, TextType.LINK), non_text_node)

if __name__ == "__main__":
    unittest.main()
