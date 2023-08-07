from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap


# Text and title for "Black Swan"
title = "Black Swan"
description = (
    "A Black Swan is an unpredictable event that is beyond what is normally expected of a situation and "
    "has potentially severe consequences. Black Swan events are characterized by their extreme rarity, "
    "severe impact, and the widespread insistence they were obvious in hindsight."
)


def calculate_text_height(text, font, spacing=0):
    return sum(font.getbbox(line)[3] + spacing for line in text.splitlines())

def create_image(title, description, title_font_path=None, description_font_path=None):
    square_width = 1280
    square_height = square_width

    title_font_size = 140 # 70
    description_font_size = 60 # 30
    margin_left_square = square_width * 0.20
    margin_right_square = square_width * 0.20

    # font_path_bold = "CanelaText-Bold-Trial.otf"
    # font_path_regular = "CanelaText-Regular-Trial.otf"

    # Use default fonts if none are provided
    if title_font_path is None:
        title_font_path = 'CanelaText-Bold-Trial.otf'
    if description_font_path is None:
        description_font_path = 'CanelaText-Regular-Trial.otf'

    title_font = ImageFont.truetype(title_font_path, title_font_size)
    description_font = ImageFont.truetype(description_font_path, description_font_size)

    # Define max title width considering the left and right margins
    max_title_width = square_width - margin_left_square - margin_right_square

    # Wrap the title text based on the maximum width (considering both left and right margins)
    wrapped_title = wrap(title, width=int(max_title_width / (title_font_size / 2)))
    wrapped_title_text = "\n".join(wrapped_title)

    # Title text position (left margin, vertical position)
    title_position = (
        margin_left_square, # horisontal margin
        (square_height / 6) - (title_font_size / 4), # vertical position
    )

    # Calculate the total height of the title text (including any newlines and spacing)
    title_text_height = calculate_text_height(wrapped_title_text, title_font)

    # Description position (left margin, below title by title_text_height plus description_font_size pixels)
    description_position = (
        margin_left_square,
        title_position[1] + title_text_height + description_font_size*1.5,
    )

    # Wrap description
    wrapped_description = "\n".join(wrap(description, width = 30)) # width=30))

    # Create image
    image = Image.new("RGB", (square_width, square_height), (253, 241, 230))
    draw = ImageDraw.Draw(image)

    # Draw title text (potentially multiple lines)
    draw.multiline_text(
        title_position,
        wrapped_title_text,
        font=title_font,
        fill="black",
        spacing=10)

    # Draw title
    draw.multiline_text(
        description_position,
        wrapped_description,
        font=description_font,
        fill="black",
        spacing= 10,
    )

    # Display or save the image
    #image.show()
    image.save(title + ".png")