from PIL import Image, UnidentifiedImageError
import sys
import os
import math

def display_image(file_path, output_height=None):
    os.system("")

    term_size = os.get_terminal_size()
    output_width = math.floor(term_size.columns / 2)
    output_height = math.floor(term_size.lines - 2) if output_height is None else output_height

    try:
        img = Image.open(file_path)
    except FileNotFoundError:
        print("file not found")
        sys.exit(1)
    except UnidentifiedImageError:
        print("file format not supported")
        sys.exit(1)

    if img.format == "PNG":
        img = img.convert("RGB")

    if output_width < img.width:
        height = math.floor(output_width / img.width * img.height)
        img = img.resize((output_width, height))
    if output_height < img.height:
        width = math.floor(output_height / img.height * img.width)
        img = img.resize((width, output_height))

    for y in range(img.height):
        for x in range(img.width):
            color = img.getpixel((x, y))
            print(f"\033[48;2;{color[0]};{color[1]};{color[2]}m  \033[m", end="")
        print()