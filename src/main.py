from textnode import *
from static import clear_public, copy_static
from page import generate_page, generate_pages_recursive

def main():
    clear_public(deleted_paths=[], directory="../ssg/public")
    copy_static(copied_paths=[], directory="../ssg/static")
    generate_pages_recursive("../ssg/content", "../ssg/template.html", "../ssg/public/")

if __name__ == "__main__":
    main()
