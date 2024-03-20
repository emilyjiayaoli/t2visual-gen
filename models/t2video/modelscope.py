import pathlib
from huggingface_hub import snapshot_download
from ..base_model import BaseModel
from modelscope.pipelines import pipeline
from modelscope.outputs import OutputKeys
import os
import shutil
import torch
from dotenv import load_dotenv
load_dotenv()

TRANSFORMERS_CACHE = os.getenv("TRANSFORMERS_CACHE")
# os.environ["CUDA_VISIBLE_DEVICES"] = os.getenv("CUDA_VISIBLE_DEVICES")  # Specify the GPU device ID to use.

class ModelScope(BaseModel):
    """
    ModelScopeDamo
    This class facilitates generating videos from textual descriptions using the ModelScope-DAMO model,
    hosted on Hugging Face's model hub at:
    https://huggingface.co/ali-vilab/modelscope-damo-text-to-video-synthesis
    """
    def __init__(self, device:str):
        """
        Initializes the ModelScope class by downloading the model weights and setting up the pipeline.

        Parameters:
        - device: The computing device ('cpu' or 'cuda') for the model to run on. Defaults to 'cuda'.
        """
        if "cuda" not in device:
            raise ValueError("ModelScope only supports CUDA devices.")
        
        # Define the directory to store model weights.
        model_dir = pathlib.Path(os.path.join(TRANSFORMERS_CACHE, 'modelscope_weights'))
        
        # Download model weights to the specified directory.
        snapshot_download('damo-vilab/modelscope-damo-text-to-video-synthesis', 
                          repo_type='model', local_dir=model_dir)

        # Initialize the pipeline with the model directory.
        self.pipe = pipeline('text-to-video-synthesis', model_dir.as_posix())

    def generate(self, prompt, folder_path="./", filename="modelscope_video.mp4"):
        """
        Generates a video based on the provided textual prompt and saves it to the specified location.

        Parameters:
        - prompt: The textual prompt to guide video generation.
        - folder_path: The directory path where the generated video will be saved. Defaults to './'.
        - filename: The filename for the saved video. Defaults to 'modelscope_video.mp4'.

        Returns:
        The path to the saved video file.
        """
        # Package the prompt into the expected input format.
        test_text = {'text': prompt}
        
        # Generate the video.
        output = self.pipe(test_text)
        output_video_path = output[OutputKeys.OUTPUT_VIDEO]

        final_path = pathlib.Path(folder_path) / filename
        
        # Move the generated video file to the desired location.
        if pathlib.Path(output_video_path).exists():
            shutil.move(output_video_path, final_path)
        else:
            print(f'Error: Generated video not found at {output_video_path}')

        # Log the final path of the generated video.
        print(f'Generated video path: {final_path}')
        return final_path.as_posix()