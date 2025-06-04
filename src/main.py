from textnode import *
from static import clear_public

def main():
    textnode_test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(repr(textnode_test))
    return clear_public("../public")


if __name__ == "__main__":
    main()
