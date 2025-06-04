from textnode import *
from static import clear_public, copy_static

def main():
    clear_public(deleted_paths=[], directory="../ssg/public")
    copy_static(copied_paths=[], directory="../ssg/static")

if __name__ == "__main__":
    main()
