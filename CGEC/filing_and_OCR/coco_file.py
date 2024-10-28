"""
standard format of dictionary of annotations stored in a coco file:
"suppliers": [
    {"id": 1, "name": "Supplier A"},
    {"id": 2, "name": "Supplier B"}
],
"annotations": {
    1: {"supplier_id": 1, "type": "date", "data_type": ["en"], "bbox": [[0, 0], [50, 50]] },
    2: {"supplier_id": 1, "type": "name", "data_type": ["en"], "bbox": [[60, 60], [120, 120]] },
    3: {"supplier_id": 2, "type": "date", "data_type": ["en"], "bbox": [[10, 10], [60, 60]] },
    4: {"supplier_id": 2, "type": "name", "data_type": ["ch_tra"], "bbox": [[70, 70], [130, 130]] }
}
"""

import json


def save_to_coco_file(coco_data, file_path):
    """
    Save the dictionary to a .coco file format.

    :param coco_data: Dictionary containing COCO data.
    :param file_path: Path to the .coco file.
    """

    with open(file_path, 'w') as file:
        json.dump(coco_data, file, indent=4)

def load_coco_file(file_path):
    """
    Read the dictionary from a .coco file format and create a mapping of annotation IDs to annotations.

    :param file_path: Path to the .coco file.
    :return: Dictionary containing COCO data and a mapping of annotation IDs to annotations.
    """
    with open(file_path, 'r') as file:
        coco_data = json.load(file)

    return coco_data
# Example usage of save_to_coco_file and load_coco_file, works as expected
def test_save_load_coco_file():
    coco_data = {
        "suppliers": [
            {"id": 1, "name": "Supplier A"},
            {"id": 2, "name": "Supplier B"}
        ],
        "annotations": {
            1: {"supplier_id": 1, "type": "date", "data_type": ["en"], "bbox": [[0, 0], [50, 50]] },
            2: {"supplier_id": 1, "type": "name", "data_type": ["en"], "bbox": [[60, 60], [120, 120]] },
            3: {"supplier_id": 2, "type": "date", "data_type": ["en"], "bbox": [[10, 10], [60, 60]] },
            4: {"supplier_id": 2, "type": "name", "data_type": ["ch_tra"], "bbox": [[70, 70], [130, 130]] }
        }
    }

    # Save to .coco file
    file_path = 'annotations.coco'
    save_to_coco_file(coco_data, file_path)

    # Read from .coco file
    loaded_coco_data = load_coco_file(file_path)
    print(loaded_coco_data)
#  test_save_load_coco_file()

def add_annotation_to_dict(coco_data, supplier_id, annotation_type, bbox, data_type='en'):
    """
        Add an annotation to the dictionary for a specific supplier.

        :param coco_data: Dictionary containing COCO data.
        :param supplier_id: ID of the supplier.
        :param annotation_type: Type of the annotation (e.g., 'date', 'name').
        :param bbox: Bounding box for the annotation in the format [[x1, y1], [x2, y2]].
        :param data_type: Data type of the annotation (default is 'en' (English), choose 'ch_tra' for Chinese).
        """
    # Find the next available annotation ID
    existing_ids = set(coco_data['annotations'].keys())
    next_id = next(i for i in range(1, len(existing_ids) + 2) if str(i) not in existing_ids)

    # Create the new annotation
    new_annotation = {
        "supplier_id": supplier_id,
        "type": annotation_type,
        "data_type": [data_type],
        "bbox": bbox
    }

    # Add the new annotation to the dictionary
    coco_data['annotations'][str(next_id)] = new_annotation
# Example usage of add_annotation_to_dict, works as expected
def test_add_annotation_to_dict():
    test_save_load_coco_file()
    file_path = 'annotations.coco'
    coco_data = load_coco_file(file_path)
    add_annotation_to_dict(coco_data, 2, 'location', [[80, 80], [140, 140]])
    save_to_coco_file(coco_data, file_path)
    print(load_coco_file(file_path))


def delete_annotation_from_dict(coco_data, annotation_id):
    """
    Delete an annotation from the dictionary by its ID.

    :param coco_data: Dictionary containing COCO data.
    :param annotation_id: ID of the annotation to be deleted.
    """
    del coco_data['annotations'][str(annotation_id)]
