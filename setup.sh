#!/bin/bash

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Run the sample.py script
# python tests/test_img_models.py
python -m tests.test_img_models