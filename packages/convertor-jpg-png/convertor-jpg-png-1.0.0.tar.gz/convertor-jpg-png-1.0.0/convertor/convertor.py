import os
from PIL import Image


def convert_images(input_folder, output_folder):
    """
    Convert all PNG images in the input folder to JPEG format and save them in the output folder.
    :param input_folder:
    :param output_folder:
    :return:
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            # Check if the file is a JPEG image
            if file.lower().endswith('.png'):
                # Construct full file path
                input_path = os.path.join(root, file)

                # Create output path by replacing input folder with output folder
                # and changing the file extension to .png
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.jpg')

                # Create the output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Open the image and convert it to PNG
                try:
                    with Image.open(input_path) as img:
                        img.save(output_path, 'JPEG', quality=95)
                    print(f"Converted: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Failed to convert {input_path}: {e}")


