import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
