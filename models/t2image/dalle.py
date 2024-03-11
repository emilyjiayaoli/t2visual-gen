"""
This file defines the Dalle class, which integrates with OpenAI's DALL-E API to generate images based on text prompts.
"""

from typing import Optional
from openai import OpenAI
from ..base_model import BaseModel
import os
import requests 

class DALLE(BaseModel):
    def __init__(self, openai_api_key:str, version:int, usr_provided_prompt:Optional[str]=None):
        """
        Initializes the DALLE class with the provided OpenAI API key, version, and an optional user-provided prompt.
        
        Parameters:
        - openai_api_key: The API key to be used for the OpenAI API.
        - version: The version of DALL-E to be used. Must be 2 or 3.
        - usr_provided_prompt: If provided, it will be used as the prompt for the generation, excluding sample specific caption.
        """

        if version == 3 or version == 2: 
            self.version = version
        else:
            raise ValueError("Version must be 2 or 3.")

        self.client = OpenAI(api_key=openai_api_key) 

        # Setting up the prompt
        if usr_provided_prompt:
            self.set_prompt(usr_provided_prompt)
        else: # Default prompt suggested by OpenAI
            default_prompt = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS. "
            default_prompt += "Generate a realistic image with text_prompt: "
            self.set_prompt(default_prompt)

    def set_prompt(self, prompt):
        """
        Sets the prompt for the DALLE class.
        
        Parameters:
        - prompt: The prompt to be set.
        """
        self.prompt = prompt

    def get_dalle_prompt(self, text_prompt):
        """
        Returns the complete prompt by appending the provided text prompt to the class's prompt.
        
        Parameters:
        - text_prompt: The text prompt to append.
        """
        return self.prompt + text_prompt

    def reset_api_key(self, new_api_key):
        """
        Resets the OpenAI API key for the DALLE class.
        
        Parameters:
        - new_api_key: The new API key to be set.
        """
        self.client = OpenAI(api_key=new_api_key)

    def _call_dalle_api_helper(self, prompt, **kwargs):
        """
        Helper function to call the DALL-E API with the provided prompt and additional arguments.
        
        Parameters:
        - prompt: The prompt to be used for the API call.
        - kwargs: Additional arguments to be passed to the API call, e.g., size, quality, n.
        """
        # Setting default values
        size = kwargs.get("size", "1024x1024")
        quality = kwargs.get("quality", "standard")
        n = kwargs.get("n", 1)
        
        response = self.client.images.generate(
            model=f"dall-e-{self.version}",
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
        )
        return response
    
    def generate(self, text_prompt:str, folder_path:str="./", filename:str="dalle-image.jpeg", download:bool=True, **kwargs):
        """ 
        Generates an image from a given text prompt using the DALL-E API and optionally downloads it.
        
        Parameters:
        - text_prompt: The text prompt to be used for the generation.
        - folder_path: The folder path where the image will be downloaded.
        - filename: The name of the downloaded image + filetype, e.g., 'image.jpg'.
        - download: If True, the generated image will be downloaded to the specified folder.
        - kwargs: Additional arguments to be passed to the API call, e.g., size, quality, n.
        
        Returns:
        - The URL of the generated image, or None if an error occurred.
        """
        # Validating parameters for download
        if download:
            assert folder_path is not None, "folder_path must be provided when download is True."
            assert filename is not None, "filename must be provided when download is True."

        prompt = self.get_dalle_prompt(text_prompt)
        dalle_response = self._call_dalle_api_helper(prompt, **kwargs)

        self.recent_dalle_response = dalle_response

        if 'errors' in vars(dalle_response).keys():
            print("Error occurred. Response:", dalle_response)
            return None

        image_url = dalle_response.data[0].url

        if download:
            return self.download_image(image_url, folder_path, filename)
        else:   
            print(f"Generated image: {image_url}")
            return image_url
    

    
    def download_image(self, image_url:str, folder_path:str, filename:str):
        """
        Downloads an image from a given URL to a specified file path.
        
        Parameters:
        - image_url: URL of the image to download.
        - folder_path: The folder path where the image will be saved.
        - filename: The name of the file to save the image as.
        """
        # Checking if the folder exists, if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        save_path = os.path.join(folder_path, filename)
        
        response = requests.get(image_url) # Sending a GET request to the image URL

        # Saving the image if the request was successful
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return save_path
        else:
            print(f"Failed to download the image. Status code: {response.status_code}")
            return None
