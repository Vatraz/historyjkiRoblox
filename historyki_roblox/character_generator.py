from rembg import remove
from PIL import Image


class CharacterGenerator:
    def remove_background(self):
        input_path = 'C:/Users/Janek/postacki/1.png'

        # Store path of the output image in the variable output_path
        output_path = 'C:/Users/Janek/postacki/1_changed.png'

        # Processing the image
        input_image = Image.open(input_path)

        # Removing the background from the given Image
        output_image = remove(input_image)

        # Saving the image in the given path
        output_image.save(output_path)

