from textnode import TextNode, TextType
#textnode (text, type, url)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # check order text, bold, italic, code, link, image
    new_nodes = []
    split_old = []

    for oldie in old_nodes:

        if oldie.text_type != TextType.TEXT:
            new_nodes.append(TextNode(oldie, oldie.text_type))
        elif oldie.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown syntax")
        else:
            split_old = oldie.text.split(delimiter)
            #catch formatted first word
            if oldie.text.index(delimiter) == 0:
                split_old = split_old[1:]
                new_nodes.append(TextNode(split_old[0], text_type))
                new_nodes.append(TextNode(split_old[1], TextType.TEXT))
            #catch formatted last word
            elif oldie.text[::-1].index(delimiter) == 0:
                new_nodes.append(TextNode(split_old[0], TextType.TEXT))
                new_nodes.append(TextNode(split_old[1], text_type))
            #catch formatted word in middle
            else:
                for i in range(0, len(split_old)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_old[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_old[i], text_type))

    return new_nodes




    '''first pass code with link & image
    match text_type:
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
    '''
