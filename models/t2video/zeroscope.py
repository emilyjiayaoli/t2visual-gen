"""
ZeroScope
    This class is used to generate videos from descriptions using the ZeroScope v2 model.
    https://huggingface.co/cerspense/zeroscope_v2_576w
"""

import os
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from ..base_model import BaseModel
from dotenv import load_dotenv
load_dotenv()
TRANSFORMERS_CACHE = os.getenv("TRANSFORMERS_CACHE")

class ZeroScope(BaseModel):
    """
    ZeroScope
    This class is used to generate videos from descriptions using the ZeroScope v2 model.
    https://huggingface.co/cerspense/zeroscope_v2_576w
    """
    def __init__(self, device:str, torch_dtype=torch.float16):
        self.pipe = DiffusionPipeline.from_pretrained("cerspense/zeroscope_v2_576w", torch_dtype=torch_dtype, cache_dir=TRANSFORMERS_CACHE)
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
        
        if device != "cpu":
            print(f"Moving model to GPU... device {device}")
            self.pipe.to(device)
        else:
            self.pipe.enable_model_cpu_offload()

    def generate(self, prompt, folder_path="./", filename="zeroscope-video.mp4", 
                  num_inference_steps=40, height=320, width=576, num_frames=24):
        
        video_frames = self.pipe(prompt=prompt, 
                                 num_inference_steps=num_inference_steps, 
                                 height=height, width=width, 
                                 ).frames[0]
        
        video_path = os.path.join(folder_path, filename)

        print(f"    Generating video with caption: {prompt}")
        export_to_video(video_frames, output_video_path=video_path)
        
        return video_path
