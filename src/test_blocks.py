import unittest
from blocks import BlockType, block_to_block_type, markdown_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode

class BlockTypeTest(unittest.TestCase):

    def test_block_to_block_type(self):

        test_blocks_headings = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        #test valid headings 1 through 6
        for block in test_blocks_headings:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        test_block_code = "```\nCode as one line\n```"
        #test valid single and multi line code
        self.assertEqual(block_to_block_type(test_block_code), BlockType.CODE)

        test_blocks_quote = [
            ">Quote on one line",
            ">A multiline quote\n>that is oh so insightful \n>and thought provoking"
        ]
        #test valid single and multi line quotes
        for block in test_blocks_quote:
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        #test bad multi line list
        bad_quote = ">A multiline quote\n missing the second carrot"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

        test_blocks_uolists = [
            "- A one line unordered list",
            "- A multi line one\n- The second line\n- And the third"
        ]
        #test valid single and multi line lists
        for block in test_blocks_uolists:
            self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        test_blocks_olists = [
            "1. A one line ordered list",
            "1. A multi line one\n2. Second line\n3. Third line"
        ]
        #test valid single and mutli line ordered lists
        for block in test_blocks_olists:
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        test_blocks_paragraphs = [
            "Paragraph 1",
            "Paragraph 2\nParagraph 3\nParagraph 4",
            "1.Paragraph 5",
            "Paragraph 6```",
            "```Paragraph 7",
            "1. Paragraph 8\n3. Paragraph 9"
        ]

        #test blocks which should be paragraphs, either as valid paragraph or invalid other type
        for block in test_blocks_paragraphs:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_headings(self):
        mdh1 = "# Heading 1"

        mdh2 = "## Heading 2"

        nodeh1 = markdown_to_html_node(mdh1)
        html = nodeh1.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1></div>",
        )

        nodeh2 = markdown_to_html_node(mdh2)
        html = nodeh2.to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading 2</h2></div>",
        )


    def test_quotes(self):
        md = """
>Quote 1
>quote 2
>quote 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote 1 quote 2 quote 3</blockquote></div>",
        )


    def test_lists(self):
        md = """
1. List item 1
2. List item 2
3. List item 3

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>List item 1</li><li>List item 2</li><li>List item 3</li></ol></div>",
        )

        md2 = """
- Bullet 1
- Bullet 2
- Bullet 3
"""

        node2 = markdown_to_html_node(md2)
        html2 = node2.to_html()
        self.assertEqual(
            html2,
            "<div><ul><li>Bullet 1</li><li>Bullet 2</li><li>Bullet 3</li></ul></div>",
        )

        md3 = """
1. Item 1
3. Item 3
- Bullet 1
"""

        node3 = markdown_to_html_node(md3)
        html3 = node3.to_html()
        self.assertEqual(
            html3,
            "<div><p>1. Item 1 3. Item 3 - Bullet 1</p></div>",
        )
