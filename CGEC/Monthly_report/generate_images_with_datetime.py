'''
Part 3: Generate Images with Date and Time
    generate another image folder and copy the images from the original image folder,
        and stick the date and time on the bottom right of images,
    rename the images with the generated date and time.
    (format of $ref_no$_$location$_$title$_$date_time$_$weather_condition$.jpg)
'''

import os
from PIL import Image, ImageDraw, ImageFont
import shutil


def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def add_datetime_to_image(image_path, date_time, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    # Load a TrueType font with a larger size
    font_path = "arial.ttf"  # Path to a TrueType font file
    font_size = 36  # Set the desired font size
    font = ImageFont.truetype(font_path, font_size)
    text = date_time
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    width, height = image.size
    x, y = width - text_width - 10, height - text_height - 10
    draw.text((x, y), text, font=font, fill="white")
    image.save(output_path)


def process_images_with_datetime(image_folder, output_folder, image_variables, date_times):
    create_output_folder(output_folder)
    processed_image_paths = []

    for i, image_var in enumerate(image_variables):
        ref_no, location, title, weather_condition = image_var.values()
        date_time = date_times[i]

        # Construct file paths with and without weather condition
        original_image_path_with_weather = os.path.join(image_folder,
                                                        f"{ref_no}_{location}_{title}_{weather_condition}.png")
        original_image_path_without_weather = os.path.join(image_folder, f"{ref_no}_{location}_{title}.png")

        # Determine which file path exists
        if os.path.exists(original_image_path_with_weather):
            original_image_path = original_image_path_with_weather
        elif os.path.exists(original_image_path_without_weather):
            original_image_path = original_image_path_without_weather
        else:
            print(f"File not found: {original_image_path_with_weather} or {original_image_path_without_weather}")
            continue  # Skip to the next iteration if neither file exists

        # Print the constructed file path for debugging
        print(f"Using file: {original_image_path}")

        # Format date_time for image text
        date_time_for_image = date_time

        # Format date_time for file name
        date_time_for_filename = date_time.replace("/", "-").replace(":", ".")

        new_image_name = f"{ref_no}_{location}_{title}_{date_time_for_filename}_{weather_condition}.png"
        output_image_path = os.path.join(output_folder, new_image_name)

        add_datetime_to_image(original_image_path, date_time_for_image, output_image_path)
        processed_image_paths.append(output_image_path)

    return processed_image_paths

# Example usage, works as expected
'''
image_folder = "C:/Users/ddjfe/Downloads/Monthly Report Photos/photos"
output_folder = "C:/Users/ddjfe/Downloads/Monthly Report Photos/photos_with_datetime"
image_variables = [
    # Example image variables
    ("01", "SWHWRP", "Aerial View", "FINE")
    # Add more as needed
]
date_times = [
    "31/01/2024 13:59"
    # Add more as needed
]

process_images_with_datetime(image_folder, output_folder, image_variables, date_times)
'''