import unittest

from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("b", "BOOOOOOLLLLDDDD", {"font-weight": "600"})
        self.assertEqual(node2.to_html(), '<b font-weight="600">BOOOOOOLLLLDDDD</b>')
        #print(node2)

        node3 = LeafNode(None, "No tag text")
        self.assertEqual(node3.to_html(), "No tag text")
        #print(node3)

        node4 = LeafNode("", "No tag text")
        self.assertEqual(node4.to_html(), "No tag text")
        #print(node4)

        node5 = LeafNode("p", "")
        self.assertRaises(ValueError)


if __name__ == "__main__":
    unittest.main()
