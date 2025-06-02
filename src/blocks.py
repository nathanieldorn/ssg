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
        if block == "":
            continue
        final_block_list.append(block.strip())
    return final_block_list


def block_to_block_type(block):
    block_lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(block_lines) > 1 and block_lines[0].startswith("```") and block_lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in block_lines:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in block_lines:
            if line[0:2] != "- ":
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
    return child_nodes


def block_to_paragraph(block):
    block_lines = block.split("\n")
    paragraph = " ".join(block_lines)
    paragraph_children = text_to_children(paragraph)
    return ParentNode("p", paragraph_children)


def block_to_heading(block):
    header_count = block[0:7].count("#")
    if 0 < header_count < 7:
        header_html = ParentNode(f"h{header_count}", text_to_children(block[header_count + 1:]))
        return header_html
    else:
        raise ValueError("Invalid Markdown heading syntax")


def block_to_code(block):
    code_text_node = TextNode(block[4:-3], TextType.TEXT)
    code_html = text_node_to_html_node(code_text_node)
    code_node = ParentNode("code", [code_html])
    pre_code_node = ParentNode("pre", [code_node])
    return pre_code_node


def block_to_quote(block):
    lines = block.split("\n")
    html_quotes = []
    for line in lines:
        if line[0] != ">":
            raise ValueError("Invalid quote format")
        else:
            html_quotes.append(line[1:].strip())
    quote_joined = " ".join(html_quotes)
    quote_html = ParentNode("blockquote", text_to_children(quote_joined))
    return quote_html


def block_to_list(block, list_type):
    lines = block.split("\n")
    html_list = []
    list_text = ""
    for line in lines:
        if list_type == "ul":
            list_text = line[2:]
        elif list_type == "ol":
            list_text = line[3:]
        list_children = text_to_children(list_text)
        html_list.append(ParentNode("li", list_children))
    return ParentNode(list_type, html_list)



def block_to_html_node(block):
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return block_to_paragraph(block)
        case BlockType.HEADING:
            return block_to_heading(block)
        case BlockType.CODE:
            return block_to_code(block)
        case BlockType.QUOTE:
            return block_to_quote(block)
        case BlockType.UNORDERED_LIST:
            return block_to_list(block, "ul")
        case BlockType.ORDERED_LIST:
            return block_to_list(block, "ol")
        case _:
            raise ValueError("Block type invalid")


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    child_nodes = []

    for block in md_blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes, None)
