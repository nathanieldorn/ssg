import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_links, text_to_textnodes

class TestSplitNodes(unittest.TestCase):

    def test_split_textnodes(self):

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
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([test_nodes_bad[1]], None, TextType.TEXT))

        #test bad bold sample
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([test_nodes_bad[2]], "**", TextType.BOLD))

        #test bad italic sample
        self.assertRaises(ValueError, lambda: split_nodes_delimiter([test_nodes_bad[3]], "_", TextType.ITALIC))

        #test non-text nodes pass through with correct and incorrect parameters
        non_text_node = [TextNode("This is some code", TextType.CODE)]
        self.assertEqual(split_nodes_delimiter(non_text_node, "`", TextType.CODE), non_text_node)
        self.assertEqual(split_nodes_delimiter(non_text_node, None, TextType.LINK), non_text_node)


    def test_split_images(self):
        #test with valid text and two images
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        #test with valid text and three images
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a third ![third image](https://i.imgur.com/test)",
            TextType.TEXT,
        )
        new_nodes2 = split_nodes_image([node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a third ", TextType.TEXT),
                TextNode("third image", TextType.IMAGES, "https://i.imgur.com/test")
            ],
            new_nodes2,
        )

        #test with valid text and one images
        node3 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes3 = split_nodes_image([node3])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes3,
        )

        #test with no image
        node4 = TextNode(
            "There's no image here",
            TextType.TEXT,
        )
        new_nodes4 = split_nodes_image([node4])
        self.assertListEqual(
            [
                TextNode("There's no image here", TextType.TEXT)
            ],
            new_nodes4,
        )

    def test_split_links(self):
        #test with valid text and two links
        node = TextNode(
            "This is text with a [hyperlink](https://i.imgur.com/zjjcJKZ.png) and a [second link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("hyperlink", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )

        #test with valid text and three links
        node2 = TextNode(
            "This is text with a [hyperlink](https://i.imgur.com/zjjcJKZ.png) and a [second link](https://www.boot.dev) and a last one [here](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes2 = split_nodes_links([node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("hyperlink", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev"
                ),
                TextNode(" and a last one ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://www.google.com")
            ],
            new_nodes2,
        )

    def test_text_to_text_node(self):

            #test valid text
            node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
            self.assertListEqual(node,
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
            )

            #test text with invalid MD syntax
            self.assertRaises(ValueError, lambda: text_to_textnodes("This is **text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))

            #test plain text only
            node2 = text_to_textnodes("Here we have nothing but plain old text")
            self.assertListEqual(node2,
                [
                    TextNode("Here we have nothing but plain old text", TextType.TEXT)
                ]
            )

            #test italic before bold
            node3 = text_to_textnodes("A new _order_ of markdown to **test**, complete with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a bit of `code` before a [link](https://www.boot.dev)")
            self.assertListEqual(node3,
                [
                    TextNode("A new ", TextType.TEXT),
                    TextNode("order", TextType.ITALIC),
                    TextNode(" of markdown to ", TextType.TEXT),
                    TextNode("test", TextType.BOLD),
                    TextNode(", complete with an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a bit of ", TextType.TEXT),
                    TextNode("code", TextType.CODE),
                    TextNode(" before a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://www.boot.dev"),
                ]
            )

            #test new norder with minimal text between
            node4 = text_to_textnodes("Word [link](https://www.google.com)![image](https://imgur.com)`code`_italic_ and **bold**")
            self.assertListEqual(node4,
                [
                    TextNode("Word ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://www.google.com"),
                    TextNode("image", TextType.IMAGES, "https://imgur.com"),
                    TextNode("code", TextType.CODE),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD)
                ]
            )

if __name__ == "__main__":
    unittest.main()
