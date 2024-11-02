import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os
from coco_file import load_coco_file, save_to_coco_file, test_save_load_coco_file
from coco_file import get_annotations_by_supplier, update_annotation
from pdf_to_image import pdf_to_image, crop_and_ocr_bboxes
import tkinter.messagebox as messagebox

window_to_screen_ratio_width = 0.6
window_to_screen_ratio_height = 0.6
pdf_panel_ratio_width = 0.7
pdf_panel_ratio_height = 0.9
ocr_panel_ratio_width = 1 - pdf_panel_ratio_width
ocr_panel_ratio_height = 0.9
max_image_ratio = 0.75


class PDFToImageApp:
    def __init__(self, root, window_width, window_height, max_image_width, max_image_height):

        self.root = root
        self.root.title("PDF to Image OCR")
        self.file_path = 'annotations.coco'

        # Set the ratio of window to pdf_panel dimensions
        self.pdf_panel_width = int(window_width * pdf_panel_ratio_width)
        self.pdf_panel_height = int(window_height * pdf_panel_ratio_height)
        self.ocr_panel_width = int(window_width * ocr_panel_ratio_width)
        self.ocr_panel_height = int(window_height * ocr_panel_ratio_height)
        self.max_image_width = max_image_width
        self.max_image_height = max_image_height
        self.original_width, self.original_height = None, None
        self.resized_width, self.resized_height = None, None

        # Load company DN styles
        self.coco_data = load_coco_file(self.file_path)
        self.company_styles = [supplier['name'] for supplier in self.coco_data['suppliers']]

        # Variables to store selected supplier name and ID
        self.selected_supplier_name = None
        self.selected_supplier_id = None

        # Create the main layout
        self.create_widgets()

    def create_widgets(self):
        # Top panel for company DN style selection
        self.style_label = ttk.Label(self.root, text="Select Company DN Style:")
        self.style_label.pack(pady=5)

        self.style_combobox = ttk.Combobox(self.root, values=self.company_styles)
        self.style_combobox.pack(pady=5)
        self.style_combobox.bind("<<ComboboxSelected>>", self.update_ocr_panel)

        # PDF panel for drag-and-drop and image display
        self.pdf_panel = tk.Frame(self.root, width=self.pdf_panel_width, height=self.pdf_panel_height, bg='white',
                                  relief=tk.SUNKEN, bd=2)
        self.pdf_panel.pack(side=tk.LEFT, padx=10, pady=10)

        self.pdf_panel.drop_target_register(DND_FILES)
        self.pdf_panel.dnd_bind('<<Drop>>', self.drop)

        self.canvas = tk.Canvas(self.pdf_panel, width=self.pdf_panel_width, height=self.pdf_panel_height)
        self.canvas.place(x=0, y=0, width=self.pdf_panel_width, height=self.pdf_panel_height)

        # Variables for dragging bounding boxes
        self.bboxes = []
        self.dragging_corner = None
        self.current_bbox = None
        self.current_annotation_key = None

        # OCR panel for displaying selected supplier DN type
        self.ocr_panel = tk.Frame(self.root, width=self.ocr_panel_width, height=self.ocr_panel_height, bg='lightgrey', relief=tk.SUNKEN, bd=2)
        self.ocr_panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.ocr_label = ttk.Label(self.ocr_panel, text="Selected Supplier DN Type:")
        self.ocr_label.pack(pady=5)

        self.selected_dn_type_label = ttk.Label(self.ocr_panel, text="None")
        self.selected_dn_type_label.pack(pady=5)

        # Add OCR button
        self.ocr_button = ttk.Button(self.ocr_panel, text="OCR", command=self.perform_ocr)
        self.ocr_button.pack(pady=5)

        self.annotations_frame = tk.Frame(self.ocr_panel, bg='lightgrey')
        self.annotations_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.data_type_comboboxes = {}
        self.type_entries = {}

        self.coordinates_label = ttk.Label(self.ocr_panel, text="Coordinates: (0, 0), (0, 0)")
        self.coordinates_label.pack(pady=5)
        self.coordinates_label_original = ttk.Label(self.ocr_panel, text="Original Coordinates: (0, 0), (0, 0)")
        self.coordinates_label_original.pack(pady=5)

        self.save_button = ttk.Button(self.ocr_panel, text="Save OCR Settings", command=self.save_ocr_settings)
        self.save_button.pack(pady=5)

    def update_ocr_panel(self, event):
        selected_supplier_name = self.style_combobox.get()
        selected_supplier = next((supplier for supplier in self.coco_data['suppliers'] if supplier['name'] == selected_supplier_name), None)
        if selected_supplier:
            self.selected_supplier_name = selected_supplier['name']
            self.selected_supplier_id = selected_supplier['id']
            self.selected_dn_type_label.config(text=f"{self.selected_supplier_name} (ID: {self.selected_supplier_id})")
            self.display_annotations()

    def display_annotations(self):
        for widget in self.annotations_frame.winfo_children():
            widget.destroy()

        self.data_type_comboboxes.clear()
        self.type_entries.clear()
        self.bboxes.clear()

        annotations = get_annotations_by_supplier(self.coco_data, self.selected_supplier_id)
        for annotation_key, annotation in annotations.items():
            if annotation['supplier_id'] == self.selected_supplier_id:
                annotation_frame = tk.Frame(self.annotations_frame, bg='lightgrey')
                annotation_frame.pack(pady=2, fill=tk.X)

                id_label = ttk.Label(annotation_frame, text=f"{annotation_key}")
                id_label.pack(side=tk.LEFT, padx=5)

                data_type_combobox = ttk.Combobox(annotation_frame, values=["en", "ch_tra"], width=6)
                data_type_combobox.set(annotation['data_type'])
                data_type_combobox.pack(side=tk.LEFT, padx=5)
                self.data_type_comboboxes[annotation_key] = data_type_combobox

                type_entry = ttk.Entry(annotation_frame, width=20)
                type_entry.insert(0, annotation['type'])
                type_entry.pack(side=tk.LEFT, padx=5)
                self.type_entries[annotation_key] = type_entry

                # Initialize bounding boxes
                self.init_bounding_box(annotation['bbox'], annotation_key)

        # Update the image with bounding boxes
        self.update_image_with_bboxes()

    def save_ocr_settings(self):
        for annotation_key, annotation in self.coco_data['annotations'].items():
            if annotation['supplier_id'] == self.selected_supplier_id:
                annotation_key_str = str(annotation_key)
                new_data_type = f"[{self.data_type_comboboxes[annotation_key_str].get()}]"
                new_type = self.type_entries[annotation_key_str].get()
                update_annotation(self.coco_data['annotations'], annotation_key_str, new_data_type, new_type)
        # Save the updated coco_data to the file
        save_to_coco_file(self.coco_data, 'annotations.coco')

        # Display a message box indicating that changes have been saved
        messagebox.showinfo("Save OCR Settings", "Changes have been saved successfully.")

    def drop(self, event):
        pdf_path = event.data.strip('{}')
        if pdf_path.endswith('.pdf'):
            self.display_pdf_image(pdf_path)

    def display_pdf_image(self, pdf_path):
        output_folder = os.path.dirname(pdf_path)
        output_image_name = 'output_image.jpg'
        image_path = pdf_to_image(pdf_path, output_folder, output_image_name)

        self.image = Image.open(image_path)
        self.original_width, self.original_height = self.image.size

        # Resize image if it exceeds the maximum allowed dimensions
        if self.image.width > self.max_image_width or self.image.height > self.max_image_height:
            self.image.thumbnail((self.max_image_width, self.max_image_height))

        self.resized_width, self.resized_height = self.image.size

        # Calculate the width and height ratios
        self.width_ratio = self.resized_width / self.original_width
        self.height_ratio = self.resized_height / self.original_height

        self.photo = ImageTk.PhotoImage(self.image)

        # Resize the main window to fit the new dimensions
        new_window_width = self.resized_width + self.ocr_panel_width  # Adding some padding
        new_window_height = self.resized_height + 50  # Adding some padding
        self.root.geometry(f"{new_window_width}x{new_window_height}")

        # Resize pdf_panel and canvas to fit the image
        self.pdf_panel.config(width=self.resized_width, height=self.resized_height)
        self.canvas.place(x=0, y=0, width=self.resized_width, height=self.resized_height)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)


    def init_bounding_box(self, bbox, annotation_key):
        x1, y1 = bbox[0]
        x2, y2 = bbox[1]
        x1 = int(x1 * self.width_ratio)
        y1 = int(y1 * self.height_ratio)
        x2 = int(x2 * self.width_ratio)
        y2 = int(y2 * self.height_ratio)

        # Store the bbox and annotation key
        self.bboxes.append({'bbox': [(x1, y1), (x2, y2)], 'key': annotation_key})

        # Bind mouse events for dragging
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        x, y = event.x, event.y
        for bbox_info in self.bboxes:
            x1, y1 = bbox_info['bbox'][0]
            x2, y2 = bbox_info['bbox'][1]

            # Check if the click is near the corners of the bbox
            if abs(x - x1) < 5 and abs(y - y1) < 5:
                self.dragging_corner = "top_left"
                self.current_bbox = bbox_info['bbox']
                self.current_annotation_key = bbox_info['key']
                break
            elif abs(x - x2) < 5 and abs(y - y2) < 5:
                self.dragging_corner = "bottom_right"
                self.current_bbox = bbox_info['bbox']
                self.current_annotation_key = bbox_info['key']
                break

    def on_drag(self, event):
        if self.dragging_corner:
            x, y = event.x, event.y

            # Ensure the coordinates are within the canvas boundaries
            x = max(0, min(x, self.resized_width))
            y = max(0, min(y, self.resized_height))

            if self.dragging_corner == "top_left":
                self.current_bbox[0] = (x, y)
            elif self.dragging_corner == "bottom_right":
                self.current_bbox[1] = (x, y)

            # Update the coordinates label
            x1, y1 = self.current_bbox[0]
            x2, y2 = self.current_bbox[1]
            self.coordinates_label.config(text=f"Coordinates: ({x1}, {y1}), ({x2}, {y2})")

            # calculate the original coordinates of the bbox on the original image
            self.update_image_with_bboxes()

    def on_release(self, event):
        if self.dragging_corner:
            # Update the annotation with the new bbox values
            x1, y1 = self.current_bbox[0]
            x2, y2 = self.current_bbox[1]
            x1 = int(x1 / self.width_ratio)
            y1 = int(y1 / self.height_ratio)
            x2 = int(x2 / self.width_ratio)
            y2 = int(y2 / self.height_ratio)
            new_bbox = [(x1, y1), (x2, y2)]
            update_annotation(self.coco_data['annotations'], self.current_annotation_key, bbox=new_bbox)
            self.dragging_corner = None
            self.current_annotation_key = None
            self.current_bbox = None

    def update_image_with_bboxes(self):
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)  # Redraw the image
        for bbox_info in self.bboxes:
            x1, y1 = bbox_info['bbox'][0]
            x2, y2 = bbox_info['bbox'][1]
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
            # Draw circles at the corners
            self.canvas.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill="blue")
            self.canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill="blue")

        if self.current_bbox:
            x1, y1 = self.current_bbox[0]
            x2, y2 = self.current_bbox[1]
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)  # Draw the current bbox in a different color


    def perform_ocr(self):
        for annotation_key, annotation in self.coco_data['annotations'].items():
            if annotation['supplier_id'] == self.selected_supplier_id:
                bbox = annotation['bbox']
                resized_bbox = [(int(bbox[0][0] * self.width_ratio), int(bbox[0][1] * self.height_ratio)),
                                (int(bbox[1][0] * self.width_ratio), int(bbox[1][1] * self.height_ratio))]
        ocr_results = crop_and_ocr_bboxes(self.image_path, [resized_bbox], self.width_ratio, self.height_ratio, [annotation['data_type']])
        self.display_ocr_results(annotation_key, ocr_results[0])

    def display_ocr_results(self, annotation_key, ocr_result):
        annotation_frame = self.annotations_frame.winfo_children()[annotation_key]
        ocr_textbox = tk.Text(annotation_frame, height=4, width=50)
        ocr_textbox.insert(tk.END, ocr_result)
        ocr_textbox.pack(pady=5)


if __name__ == "__main__":
    test_save_load_coco_file()

    root = TkinterDnD.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * window_to_screen_ratio_width)
    window_height = int(screen_height * window_to_screen_ratio_height)
    max_image_width = int(screen_width * max_image_ratio)
    max_image_height = int(screen_height * max_image_ratio)
    root.geometry(f"{window_width}x{window_height}")  # Set the dimensions of the main window
    app = PDFToImageApp(root, window_width, window_height, max_image_width, max_image_height)
    root.mainloop()
