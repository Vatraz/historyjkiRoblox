import os

from PIL import Image


def remove_white_margins(input_path, output_path):
    image = Image.open(input_path)
    image_data = image.getdata()

    non_transparent_pixels = [
        (x, y)
        for x in range(image.width)
        for y in range(image.height)
        if image_data.getpixel((x, y))[3] != 0
    ]
    if non_transparent_pixels:
        min_x = min(non_transparent_pixels, key=lambda p: p[0])[0]
        max_x = max(non_transparent_pixels, key=lambda p: p[0])[0]
        min_y = min(non_transparent_pixels, key=lambda p: p[1])[1]
        max_y = max(non_transparent_pixels, key=lambda p: p[1])[1]

        cropped_image = image.crop((min_x, min_y, max_x + 1, max_y + 1))

        max_side = max(cropped_image.width, cropped_image.height)
        padded_image = Image.new(cropped_image.mode, (max_side, max_side), (0, 0, 0, 0))
        padded_image.paste(
            cropped_image,
            (
                (max_side - cropped_image.width) // 2,
                (max_side - cropped_image.height) // 2,
            ),
        )

        padded_image.save(output_path)
    else:
        print("Image is entirely transparent.")


def remove_background():
    list_of_files = os.listdir("C:/Users/Janek/postacki/")
    name_of_file = 0

    for file in list_of_files:
        name_of_file += 1
        input_path = "C:/Users/Janek/postacki/" + file
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_path = "C:/Users/Janek/postacki_png/" + str(name_of_file) + ".png"
        output_image.save(output_path)


def random_string(n: int = 8) -> str:
    return ""
