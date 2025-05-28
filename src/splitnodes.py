import re

from imglinkextractor import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for oldie in old_nodes:
        if oldie.text_type != TextType.TEXT:
            new_nodes.append(oldie)
            continue
        split_old = []
        delimited_text = oldie.text.split(delimiter)
        if len(delimited_text) % 2 == 0:
            raise ValueError("Incorrect Markdown syntax")

        for i in range(0, len(delimited_text)):
            if delimited_text[i] == "":
                continue
            if i % 2 == 0:
                split_old.append(TextNode(delimited_text[i], TextType.TEXT))
            else:
                split_old.append(TextNode(delimited_text[i], text_type))
        new_nodes.extend(split_old)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type == TextType.TEXT:
            matches = extract_markdown_images(old_node.text)
            if matches:
                split_text = old_node.text
                for tuple in matches:
                    alt_text, url = tuple
                    text_before, split_text = split_text.split(f"![{alt_text}]({url})", 1)
                    if text_before != "":
                        new_nodes.append(TextNode(text_before, TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
                if split_text != "":
                    new_nodes.append(TextNode(split_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
        else:
            new_nodes.append(old_node)

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type == TextType.TEXT:
            matches = extract_markdown_links(old_node.text)
            if matches:
                split_text = old_node.text
                for tuple in matches:
                    anchor_text, url = tuple
                    text_before, split_text = split_text.split(f"[{anchor_text}]({url})", 1)
                    if text_before != "":
                        new_nodes.append(TextNode(text_before, TextType.TEXT))
                    new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                if split_text != "":
                    new_nodes.append(TextNode(split_text, TextType.TEXT))
            else:
                new_nodes.append(old_node)
        else:
            new_nodes.append(old_node)

    return new_nodes

def text_to_textnodes(text):
    textnode_list = []
    bold_list = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    italic_list = split_nodes_delimiter(bold_list, "_", TextType.ITALIC)
    code_list = split_nodes_delimiter(italic_list, "`", TextType.CODE)
    image_list = split_nodes_image(code_list)
    textnode_list = split_nodes_links(image_list)

    return textnode_list
