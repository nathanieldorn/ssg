from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=0, props=None):
        super().__init__(tag, value, children, props)
        self.tag = tag
        self.value = value
        self.props = props
        self.children = 0 #revisit this method of default

    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None or self.tag == "":
            return f"{self.value}"
        return f"<{self.tag}>{self.value}</{self.tag}>"
