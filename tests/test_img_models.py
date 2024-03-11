from models.t2image import get_model_class, print_all_model_names
from utils import detect_device
import os
from dotenv import load_dotenv
load_dotenv()

SAVE_PATH = os.path.join(os.getenv("SAVE_PATH"), "imgs")

def test_dalle(openai_api_key:str):
    print("Initializing DALLE...", end="")
    model = get_model_class('DALLE')(openai_api_key, version=3) # DALLE-3
    print("Done.")

    print("--Testing DALLE-3...", end="")
    save_path = model.generate(text_prompt="A red apple on a table", folder_path=SAVE_PATH, filename="dalle3-image-test.jpeg", download=True, size="1024x1024")
    print("Done. Image saved at", save_path)

    print("Initializing DALLE2...", end="")
    model = get_model_class('DALLE')(openai_api_key, version=2) # DALLE-2
    print("Done.")

    print("--Testing DALLE-2...", end="")    
    save_path = model.generate(text_prompt="A red apple on a table", folder_path=SAVE_PATH, filename="dalle2-image-test.jpeg", download=True, size="512x512", version=2)
    print("Done. Image saved at", save_path)

def test_midjourney(host_url:str):
    print("Initializing Midjourney v5...", end="")
    args = {
        'version': 6.0,
    }
    model = get_model_class('Midjourney')(host_url, **args)
    print("Done.")

    print("--Testing Midjourney...", end="")
    save_path = model.generate(text_prompt="A red apple on a table", folder_path=SAVE_PATH, filename="mj-image-test.jpeg", download=True)
    print("Done. Image saved at", save_path)

def test_deepfloyd(device:str): # Running on CPU is not supported

    print("Initializing DeepFloyd_I_XL_v1...", end="")
    model = get_model_class('DeepFloyd_I_XL_v1')(device=device)
    print("Done.")

    print("--Testing DeepFloyd...", end="")
    save_path = model.generate(text_prompt="A red apple on a table", folder_path=SAVE_PATH, filename="df-image-test.jpeg")
    print("Done. Image saved at", save_path)


def test_sdxl_turbo(device:str): # Running on CPU is not supported
    print("Initializing SDXL_Turbo...", end="")
    model = get_model_class('SDXL_Turbo')(device=device)
    print("Done.")

    print("--Testing SDXL_Turbo...", end="")
    save_path = model.generate(text_prompt="A red apple on a table", folder_path=SAVE_PATH, filename="sdxl-turbo-image-test.jpeg")
    print("Done. Image saved at", save_path)

def test_sdxl_base(device:str): # Running on CPU is not supported
    print("Initializing SDXL...", end="")
    model = get_model_class('SDXL_Base')(device=device)
    print("Done.")
    save_path = model.generate(text_prompt="A red apple on a table", folder_path=SAVE_PATH, filename="sdxl-base-image-test.jpeg")
    print("Done. Image saved at", save_path)

def test_sdxl_2_1(device:str): # Running on CPU is not supported
    print("Initializing SDXL...", end="")
    model = get_model_class('SDXL_2_1')(device=device)
    print("Done.")
    save_path = model.generate(text_prompt="A red apple on a table", folder_path=SAVE_PATH, filename="sdxl-2-1-image-test.jpeg")
    print("Done. Image saved at", save_path)


def test_all():
    OAI_KEY = os.getenv("OAI_KEY")
    MJ_SERVER_URL = os.getenv("MJ_SERVER_URL")
    DEVICE, type = detect_device()

    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    test_dalle(openai_api_key=OAI_KEY)
    test_midjourney(host_url=MJ_SERVER_URL)
    test_deepfloyd(device=DEVICE)
    test_sdxl_turbo(device=DEVICE)
    test_sdxl_base(device=DEVICE)
    test_sdxl_2_1(device=DEVICE)


if __name__ == "__main__":
    print_all_model_names()
    test_all()