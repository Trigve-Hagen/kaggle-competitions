import json
import pprint
import copy
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib import colors
from collections import Counter

import os
import numpy as np
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent
BASEPATH = script_dir / "dataset"

def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

training_challenges   = load_json(BASEPATH / 'arc-agi_training_challenges.json')
training_solutions    = load_json(BASEPATH / 'arc-agi_training_solutions.json')
evaluation_challenges = load_json(BASEPATH / 'arc-agi_evaluation_challenges.json')
evaluation_solutions  = load_json(BASEPATH / 'arc-agi_evaluation_solutions.json')
test_challenges       = load_json(BASEPATH / 'arc-agi_test_challenges.json')

p = pd.DataFrame(training_challenges)
# print(p.T.head(6))

task = training_challenges['007bbfb7']
# print(task)

pp = pprint.PrettyPrinter(indent=1)
# pp.pprint(task)

task = training_challenges['007bbfb7']['train']
# pp.pprint(task)

task = training_challenges['007bbfb7']['train'][0]['input']
# pp.pprint(task)

# Thus, we can dive to any level using the following construction:

# training_challenges[i][j][k][l],

# where:
# i - Name of task
# j - Train/test
# k - Number of instance
# l - Input/ouput

task = training_challenges['007bbfb7']['train'][1]
# pp.pprint(task)

# To get full list of keys there are two ways.
# Way #1: using keys()
# print(training_challenges.keys())

# Way #2: using list()
# List_Of_Task = list(training_challenges)
# print(List_Of_Task)

cmap = colors.ListedColormap(
   ['#000000', '#0074D9', '#FF4136', '#2ECC40', '#FFDC00',
    '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25', '#FFFFFF'])
norm = colors.Normalize(vmin=0, vmax=10)

def plot_one(ax, i, task, train_or_test, input_or_output):
    input_matrix = task[train_or_test][i][input_or_output]
    ax.imshow(input_matrix, cmap=cmap, norm=norm)
    ax.grid(True, which = 'both',color = 'lightgrey', linewidth = 0.5)
    plt.setp(plt.gcf().get_axes(), xticklabels=[], yticklabels=[])
    ax.set_xticks([x-0.5 for x in range(1 + len(input_matrix[0]))])
    ax.set_yticks([x-0.5 for x in range(1 + len(input_matrix))])
    ax.set_title(train_or_test + ' ' + input_or_output)

def plot_task(task1, text):
    num_train = len(task1['train'])

    w=num_train
    fig, axs  = plt.subplots(2, w, figsize=(3*w ,3*2))
    plt.suptitle(f'{text}:', fontsize=20, fontweight='bold', y=1)

    for j in range(num_train):
        plot_one(axs[0, j], j,task1,'train', 'input')
        plot_one(axs[1, j], j,task1,'train', 'output')

    fig.patch.set_linewidth(5)
    fig.patch.set_edgecolor('black')
    fig.patch.set_facecolor('#dddddd')
    plt.tight_layout()

    plt.show()








