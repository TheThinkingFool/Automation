import fitz  # PyMuPDF
import os
from PIL import Image, ImageDraw
from ocr_image import ocr_image_english, ocr_image_chinese

def pdf_to_image(pdf_path, output_folder, output_image_name):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Get the first page
    page = pdf_document.load_page(0)

    # Render the page to an image
    pix = page.get_pixmap()

    # Save the image
    output_image_path = os.path.join(output_folder, output_image_name)
    pix.save(output_image_path)

    return output_image_path

# Example usage, works as expected
'''
import tk_file
def test_pdf_to_image():
    pdf_path = tk_file.open_file_explorer(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    output_folder = tk_file.open_folder_explorer(title="Select a folder to save the image")
    output_image_name = 'output_image.jpg'
    image_path = pdf_to_image(pdf_path, output_folder, output_image_name)
    print(f"Image saved at: {image_path}")

test_pdf_to_image()
'''


def crop_image(image_path, box):
    """
    Crop the image to the specified box.

    :param image_path: Path to the input image.
    :param box: A tuple (x1, y1, x2, y2) defining the rectangular box to crop.
    :return: Cropped image.
    """
    image = Image.open(image_path)
    cropped_image = image.crop(box)
    return cropped_image

def get_original_coordinates(resized_bbox, width_ratio, height_ratio):
    x1_resized, y1_resized = resized_bbox[0]
    x2_resized, y2_resized = resized_bbox[1]

    x1_original = int(x1_resized / width_ratio)
    y1_original = int(y1_resized / height_ratio)
    x2_original = int(x2_resized / width_ratio)
    y2_original = int(y2_resized / height_ratio)

    return (x1_original, y1_original), (x2_original, y2_original)

# Example usage, works as expected
def test_get_original_coordinates():
    resized_bbox = [(50, 50), (150, 150)]
    width_ratio = 0.5  # Example ratio
    height_ratio = 0.5  # Example ratio

    original_bbox = get_original_coordinates(resized_bbox, width_ratio, height_ratio)
    print("Original coordinates:", original_bbox)

# test_get_original_coordinates() # Output: Original coordinates: ((100, 100), (300, 300))


def crop_and_draw_bboxes(image_path, bboxes, width_ratio, height_ratio):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for bbox in bboxes:
        original_bbox = get_original_coordinates(bbox, width_ratio, height_ratio)
        x1, y1 = original_bbox[0]
        x2, y2 = original_bbox[1]

        # Crop the image
        cropped_image = image.crop((x1, y1, x2, y2))
        cropped_image.show()

        # Draw the bounding box on the original image
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

    # Save the image with bounding boxes
    output_image_with_bboxes = os.path.join(os.path.dirname(image_path), "output_image_with_bboxes.jpg")
    image.save(output_image_with_bboxes)
    return output_image_with_bboxes

# Example usage, works as expected
def test_crop_and_draw_bboxes():
    import tk_file
    pdf_path = tk_file.open_file_explorer(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    output_folder = tk_file.open_folder_explorer(title="Select a folder to save the image")
    output_image_name = output_folder + 'output.jpg'
    image_path = pdf_to_image(pdf_path, output_folder, output_image_name)

    # Example bounding boxes in resized coordinates
    bboxes = [[(50, 50), (210, 90)], [(200, 200), (300, 300)]]
    width_ratio = 0.77  # Example ratio
    height_ratio = 0.77  # Example ratio

    output_image_with_bboxes = crop_and_draw_bboxes(image_path, bboxes, width_ratio, height_ratio)
    print(f"Image with bounding boxes saved at: {output_image_with_bboxes}")


def crop_and_ocr_bboxes(image_path, bboxes, width_ratio, height_ratio, langs):
    """
    Crop the image to the specified bounding boxes and perform OCR on each cropped image.
    :param image_path: Path to the input image.
    :param bboxes: List of bounding boxes in resized coordinates.
    :param width_ratio: Width ratio used for resizing.
    :param height_ratio: Height ratio used for resizing.
    :param langs: List of languages for OCR.
    :return: List of OCR results for each bounding box.
    """
    image = Image.open(image_path)
    ocr_results = []

    for bbox in bboxes:
        original_bbox = get_original_coordinates(bbox, width_ratio, height_ratio)
        x1, y1 = original_bbox[0]
        x2, y2 = original_bbox[1]

        # Crop the image
        cropped_image = image.crop((x1, y1, x2, y2))

        # Perform OCR on the cropped image
        if ['en'] in langs:
            ocr_results.append(ocr_image_english(cropped_image, 'easyOCR_models'))
        elif ['ch_tra'] in langs:
            ocr_results.append(ocr_image_chinese(cropped_image, 'easyOCR_models'))
        else:
            ocr_results.append("Language not supported")

    return ocr_results

# Example usage, works as expected
def test_crop_and_ocr_bboxes():
    import tk_file
    pdf_path = tk_file.open_file_explorer(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    output_folder = tk_file.open_folder_explorer(title="Select a folder to save the image")
    output_image_name = output_folder + 'output.jpg'
    image_path = pdf_to_image(pdf_path, output_folder, output_image_name)

    # Example bounding boxes in resized coordinates
    bboxes = [[(50, 50), (210, 90)], [(200, 200), (300, 300)]]
    width_ratio = 0.77  # Example ratio
    height_ratio = 0.77  # Example ratio

    output_image_with_bboxes = crop_and_ocr_bboxes(image_path, bboxes, width_ratio, height_ratio, [['en'], ['en']])
    print(f"OCR Results: {output_image_with_bboxes}")
