import tkinter as tk
from tkinter import filedialog


def open_file_explorer(title="Select a file", filetypes=None):
    if filetypes is None:
        filetypes = [("All files", "*.*")]
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

# Example usage, works as expected
'''
def test_open_file_explorer():
    file_path = open_file_explorer(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    print(f"Selected file: {file_path}")
    
test_open_file_explorer()
'''

def open_folder_explorer(title="Select a folder"):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title=title)
    root.destroy()  # Destroy the root window
    return folder_path

# Example usage, works as expected
'''
selected_folder = open_folder_explorer()
print(f"Selected folder: {selected_folder}")
'''