from textnode import *

def main():
    textnode_test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(repr(textnode_test))

if __name__ == "__main__":
    main()
