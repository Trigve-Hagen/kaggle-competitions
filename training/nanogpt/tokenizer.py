# https://www.youtube.com/watch?v=kCc8FmEb1nY&t=663s

import os
import tiktoken
import torch
import numpy as np

# goal: create a class to use for tokenizing.

# encoding will come from a file or ?..
# decoding will come from a prediction..

# torch
# SentencePiece
# ticktoken
# CharEncode

# path: a list of paths to trainins data
class Tokenizer:
  def __init__(self, path):
    self.path = path
    self.text = None
    self.tokens = None

  def getText(self):
    with open(self.path, 'r') as f:
      self.text = f.read()

  def encodeCharacters(self):
    self.getText()
    chars = sorted(list(set(self.text)))
    stoi = { ch:i for i,ch in enumerate(chars) }
    encoded = [stoi[c] for c in self.text] # encode takes a string, outputs a list of integers
    return encoded

  def decodeCharacters(self, data):
    chars = sorted(list(set(self.text)))
    itos = { i:ch for i,ch in enumerate(chars) }
    decoded = ''.join([itos[i] for i in data]) # encode takes integers, outputs a string
    return decoded

  def encodeWords(self):
    pass

  def decodeWords(self):
    pass

  def encodeSubWords(self):
    pass

  def decodeSubWords(self):
    pass

input_file_path = os.path.join(os.path.dirname(__file__), "dataset", 'input.txt')
token = Tokenizer(input_file_path)

# encode and decode by character
data = token.encodeCharacters()
# print(data)
print(token.decodeCharacters(data))

# (.venv)
# activate and install dependencies
# python -m training.nanogpt.tokenizer
