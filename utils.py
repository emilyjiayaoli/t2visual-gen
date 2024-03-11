import os
from PIL import Image
import torch

def detect_device():
    """
    Detects the appropriate device to run on, and return the device and dtype.
    """
    if torch.cuda.is_available():
        return torch.device("cuda"), torch.float16
    elif torch.backends.mps.is_available():
        return torch.device("mps"), torch.float16
    else:
        return torch.device("cpu"), torch.float32


def crop_for_left_top(input_folder, output_folder):
    """
    crop the left top of the image for the Midjourney images
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpeg"):  
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with Image.open(input_path) as img:
                width, height = img.size

                crop_img = img.crop((0, 0, width // 2, height // 2))
                crop_img.save(output_path)

# input_folder = "./imgs-batch2/Midjourney_orig"  
# output_folder = "./imgs-batch2/Midjourney"  
# crop_left_top(input_folder, output_folder)
