GenAI Bench

##Models supported
###Text-to-image

###Text-to-video

##Get started: 
1. ```bash
git clone https://github.com/emilyjiayaoli/GenAI-Bench.git
cd GenAI-Bench


# Setup environment & install requirements
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Rename `.env_example` to `.env` and fill in the environment variables

3. Special setup instructions:
- Midjourney: since Midjourney has no API support, you will need to host your own discord server, we use [this](https://github.com/novicezk/midjourney-proxy) and Railway. Once the server is hosted, please define the environment variable `MJ_SERVER_URL` in `.env` to be the host url.
- For DALLE-x series, please populate the environment variable `OAI_KEY` in `.env` with your OpenAI API key.


4. Run tests: In the root directory, run
```
python -m tests.test_img_models
python -m tests.test_video_models
```


Todos:
- save videos right for video models