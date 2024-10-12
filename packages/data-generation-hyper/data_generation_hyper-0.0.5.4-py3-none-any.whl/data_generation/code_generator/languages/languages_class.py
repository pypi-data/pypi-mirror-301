import numpy as np
import pandas as pd
import re
import random

class languages_dict:

  def __init__(self, ds, share=None, Total_number=200000, file_name='question', content='answer'):
    """
    Initialize the languages_dict class with the given parameters.

    Args:
    - ds (DataFrame): The DataFrame containing code snippets and their languages.
    - share (dict): A dictionary specifying the share of snippets for each language.
    - Total_number (int): Total number of snippets to consider.
    - file_name (str): Name of the file column in the DataFrame.
    - content (str): Name of the content column in the DataFrame.
    """
    ds = ds.copy()
    self.snippets_index = 'Not yet created, use \'''extract_snippets_to_take\''' function '

    self.ds = ds
    self.language = ds['language'].value_counts().index
    self.lan_count = ds['language'].value_counts()
    self.ds.index = range(len(self.ds))
    self.start_n_lines = {key: [] for key in self.language}
    self.share = [share[key] for key in self.language] if share else None
    self.Total_number = Total_number

  def extract_index(self):
    """
    Function used to extract index of each snippet.
    """
    snippets_index = {}
    language = self.language
    ds = self.ds.copy()

    language_snippets_number = {key: round((value * self.Total_number)//1) for key, value in zip(language, self.share)}

    for lan in language:
      content_len = self.lan_count[lan]
      number = language_snippets_number[lan]
      snippets_index[lan] = []

      while number > content_len:
        sampled = ds[ds['language'] == lan].index.to_list()
        snippets_index[lan].extend(sampled)
        number -= content_len

      if number <= content_len and number > 0:
        sampled = random.sample(ds[ds['language'] == lan].index.to_list(), number)
        snippets_index[lan].extend(sampled)

    self.snippets_index = snippets_index
    return snippets_index

  def split_strings(self, ds):
    """
    Function used to split string using the character "\n".
    """
    lan = self.language
    dataset_list = []
    ds = ds.copy()
    ds['string'] = ds['string'].apply(lambda x: re.split('\n(?!$)', x))
    return ds['string'].apply(lambda x: [i for i in x if i != ''])

  def start(self, strn, language):
    """
    Function to sample the starting point and the number of lines to take.
    """
    n_lines = random.randint(2, 12)

    if len(strn) <= n_lines:
      return strn

    start = random.randint(0, len(strn) - n_lines - 1)
    self.start_n_lines[language].append((n_lines, start, strn[start:start + n_lines]))
    return strn[start:start + n_lines]

  def select_lines(self, language):
    """
    Function that uses all the previous functions to get the snippets of code.
    """
    snippets_to_take = self.extract_index()
    language = self.language
    dataset_list = []
    ds = self.ds.copy()

    for lan in language:
      lan_mask = ds['language'] == lan
      df = ds[lan_mask].copy()
      df = df.loc[snippets_to_take[lan]]
      df['string'] = self.split_strings(df)
      df['string'] = df['string'].apply(lambda x: self.start(x, lan))
      dataset_list.append(df)

    ds = pd.concat(dataset_list, ignore_index=True)
    ds.index = range(len(ds))
    ds['string'] = ds['string'].apply(lambda x: '\n'.join([i.strip() for i in x]))

    return ds

  def seeds(self):
    """
    Function to generate and return the code seeds.
    """
    self.code_seeds = self.select_lines(self.language)
    return self.code_seeds
