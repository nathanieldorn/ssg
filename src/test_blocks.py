import unittest
from blocks import BlockType, block_to_block_type

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

        test_blocks_code = [
            "```Code as one line```",
            "```Code as multiline\nsecond line```"
        ]
        #test valid single and multi line code
        for block in test_blocks_code:
            self.assertEqual(block_to_block_type(block), BlockType.CODE)

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
