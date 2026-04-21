# https://www.youtube.com/watch?v=1h6lfzJ0wZw&t=677s
# New changes in the API require you to study the site and use the newest
# parameters.

from transformers import pipeline
import torch

# print(torch.cuda.is_available())
# print(torch.cuda.get_device_name(0))

# This downloads and caches the model automatically on the first run
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

result = classifier("I love using Hugging Face models!")
print(result)

# (.venv)
# activate and install dependencies
# pip install transformers torch accelerate
# python -m agents.hugface.techwtim.basic

# outputs
# [{'label': 'POSITIVE', 'score': 0.9992625117301941}]
