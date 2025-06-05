import os, pathlib

from blocks import markdown_to_html_node


def extract_title(markdown):

    with open(markdown, "r") as f:
        plain_heading = ""
        for line in f:
            if line.startswith("# "):
                plain_heading = line[2:].strip()
                return(plain_heading)
        print(plain_heading)
        if plain_heading == "":
            raise Exception("No heading found")


def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        source_file = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    source_heading = str(extract_title(from_path))
    source_nodes = markdown_to_html_node(source_file)
    source_html = source_nodes.to_html()

    new_title = template.replace("{{ Title }}", source_heading)
    new_page = new_title.replace("{{ Content }}", source_html)

    with open(dest_path, "w") as file:
        file.write(new_page)
        print("Page generation complete. Starting html server...")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, item)
        if os.path.isdir(path):
            new_dest = path.replace("content", "public")
            generate_pages_recursive(path, template_path, new_dest)
        if os.path.isfile(path):
            new_path = path.replace("content", "public")
            new_path = new_path[:-3] + ".html"
            generate_page(path, template_path, new_path)

    return
