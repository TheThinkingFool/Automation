# Monthly Progress Photo Generator

This Python program generates a DOCX file with photos and their corresponding details, such as location, title, reference number, date, time, and weather conditions. The program extracts variables from image filenames, generates random dates and times, processes images, and replaces placeholders in a DOCX template.

## Features

- Extracts variables from image filenames.
- Generates random dates and times for each photo.
- Replaces photos and variables in a DOCX template with actual values and correct styles.

## Installation

Install the required libraries:
    ```sh
    pip install python-docx Pillow
    ```
    ``` pip install python-docx```
   ``` pip install tkinter```

## Usage

1. Run the main script:
    ```sh
    python main.py
    ```

2. Follow the prompts to select the folder containing photos and the DOCX template file.

## File Structure

- `main.py`: The main script to run the program.
- `extract_image_variables.py`: Extracts variables from image filenames.
- `generate_date_time.py`: Generates random dates and times for each photo.
- `generate_images_with_datetime.py`: Processes images to include date and time.
- `write/generate_doc.py`: Replaces photos and variables in the DOCX file.

## Image Filename Format

The image filenames should follow the format:
```
$ref_no$_$location$_$title$_$weather_condition$.jpg
```
or
```
$ref_no$_$location$_$title$.jpg
```
(Default weather condition is "FINE")

## Example

1. Select a folder containing photos.
![image](https://github.com/user-attachments/assets/6aebf2c4-601a-4475-82ce-eecf29a528e5)
2. Input the MM/YYYY.
![image](https://github.com/user-attachments/assets/2a121906-7b96-49b8-bc0e-6602a83b4692)
3. Select a folder to store images generated with date and time.
![image](https://github.com/user-attachments/assets/461f2619-9c28-42c9-8797-60b9f1526834)
4. Select a DOCX template file. (template 4R.docx)
5. The program will generate a new DOCX file with the updated values.
```output_path = f"Monthly Progress Photos_{month_year}"```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
Nah there is no license LMAO. See what github copilot generated. Is it developed by MIT?

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
