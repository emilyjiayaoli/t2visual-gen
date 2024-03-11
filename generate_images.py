import json
import os
from utils import detect_device
from models.t2image import get_model_class, print_all_model_names

def load_prompts_dict(path):
    with open(path, "r") as f:
        return json.load(f)
    
def get_model(name):
    if name == "DALLE":
        return get_model_class('DALLE')(OAI_KEY, version=3)
    elif name == "DeepFloyd_I_XL_v1":
        return get_model_class('DeepFloyd_I_XL_v1')()
    elif name == "Midjourney":
        args = {
            'version': 6.0,
        }
        return get_model_class('Midjourney')(MJ_SERVER_URL, **args)
    elif name == "SDXL_Turbo":
        return get_model_class('SDXL_Turbo')(device=DEVICE)
    elif name == "SDXL_Base":
        return get_model_class('SDXL_Base')(device=DEVICE)
    elif name == "SDXL_2_1":
        return get_model_class('SDXL_2_1')(device=DEVICE)
    else:
        raise ValueError(f"Model {name} not found")


def generate(model_name:str, prompts_path:str, output_folder_path="./", start_idx=None, end_idx=None):

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    folder_path = os.path.join(output_folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    model = get_model(model_name)
    
    log = {}
    print("Loading model...")
    prompts = load_prompts_dict(prompts_path)
    print("Done.")
    prompts = prompts[start_idx:end_idx] if start_idx is not None and end_idx is not None else prompts

    for prompt in prompts:
        print("Prompt:", prompt["prompt"])

        prompt_data = {}
        id = prompt["id"]
        prompt = prompt["prompt"]

        filename = f"{id}.jpeg"

        prompt_data["id"] = id
        prompt_data["prompt"] = prompt

        save_path = model.generate(text_prompt=prompt, 
                                   folder_path=folder_path, 
                                   filename=filename)
        
        if save_path is not None:
            prompt_data["image_path"] = save_path
            log[id] = prompt_data

    #update log.json
    with open(os.path.join(output_folder_path, "log.json"), "w") as f:
        json.dump(log, f, indent=4)
        

if __name__ == '__main__':
    MODEL = "Midjourney" # Change me
    prompt_path = "./data/t2v_prompts.json" # Change me


    OAI_KEY = os.getenv("OAI_KEY")
    DEVICE, type = detect_device()

    if MODEL == "Midjourney":
        MJ_SERVER_URL = os.getenv("MJ_SERVER_URL") 
    
    generate(model_name=MODEL, output_folder_path=f"./output/{MODEL}", prompts_path=prompt_path)

