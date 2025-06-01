import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_print(self):
        node = HTMLNode()
        node.props = {"href": "https://www.boot.dev", "target": "_blank", "id": "test"}
        #print(node)
        #print(node.props_to_html())

        node2 = HTMLNode("p")
        #print(node2)
        #print(node2.props_to_html())

        node3 = HTMLNode()
        node3.tag, node3.value, node3.props = "h1", "Heading", {"href": "", "class": "testing", "color": "red"}
        #print(node3)
        #print(node3.props_to_html())

if __name__ == "__main__":
    unittest.main()
