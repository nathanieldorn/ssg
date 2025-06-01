from enum import Enum

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from splitnodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    initial_block_list = markdown.split("\n\n")
    final_block_list = []
    for block in initial_block_list:
        cleaned = block.strip()
        final_block_list.append(cleaned)
    return final_block_list


def block_to_block_type(block):

    block_lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(block_lines) > 1 and block_lines[0].startswith("```") and block_lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in block_lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in block_lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in block_lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        child_nodes.append(html_node)
    print("\nCHILD NODES TEST\n")
    print(child_nodes)
    return child_nodes


def block_to_paragraph(block):
    #block_lines = block.split("\n")
    #paragraph = " ".join(block_lines)
    paragraph_children = text_to_children(block)
    return ParentNode("p", paragraph_children)


def block_to_heading(block):
    header_count = block[0:7].count("#")
    if 0 < header_count < 7:
        header_html = ParentNode(f"h{header_count}", text_to_children(block))
        return header_html
    else:
        raise Exception("Invalid Markdown heading syntax")


def block_to_code(block):
    code_text_node = TextNode(block[3:-3], TextType.CODE)
    code_html = text_node_to_html_node(code_text_node)
    return code_html


def block_to_quote(block):
    quote_html = ParentNode("blockquote", text_to_children(block))
    return quote_html


def block_to_list(block, tag):
    pass
    list_html = ParentNode(tag, text_to_children(block))
    #for child in list_html.children:
      #  child.tag = "li"
    return list_html


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    child_nodes = []

    for block in md_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_node = block_to_paragraph(block)
                child_nodes.append(block_to_paragraph(block))
            case BlockType.HEADING:
                html_node = block_to_heading(block)
                child_nodes.append(html_node)
            case BlockType.CODE:
                html_node = block_to_code(block)
                child_nodes.append(html_node)
            case BlockType.QUOTE:
                html_node = block_to_quote(block)
                child_nodes.append(html_node)
            case BlockType.UNORDERED_LIST:
                html_node = block_to_list(block, "ul")
                child_nodes.append(html_node)
            case BlockType.ORDERED_LIST:
                html_node = block_to_list(block, "ol")
                child_nodes.append(html_node)
            case _:
                raise Exception("We ain't found $#@&!")

    md_parent_node = ParentNode("div", child_nodes)
    print("PARENT TEST")
    print(md_parent_node.to_html())
    return md_parent_node
