# https://www.youtube.com/watch?v=UtSSMs6ObqY

import ollama

# Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "llama2"
prompt = "What sevice could I make with an AI agent that will make me a millionaire?"

# Send the query to the model
response= client.generate(model=model, prompt=prompt)

# Print the response from the model
print("Response from Ollama:")
print(response.response)

# https://ollama.com/download
# (.venv)
# activate and install dependencies
# pip install ollama
# python -m agents.ollama.ollama_client
