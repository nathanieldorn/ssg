class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        all_attr = ""
        if self.props == None:
            return ""
        else:
            for attr in self.props:
                all_attr = all_attr + (f' {attr}="{self.props[attr]}"')
            return all_attr

    def __repr__(self):
        return f"HTMLnode({self.tag}, {self.value}, {self.children}, {self.props})"
