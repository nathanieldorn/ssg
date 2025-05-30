from enum import Enum

from splitnodes import markdown_to_blocks, text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):

    #check for heading 1-6 blocks
    if "# " in block[0:7]:
        return BlockType.HEADING

    #check for code blocks
    elif block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    #check for quote blocks
    elif block[0] == ">":

        if "\n" in block:
            line_indices = []
            num_lines = block.count("\n")
            start = 0
            match_tally = 0

            #get indices of each new line
            for x in range(0, num_lines):
                start = block.find("\n", start)
                line_indices.append(start)
                start += 2

            #verify incremental list start
            for i in range(0, len(line_indices)):
                if block[line_indices[i]+1] == ">":
                    match_tally += 1
                else:
                    return BlockType.PARAGRAPH

            if match_tally == num_lines:
                return BlockType.QUOTE
            else:
                return BlockType.PARAGRAPH

        else:
            return BlockType.QUOTE


    #check for unordered lists
    elif block[0:2] == "- ":

        if "\n" in block:
            line_indices = []
            num_lines = block.count("\n")
            start = 0
            match_tally = 0

            #get indices of each new line
            for x in range(0, num_lines):
                start = block.find("\n", start)
                line_indices.append(start)
                start += 2

            #verify incremental list start
            for i in range(0, len(line_indices)):
                if block[line_indices[i]+1:line_indices[i]+3] == "- ":
                    match_tally += 1
                else:
                    return BlockType.PARAGRAPH

            if match_tally == num_lines:
                return BlockType.UNORDERED_LIST
            else:
                return BlockType.PARAGRAPH

        else:
            return BlockType.UNORDERED_LIST


    #check for ordered lists
    elif block[0:3] == "1. ":

        if "\n" in block:
            line_indices = []
            num_lines = block.count("\n")
            start = 0
            match_tally = 0

            #get indices of each new line
            for x in range(0, num_lines):
                start = block.find("\n", start)
                line_indices.append(start)
                start += 2

            #verify incremental list start
            for i in range(0, len(line_indices)):
                if block[line_indices[i]+1:line_indices[i]+4] == f"{match_tally+2}. ":
                    match_tally += 1
                else:
                    return BlockType.PARAGRAPH

            if match_tally == num_lines:
                return BlockType.ORDERED_LIST
            else:
                return BlockType.PARAGRAPH

        else:
            return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    #convert md doc into a single parent htmlnode, may contain children htmlnodes
    #for parent, (tag, children, props=None)

    md_blocks = markdown_to_blocks(markdown)

    for block in md_blocks:

        #based on type, create a new htmlnode with the proper data
        #for html, (tag=None, value=None, children=None, props=None)
        match block_to_block_type(block):
            case BlockType.HEADING:
                #text to textnode
                text_node = text_to_textnodes(block)
                #textnode to htmlnode
                html_node = text_node_to_html_node(text_node)

                return
