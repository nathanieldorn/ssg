from blocks import markdown_to_html_node


def extract_title(markdown):

    with open(markdown, "r") as f:
        plain_heading = ""
        for line in f:
            if line.startswith("# "):
                plain_heading = line[2:].strip()
                return(plain_heading)
        if plain_heading == "":
            raise Exception("No heading found")


def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        source_file = file.read()
        with open(template_path, "r") as file:
            template = file.read()
            source_nodes = markdown_to_html_node(source_file)
            source_html = source_nodes.to_html
            source_heading = extract_title(source_file)
            if source_heading != None:
                template.replace("{{ Title }}", source_heading)
            if source_html != "":
                template.replace("{{ Content }}", str(source_html))
            with open(dest_path, "w") as file:
                file.write(template)
                #incorporate paths and directories that don't exist!!!
