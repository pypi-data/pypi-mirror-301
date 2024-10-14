import argparse
from commands.display_image import display_image

def main():
    parser = argparse.ArgumentParser(prog="gazo")
    parser.add_argument("file", help="the image file to display")
    parser.add_argument("-l", "--line", type=int, help="specifies output height")

    args = parser.parse_args()

    display_image(args.file, args.line)

if __name__ == "__main__":
    main()