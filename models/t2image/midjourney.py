""" 
This file defines the Midjourney class, which is used to generate images from text prompts by calling the Midjourney API.

Midjourney
    Since there is no public API for Midjourney, we use this repo: https://github.com/novicezk/midjourney-proxy
    Please follow the server setup instructions there to make requests.

    Interface:
        - generate(text_prompt): generates an image using Dalle3 from the given text_prompt, returns the image url.
        - reset_api_key(new_api_key): resets the API key to a new one.
        - set_prompt(prompt): sets the prompt to be used for the generation.
        - get_dalle_3_prompt(text_prompt): returns the prompt to be used for the generation.
"""

import os
import requests 
from urllib.parse import urljoin
from ..base_model import BaseModel
import time

class Midjourney(BaseModel):
    def __init__(self, host_url, **kwargs):
        """
        Initialize the Midjourney instance.

        Parameters:
        - host_url: The base URL of the Midjourney API.
        - kwargs: Additional parameters for API requests, to be concatenated with the prompt.
        """
        self.host_url = host_url
        
        # Store additional parameters for concatenation with the prompt
        self.additional_params = " ".join(f"--{key} {value}" for key, value in kwargs.items())


    def set_prompt(self, prompt):
        """
        Set the prompt for the API request, including additional parameters.

        Parameters:
        - prompt: The prompt to be set.
        """
        self.prompt = prompt + " " + self.additional_params
    
    def call_submit_imagine_task_api(self, prompt):
        """
        Make a call to the Midjourney API with the configured prompt.

        Return: Response from the API call.
        """
        self.set_prompt(prompt)

        submit_imagine_endpoint = "mj/submit/imagine"
        submit_imagine_url = urljoin(self.host_url, submit_imagine_endpoint)
        
        body = {
            "prompt": self.prompt,
            "base64Array": [],
            "notifyHook": "",
            "state": "",
            "id":"17056193041129" # TODO: Placeholder
        }

        print("URL:", submit_imagine_url)
        print("Body:", body)

        response = requests.post(submit_imagine_url, json=body)
        return response.json()
    
    def call_task_status_api(self, task_id):
        """
        Make a call to the Midjourney API to check the status of a task.

        Parameters:
        - task_id: The ID of the task to check.
        Return: Response from the API call.
        """
        task_status_endpoint = f"mj/task/{task_id}/fetch"
        task_status_url = urljoin(self.host_url, task_status_endpoint)
        response = requests.get(task_status_url)

        return response.json()

    def call_task_status_list_api(self, task_id_list: list[str]):
        """
        Make a call to the Midjourney API to check the status of a list of tasks.

        :param task_id_list: The list of task IDs to check.
        :return: Response from the API call.
        """
        task_status_list_endpoint = "/mj/task/list-by-condition"
        task_status_list_url = urljoin(self.host_url, task_status_list_endpoint)
        body = {
            "ids": task_id_list
        }
        response = requests.post(task_status_list_url, json=body)

        return response.json()

    def process_submit_imagine_response(self, response):
        try: 
            if response["code"] == 1:
                id = response["result"]
                print(f"Task {id} submitted successfully.")
                return "SUBMITTED"
            elif response["code"] == 21:
                print("Task already exists.")
                return "ALREADY_EXISTS"
            elif response["code"] == 22:
                print("Task is in queue.")
                return "IN_QUEUE"
            else:
                print("Error submitting task. Response:", response)
                return "ERROR"
        except:
            print(response)
    
    def process_task_status_response(self, response, task_id):

        try:
            id = task_id
            if response["status"] == "SUCCESS":
                image_url = response["imageUrl"]
                print(f"Task ID {id} completed successfully. URL:", image_url)
                return "SUCCESS", image_url
            elif response["status"] == "IN_PROGRESS" or response["status"] == "SUBMITTED":
                print(f"Task ID {id} in progress. Check back later.")
                return "IN_PROGRESS", None
            elif response["status"] == "FAILURE":
                print(f"Task ID {id} failed. Reason", response["failureReason"])
                return "FAILURE", None
            else:
                print(f"Task ID {id} failed. Unknown status. Response", response)
                return "FAILURE", None
        except:
            print(response)
            return "FAILURE", None
        
    def process_task_status_list_response(self, response):
        image_urls = []
        for task in response["result"]:
            status, image_url = self.process_task_status_response(task, task["id"])
            if image_url is not None:
                image_urls.append(image_url)
        return image_urls
        
    def check_progress(self, task_id):
        while True:
            status_response = self.call_task_status_api(task_id)
            status, image_url = self.process_task_status_response(status_response, task_id)
            if status == "FAILURE":
                return status, None
            elif status == "SUCCESS":
                return status, image_url
            elif status == "IN_PROGRESS":
                print("Task in progress. Waiting 20 seconds...")
                time.sleep(20)
            else:
                print("Unknown status:", status)
                return status, None
    
    def generate(self, text_prompt, task_id=None, submit_only=False, folder_path="./", filename="mj-image.jpeg", download=True):

        """
        Generates an image from the given text prompt. 2 stages:
        1. Submit the task
        2. Check the status of the task and download the image if successful.

        Optional modes:
        - Specify 'task_id' to check the status of an existing task & download if 'download'=True. submit_only must be False.
        - Turn on 'submit_only' to submit a new task without checking the status and waiting for it to finish.
        """
        if download:
            assert folder_path is not None, "folder_path must be provided when download is True."
            assert filename is not None, "filename must be provided when download is True."

        # Submit the task
        if task_id is None:
            submit_response = self.call_submit_imagine_task_api(text_prompt)
            submission_status = self.process_submit_imagine_response(submit_response)
            if submission_status == "ERROR":
                return None
            try:
                task_id = submit_response["result"]
            except:
                print("Error submitting task. Response:", submit_response)
                return None

            print("status", submission_status, "submit_response", submit_response)
        else:
            assert submit_only is False, "submit_only must be False when task_id is provided."
        
        if submit_only:
            return f"Submitted only {task_id}"

        # Check the status of the task    
        status, image_url = self.check_progress(task_id)
        print("Status:", status, "Image URL:", image_url)
        
        if download and image_url is not None:
            return self.download_image(image_url, folder_path, filename)
        else:
            return image_url

    
    def download_image(self, image_url, folder_path, filename):
        """
        Saves an image from a given URL to a specified file path.

        Paremeter
        - image_url: URL of the image to download.
        """
        assert folder_path is not None, "folder_path must be provided when download is True."
        assert filename is not None, "filename must be provided when download is True."
        assert image_url is not None, "image_url must be provided when download is True."

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        save_path = os.path.join(folder_path, filename)
        if os.path.exists(save_path):
            print(f"Image already exists at {save_path}")
            return save_path
        
        response = requests.get(image_url) # Send a GET request to the image URL

        # Return image if the request was successful
        if response.status_code == 200:
            # Save the image
            with open(save_path, 'wb') as file:
                file.write(response.content)
            return save_path
        else:
            print(f"Failed to download the image. Status code: {response.status_code}")
            return None
        