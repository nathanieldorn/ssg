from typing_extensions import Text
import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("Some italics", TextType.ITALIC)
        node4 = TextNode("Some more italics", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

        node5 = TextNode("Some code", TextType.CODE, "https://www.boot.dev")
        node6 = TextNode("Some code", TextType.CODE)
        node7 = TextNode("Some code", TextType.TEXT, "https://www.boot.dev")
        node8 = TextNode("Some code", TextType.CODE, "https://www.boot.dev")
        node9 = TextNode("Some code", TextType.CODE, None)
        self.assertNotEqual(node5, node6)
        self.assertNotEqual(node5, node7)
        self.assertEqual(node5, node8)
        self.assertEqual(node6, node9)

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        # test node with tag and value
        node2 = TextNode("Text node in bold", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.to_html(), "<b>Text node in bold</b>")

        # test node as image
        node3 = TextNode("Alt image text", TextType.IMAGES, "https://www.boot.dev")
        html_node3 =text_node_to_html_node(node3)
        print("Test" + html_node3.props_to_html())
        self.assertEqual(html_node3.to_html(), '<img src="https://www.boot.dev" alt="Alt image text"></img>')

        # test node as link
        node4 = TextNode("A link to nowhere", TextType.LINK, "https://www.boot.dev")
        html_node4 = text_node_to_html_node(node4)
        self.assertEqual(html_node4.to_html(), '<a href="https://www.boot.dev">A link to nowhere</a>')

if __name__ == "__main__":
    unittest.main()
