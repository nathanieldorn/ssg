import re

def extract_markdown_images(text):
    # grab alt text between [] and url between () from string
    if len(re.findall(r"!\[\]", text)) > 0:
        raise Exception("No alt text found for image")
    elif len(re.findall(r"\]\(\)", text)) > 0:
        raise Exception("No url for image found")
    else:
        return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    # grab anchor text between [] and url between () but not after ! from string
    if len(re.findall(r"\[\]", text)) > 0:
        raise Exception("No anchor text found for link")
    elif len(re.findall(r"\]\(\)", text)) > 0:
        raise Exception("No url for link found")
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
