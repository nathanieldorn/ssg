import unittest

from imglinkextractor import extract_markdown_images, extract_markdown_links

class TestExtracor(unittest.TestCase):

    def test_image_extract(self):
        # test with good sample
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        #test with bad sample, misplaced ! identifier
        matches2 = extract_markdown_images(
            "This is another text with a ! [picture](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual(0, len(matches2))

        #test with bad sample, no alt text
        self.assertRaises(Exception, lambda: extract_markdown_images(
            "A sample without alt text ![](https://i.imgur.com/zjjcJKZ.png)"
            )
        )

        #test with bad sample, no img url
        self.assertRaises(Exception, lambda: extract_markdown_images(
            "A sample without a url ![No URL]()"
            )
        )


    def test_link_extract(self):
        matches = extract_markdown_links(
            "This is text with a [hyperlink](https://www.boot.dev)"
        )
        self.assertListEqual([("hyperlink", "https://www.boot.dev")], matches)

        #test with bad sample, no anchor text
        self.assertRaises(Exception, lambda: extract_markdown_links(
             "A sample without anchor text [](https://www.boot.dev)"
             )
         )

        #test with bad sample, no url
        self.assertRaises(Exception, lambda: extract_markdown_links(
             "A sample without a url [No URL]()"
             )
         )
