import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

# raw Markdown -> TextNode's list
def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_link(nodes) 
    nodes = split_nodes_image(nodes) 
    return nodes

# TextNode -> HTMLNode(LeafNode)
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, 
                            {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", 'image', {"src": text_node.url,
                                        "alt": text_node.text })


# TextNode.TEXT(with inline blocks) -> TextNode(without inline blocks) 
def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception("split_nodes_delimiter: Invalid Markdown syntax")


        for i, section in enumerate(sections):
            if not section:
                continue

            if i % 2 != 0:
                new_nodes.append(TextNode(sections[i], text_type))
            else:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))

    return new_nodes



# takes Markdown, return a list of tuples
# each tuple contain alt text and url
def extract_markdown_images(text):
    # ![Description of image](url/of/image.jpg) 
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches


# takes Markdown, return a list of tuples
# each tuple contain anchor text and url
def extract_markdown_links(text):
    # [link](https://www.google.com).
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches


#split raw markdown text into TextNodes based on images 
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text) 

        if not images:
            new_nodes.append(node)
            continue

        splited = node.text

        for anchor, link in images:
            splited = splited.split(f"![{anchor}]({link})", 1)

            if len(splited) != 2:
                raise Exception('Error spliting')

            if splited[0]:
                new_nodes.append(TextNode(splited[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.IMAGE, link))

            splited = splited[1]

        if splited:
            new_nodes.append(TextNode(splited, TextType.TEXT))

    return new_nodes
            

            
        


#split raw markdown text into TextNodes based on links. 
def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text) 

        if not links:
            new_nodes.append(node)
            continue

        splited = node.text

        for alt, link in links:
            splited = splited.split(f"[{alt}]({link})", 1)
            if len(splited) != 2:
                raise Exception('Error spliting')
            if splited[0]:
                new_nodes.append(TextNode(splited[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))

            splited = splited[1]

        if splited:
            new_nodes.append(TextNode(splited, TextType.TEXT))

    return new_nodes




