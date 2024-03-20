# GenAI Bench

## Models supported
### Text-to-image
- [DALLE-x](https://openai.com/dall-e-3)
- [Deepfloyd_I_XL_v1](https://huggingface.co/DeepFloyd/IF-I-XL-v1.0)
- [Midjourney vx](https://www.midjourney.com/home)
- [SDXL 2.1](https://huggingface.co/stabilityai/stable-diffusion-2-1)
- [SDXL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
- [SDXL Turbo](https://huggingface.co/stabilityai/sdxl-turbo)
### Text-to-video
- [Modelscope](https://huggingface.co/ali-vilab/modelscope-damo-text-to-video-synthesis)
- [Zeroscope](https://huggingface.co/cerspense/zeroscope_v2_576w)

## Get started
1. Clone the repository and set up the environment:
    ```bash
    git clone https://github.com/emilyjiayaoli/t2visual-gen.git
    cd t2visual-gen

    # Setup environment & install requirements
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Rename `.env_example` to `.env` and fill in the environment variables.

3. Special setup instructions:
   - **Midjourney**: since Midjourney has no API support, you will need to host your own discord server. Use [this proxy](https://github.com/novicezk/midjourney-proxy) and Railway for hosting. Once the server is hosted, define the environment variable `MJ_SERVER_URL` in `.env` to be the host URL.
   - **For DALLE-x series**: populate the environment variable `OAI_KEY` in `.env` with your OpenAI API key.
   - **DeepFloyd IF-I-XL-v1.0** is a gated model. You must log in to huggingface and accept the license agreement by going [here](https://huggingface.co/DeepFloyd/IF-I-XL-v1.0).

4. Run tests: In the root directory, run the following. Feel free to comment out select test cases in `test_all()`
    ```bash
    python -m tests.test_img_models
    python -m tests.test_video_models
    ```

5. Batch generation: 
   1. Prepare a json file in `data/` storing all the prompts in the following format: a list of json objects with "id" and "prompt" key.
   ```json
   [
    {
        "id": "00001",
        "prompt": "A baker pulling freshly baked bread out of an oven in a bakery.",
    },
    ...
    ]
   ```
   2. Edit [generate_images.py](./generate_images.py) or [generate_images.py](./generate_videos.py). This looks like
    ```python
    MODEL = "Midjourney" # Change me
    prompt_path = "./data/t2v_prompts.json" # Change me: Path to your json prompt file
    DEVICE, type = detect_device()

    if MODEL == "Midjourney":
        MJ_SERVER_URL = os.getenv("MJ_SERVER_URL") 
    
    generate(model_name=MODEL, output_folder_path=f"./output/{MODEL}", prompts_path=prompt_path)
    ```
   3. In the root directory, run the generation files
    ```bash 
    python generate_{images,videos}.py
    ```


### Todos:
- save videos correctly for video models
- finish readme & writing instructions
- add table for gpu/cpu/mps support, run tests on cpu