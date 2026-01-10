"""
TextNode --> HMTLNode
is the representation in HTML
of the abstraction made in the TextNode
"""
# base class
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTMLNode: to_html not implemented")

    def props_to_html(self):
        if not self.props:
            return ""

        formated = "" 
        for key, value in self.props.items():
            formated += f' {key}="{value}"'
        return formated

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"



# inherits from HTMLNode, has no childrens, is used by ParentNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children})"



# inherits from HTMLNode, has childrens, they are LeafNodes, and
# uses recursion for formatting them
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a value")
        if not self.children:
            raise ValueError("ParentNode must have children")

        formated_childrens = "" 
        for child in self.children:
            formated_childrens += child.to_html()

        return f"<{self.tag}>{formated_childrens}</{self.tag}>"
    


