# https://www.kaggle.com/code/bovard/getting-started

import subprocess
try:
    # Recommended way to call subprocess
    output = subprocess.check_output(['cmake', '--version'], stderr=subprocess.STDOUT)
    print(output.decode())
except subprocess.CalledProcessError as e:
    print(f"Error: {e.output.decode()}")

# (.venv)
# activate and install dependencies
# pip install ollama
# python -m agents.orbit_wars.orbit_wars
