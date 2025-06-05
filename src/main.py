import sys

from textnode import *
from static import clear_public, copy_static
from page import generate_page, generate_pages_recursive

def main():

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    clear_public(deleted_paths=[], directory="../docs")
    copy_static(copied_paths=[], directory="../static")
    generate_pages_recursive("../content", "../template.html", "../docs/", basepath)

if __name__ == "__main__":
    main()