# Example usage of delete_annotation_from_dict, works as expected
def test_delete_annotation_from_dict():
    test_save_load_coco_file()
    file_path = 'annotations.coco'
    coco_data = load_coco_file(file_path)
    delete_annotation_from_dict(coco_data, 1)
    save_to_coco_file(coco_data, file_path)
    print(load_coco_file(file_path))


def add_supplier_to_dict(coco_data, supplier_name):
    """
    Add a supplier to the dictionary.

    :param coco_data: Dictionary containing COCO data.
    :param supplier_name: Name of the supplier to be added.
    """
    # Find the next available supplier ID
    existing_ids = {supplier['id'] for supplier in coco_data['suppliers']}
    next_id = next(i for i in range(1, len(existing_ids) + 2) if i not in existing_ids)

    # Create the new supplier
    new_supplier = {
        "id": next_id,
        "name": supplier_name
    }

    # Add the new supplier to the list
    coco_data['suppliers'].append(new_supplier)
# Example usage of add_supplier_to_coco, works as expected
def test_add_supplier_to_dict():
    test_save_load_coco_file()
    file_path = 'annotations.coco'
    coco_data = load_coco_file(file_path)
    add_supplier_to_dict(coco_data, 'Supplier C')
    save_to_coco_file(coco_data, file_path)
    print(load_coco_file(file_path))


def delete_supplier_from_dict(coco_data, supplier_id):
    """
    Delete a supplier and its annotations from the dictionary by its ID.

    :param coco_data: Dictionary containing COCO data.
    :param supplier_id: ID of the supplier to be deleted.
    """
    # Remove the supplier with the specified ID
    coco_data['suppliers'] = [supplier for supplier in coco_data['suppliers'] if supplier['id'] != supplier_id]

    # Remove annotations associated with the supplier
    coco_data['annotations'] = {id: annotation for id, annotation in coco_data['annotations'].items() if annotation['supplier_id'] != supplier_id}
# Example usage of delete_supplier_from_coco, works as expected
def test_delete_supplier_from_dict():
    test_save_load_coco_file()
    file_path = 'annotations.coco'
    coco_data = load_coco_file(file_path)
    supplier_id = 1  # ID of the supplier to delete
    delete_supplier_from_dict(coco_data, supplier_id)
    save_to_coco_file(coco_data, file_path)
    print(load_coco_file(file_path))


def get_annotations_by_supplier(coco_data, supplier_id):
    """
    Get all annotations for a specific supplier from the COCO data dictionary.

    :param coco_data: Dictionary containing COCO data.
    :param supplier_id: ID of the supplier.
    :return: List of annotations for the supplier.
    """
    # Filter annotations by supplier ID
    annotations = {key: annotation for key, annotation in coco_data['annotations'].items()
                   if annotation['supplier_id'] == supplier_id}
    return annotations
# Example usage of get_annotations_by_supplier, works as expected
def test_get_annotations_by_supplier():
    test_save_load_coco_file()
    file_path = 'annotations.coco'
    coco_data = load_coco_file(file_path)
    supplier_id = 1  # ID of the supplier
    annotations = get_annotations_by_supplier(coco_data, supplier_id)
    print(annotations)

def update_annotation(coco_data, annotation_id, new_data_type=None, new_type=None, bbox=None):
    """
    Update a single annotation in the COCO data.

    :param coco_data: The COCO data dictionary.
    :param annotation_id: The ID of the annotation to update.
    :param new_data_type: The new data type for the annotation.
    :param new_type: The new type for the annotation.
    """
    if new_data_type is not None:
        coco_data[annotation_id]['data_type'] = new_data_type

    if new_type is not None:
        coco_data[annotation_id]['type'] = new_type

    if bbox is not None:
        coco_data[annotation_id]['bbox'] = bbox
# Example usage of update_annotation, works as expected
def test_update_annotation():
    test_save_load_coco_file()
    file_path = 'annotations.coco'
    coco_data = load_coco_file(file_path)
    annotation_id = '1'
    new_data_type = ['ch_tra']
    new_type = 'location'
    update_annotation(coco_data['annotations'], annotation_id, new_data_type, new_type)
    save_to_coco_file(coco_data, file_path)
    print(load_coco_file(file_path))

