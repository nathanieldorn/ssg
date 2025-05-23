from textnode import TextNode, TextType
#textnode (text, type, url)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # check order text, bold, italic, code, link, image
    new_nodes = []
    split_list = []

    for oldie in old_nodes:
        if oldie.TextType != TextType.TEXT:
            new_nodes.extend([TextNode(oldie, oldie.TextType, oldie.url)])
        elif oldie.count(delimiter) < 2:
            raise Exception("Invalid Markdown syntax")
        match text_type:
            case TextType.BOLD:
                split_list = oldie.split("**")
            case TextType.ITALIC:
                split_list = oldie.split("_")
            case TextType.CODE:
                split_list = oldie.split("`")
            case TextType.LINK:
                link_list1 = oldie.split("(")
                link_list2 = link_list1.split(")")
                split_list.extend(link_list1[0])
                split_list.extend(link_list2)
            case TextType.IMAGES:
                img_list1 = oldie.split("(")
                img_list2 = img_list1.split(")")
                split_list.extend(img_list1[0])
                split_list.extend(img_list2)
            case _:
                raise Exception("Invalid text type")

        for item in split_list:
            item_count = 0
            if item_count == 1:
                new_nodes.extend([TextNode(item, text_type)])
            else:
                new_nodes.extend([TextNode(item, TextType.TEXT)])
            item_count += 1
