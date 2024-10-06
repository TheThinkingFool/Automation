'''
Part 1: Extract Image Variables
    extract the variables from the images name of the image folder,
    image name format: $ref_no$_$location$_$title$_$weather_condition$.jpg,
    or $ref_no$_$location$_$title$.jpg, default weather condition is "FINE".
1. List all files in the specified image folder.
2. Use a regular expression to match the image name format.
3. Extract the reference number, location, title, and weather condition (defaulting to "FINE" if not present).
4. Store the extracted data in a list of dictionaries and return it.
'''

import tkinter as tk
from tkinter import filedialog
import re
import os


def extract_image_variables(image_folder):
    image_files = os.listdir(image_folder)
    image_data = []

    for image_file in image_files:
        match = re.match(r'(\d+)_([^_]+)_([^_]+)(?:_([^_]+))?.(jpg|png)', image_file, re.IGNORECASE)
        if match:
            ref_no = match.group(1)
            location = match.group(2)
            title = match.group(3)
            weather_condition = match.group(4) if match.group(4) else "FINE"
            image_data.append({
                'ref_no': ref_no,
                'location': location,
                'title': title,
                'weather_condition': weather_condition
            })

    return image_data
