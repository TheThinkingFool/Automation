"""
GitHub Source Link of easyocr: https://github.com/JaidedAI/EasyOCR
model hub link: https://www.jaided.ai/easyocr/modelhub/
two models are downloaded from model hub: 'en' and 'chinese'
"""

import easyocr
import numpy as np

def ocr_image_english(cropped_image, model_dir):
    """
    Perform OCR on the cropped image using easyocr.

    :param cropped_image: Cropped image.
    :param model_dir: Directory where the models are stored.
    :return: Extracted text.
    """
    lang = ['en'] # set language to English

    # Convert PIL image to numpy array
    open_cv_image = np.array(cropped_image)

    # Initialize the easyocr reader with the specified model directory
    reader = easyocr.Reader(lang, model_storage_directory=model_dir)

    # Perform OCR on the image
    result = reader.readtext(open_cv_image)

    # Extract text from the result
    text = ' '.join([res[1] for res in result])
    return text

def ocr_image_chinese(cropped_image, model_dir):
    """
    Perform OCR on the cropped image using easyocr.

    :param cropped_image: Cropped image.
    :param lang: Language code(s) to use for OCR. e.g. ['en'] for English, ['ch_tra'] for Chinese.
    :param model_dir: Directory where the models are stored.
    :return: Extracted text.
    """
    lang = ['ch_tra'] # set language to Chinese

    # Convert PIL image to numpy array
    open_cv_image = np.array(cropped_image)

    # Initialize the easyocr reader with the specified model directory
    reader = easyocr.Reader(lang, model_storage_directory=model_dir)

    # Perform OCR on the image
    result = reader.readtext(open_cv_image)

    # Extract text from the result
    text = ' '.join([res[1] for res in result])
    return text


# Example usage, eng works as expected, chinese is not ideal
'''
from pdf_to_image import crop_image
image_path = 'output_image.jpg'
box = (50, 50, 300, 300)  # Example coordinates for the rectangular box
model_dir = "easyOCR_models"  # model directory
cropped_image = crop_image(image_path, box)
text = ocr_image_english(cropped_image, model_dir)
print(f"\nExtracted text: {text}")

image_path = 'DSE.jpg'
box = (50, 50, 300, 800)  # Example coordinates for the rectangular box
model_dir = "easyOCR_models"  # model directory
cropped_image = crop_image(image_path, box)
text = ocr_image_chinese(cropped_image, model_dir)
print(f"\nExtracted text: {text}")'''