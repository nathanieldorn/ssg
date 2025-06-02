from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        elif self.children == None:
            raise ValueError("Missing children")
        else:
            child_html = ""
            for child in self.children:
                child_html += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
