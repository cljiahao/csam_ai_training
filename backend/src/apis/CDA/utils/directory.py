import os


class Directory:
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
    image_path = os.path.join(base_path, "images")
    dataset_path = os.path.join(image_path, "dataset")
    raw_path = os.path.join(image_path, "raw")


directory = Directory
