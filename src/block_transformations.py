from enum import Enum
import string 
from htmlnode import ParentNode, HTMLNode, LeafNode
from inline_transformations import text_to_textnodes, text_node_to_html_node 
from textnode import TextType, TextNode
class BlockType(Enum):
    PARAGRAPH = 1 
    HEADING = 2
    CODE = 3
    QUOTE = 4
    ULIST = 5
    OLIST = 6

# Markdown -> List of ParentNodes
def markdown_to_html_node(markdown):
    html = []
    blocks = markdown_to_blocks(markdown) 

    for block in blocks:
        block_type = block_to_block_type(block)
        lines = block.split('\n')

        match block_type:
            case BlockType.PARAGRAPH: 
                clean = clean_lines(lines, BlockType.PARAGRAPH)
                childrens = text_to_children([' '.join(clean)]) 
                node = ParentNode('p', childrens)
                html.append(node)

            case BlockType.HEADING: 
                line = lines[0]
                i = 0
                while i < len(line) and line[i] == '#':
                    i+= 1

                childrens = text_to_children(clean_lines(lines, BlockType.HEADING))
                node = ParentNode(f"h{i}", childrens) 
                html.append(node)
                    
            case BlockType.QUOTE: 
                cleaned = clean_lines(lines, BlockType.QUOTE)
                childrens = text_to_children([' '.join(cleaned)]) 
                node = ParentNode("blockquote", childrens)
                html.append(node)

            case BlockType.CODE:
                inner_lines = lines[1:-1]
                dedented = []
                for line in inner_lines:
                    if line.startswith("    "):
                        dedented.append(line[4:])
                    else:
                        dedented.append(line)

                cleaned = "\n".join(dedented) + "\n"
                child_node = LeafNode("code", cleaned)
                html.append(ParentNode("pre", [child_node]))

            case BlockType.ULIST: 
                items = clean_lines(lines, BlockType.ULIST)
                childrens = []
                for i in items:
                    childrens.append(ParentNode("li", text_to_children([i])))
                html.append(ParentNode("ul", childrens))

            case BlockType.OLIST: 
                items = clean_lines(lines, BlockType.OLIST)
                childrens = []
                for i in items:
                    childrens.append(ParentNode("li", text_to_children([i])))
                html.append(ParentNode("ol", childrens))


    return ParentNode('div', html)




def text_to_children(text):
    childrens = []
    for line in text:
        textnodes = text_to_textnodes(line)
        for node in textnodes:
            if not node.text:
                continue
            childrens.append(text_node_to_html_node(node))
    return childrens

def clean_lines(lines, block_type):
    clean = []
    for line in lines:
        match block_type:
            case BlockType.PARAGRAPH:
                clean.append(line.strip())
            case BlockType.HEADING: 
                if line:
                    clean.append(line.lstrip('#').lstrip())
                    break

            case BlockType.QUOTE: 
                clean.append(line.lstrip('>').lstrip())

            case BlockType.ULIST: 
                clean.append(line.lstrip('-').lstrip())

            case BlockType.OLIST:
                if not line:
                    continue
                while line[0].isdigit():
                    line = line[1:]
                if line.startswith('.'):
                    clean.append(line.split('. ', 1)[1])

                
    return clean




# tells the type of block it is, receives one element of str block
def block_to_block_type(block):
    block = block.strip()
    lines = block.split('\n')

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].lstrip().startswith("```") and lines[-1].lstrip().startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH



#takes markdown file, and split it into a list of inline blocks
#based on blocks separated by \n\n
def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks



