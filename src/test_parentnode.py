import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        # 1 with tag none
        child_node2 = LeafNode(None, "Text with a tag of none")
        parent_node2 = ParentNode("div", [child_node2])
        self.assertEqual(parent_node2.to_html(), "<div>Text with a tag of none</div>")

        # 1 with tag ""
        child_node3 = LeafNode("", "Text with a blank tag")
        parent_node3 = ParentNode("span", [child_node3])
        self.assertEqual(parent_node3.to_html(), "<span>Text with a blank tag</span>")

        # 1 with no value as None or ""
        child_node4 = LeafNode("p", "")
        parent_node4 = ParentNode("section", [child_node4])
        self.assertRaises(ValueError)
        child_node5 = LeafNode("div", None)
        parent_node5 = ParentNode("article", [child_node5])
        self.assertRaises(ValueError)

        # 1 with props
        child_node6 = LeafNode("h1", "Heading with Props!", {"font-style": "italics", "font-weight": "800"})
        parent_node6 = ParentNode("main", [child_node6])
        self.assertEqual(
            parent_node6.to_html(),
            '<main><h1 font-style="italics" font-weight="800">Heading with Props!</h1></main>'
        )

    def test_to_html_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        # 1 grandchild with tag none
        grandchild_node2 = LeafNode(None, "Text with a tag of none!")
        child_node2 = ParentNode("p", [grandchild_node2])
        parent_node2 = ParentNode("div", [child_node2])
        self.assertEqual(parent_node2.to_html(), "<div><p>Text with a tag of none!</p></div>")

        # 1 grandchild with tag ""
        grandchild_node3 = LeafNode("", "Grandchild plain text")
        child_node3 = ParentNode("div", [grandchild_node3])
        parent_node3 = ParentNode("span", [child_node3])
        self.assertEqual(parent_node3.to_html(), "<span><div>Grandchild plain text</div></span>")

        # 1 grandchild with no value as None or ""
        grandchild_node4 = LeafNode("p", "")
        child_node4 = ParentNode("p", [grandchild_node4])
        parent_node4 = ParentNode("section", [child_node4])
        self.assertRaises(ValueError)
        grandchild_node5 = LeafNode("a", None)
        child_node5 = ParentNode("div", [grandchild_node5])
        parent_node5 = ParentNode("article", [child_node5])
        self.assertRaises(ValueError)

        # 1 grandchild with parent props
        grandchild_node6 = LeafNode("h1", "Bold Heading 1")
        child_node6 = ParentNode("b", [grandchild_node6], {"font-style": "italics", "font-weight": "800"})
        parent_node6 = ParentNode("main", [child_node6])
        self.assertEqual(
            parent_node6.to_html(),
            '<main><b font-style="italics" font-weight="800"><h1>Bold Heading 1</h1></b></main>'
        )

        # 1 grandchild and child with props
        grandchild_node7 = LeafNode("a", "This is a link heading", {"color": "grey"})
        child_node7 = ParentNode("h1", [grandchild_node7], {"font-style": "italics", "font-weight": "800"})
        parent_node7 = ParentNode("main", [child_node7])
        self.assertEqual(
            parent_node7.to_html(),
            '<main><h1 font-style="italics" font-weight="800"><a color="grey">This is a link heading</a></h1></main>'
        )

if __name__ == "__main__":
    unittest.main()
