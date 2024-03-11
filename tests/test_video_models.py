from models.t2video import get_model_class, print_all_model_names
from utils import detect_device
import os
from dotenv import load_dotenv
load_dotenv()

SAVE_PATH = os.path.join(os.getenv("SAVE_PATH"), "vids")

def test_zeroscope(device:str): # Running on CPU is not supported
    print("Initializing ZeroScope...", end="")
    model = get_model_class('ZeroScope')(device=device)
    print("Done.")
    save_path = model.generate(prompt="two people; the one on the right has long hair and the one on the left doesn't.", folder_path="./", filename="zeroscope-video.mp4")
    print("Done. Video saved at", save_path)

def test_modelscope(): # Running on CPU is not supported
    print("Initializing ModelScope...", end="")
    model = get_model_class('ModelScope')()
    print("Done.")
    save_path = model.generate(text_prompt="A red apple on a table", folder_path="./", filename="modelscope-video.mp4")
    print("Done. Video saved at", save_path)


def test_all():
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    DEVICE, type = detect_device()
    
    test_zeroscope(device='cpu') # doesn't work on mps
    test_modelscope()


if __name__ == "__main__":
    print_all_model_names()
    test_all()