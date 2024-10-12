from typing import List
from pandas import DataFrame
import json
import pandas as pd
import random
import multiprocessing
from joblib import Parallel, delayed
import importlib.resources as pkg_resources
import re
from datasets import load_dataset
from tqdm import tqdm
import pandas as pd


from .code_generator.languages.languages_class import languages_dict
from .code_generator.helpers.seed_helper import map_to_standard

from .code_generator.prompts.prompt_list_and_probabilities import prompt_list, probabilities, prompt_list_custom, probabilities_custom
from .code_generator.helpers.generator_helper import fun, problem_text, solution_text
from .code_generator.helpers.save_batches import save_batch_result_and_concat, save_final
from .generator_custom import generator_helper

class code_generator(generator_helper):

    '''Class that takes various parameters and return a list of synthetically generated scripts of code in various programming languages
    
    custom_prompts : List[str] = problem prompt and solution prompt used to make an LLM generate the scripts. This parameter is used to input custom prompts to use in place of the standard ones.
    prob : List[int] = there are four types of prompts. This parameter is used to change the proportion of the different types.
    share : List[int] = For each of the supported languages, set the proportion of generated snippets of code. It must sum up to 1.
    model : str = LLM model to use in the script generation, the default one is llama 3.1 70b.
    temperatures : List[ int, int] = temperature for problem and solution generation.
    batch_size : int = size of each batch.'''

    def __init__(self, custom_prompt : str = None, 
                 custom_prob: List[int] = None,
                 prob : List[int] = None,
                  share : List[int] = None,
                  Total_number : int = None,
                    model : str = 'llama-3.1-70b-instruct',
                      temperatures : List[int] = [None, None],
                        batch_size : int = None,
                        api_key : str = None):
        
        self.custom = custom_prompt
        self.prob_custom = custom_prob
        self.prob = prob
        self.share = share
        self.Total_number = Total_number
        self.model = model
        self.temperature_problem = temperatures[0]
        self.temperature_solution = temperatures[1]
        self.api_key = api_key
        self.batch_size = batch_size

        #default values of some parameters
        with pkg_resources.open_text('data_generation.code_generator.config', 'arguments.json') as file:
            args = json.load(file)

        for param, value in vars(self).items():
            if not value:
                if args.get(param, None):
                    setattr(self, param, args[param])

    def change_params(self, custom_prompts: str = None, 
                      custom_prob: List[int] = None, 
                prob : List[int] = [None, None],
                  share : List[int] = None,
                  Total_number : int = None,
                    model : str = None,
                      temperatures : List[ int] = [None, None],
                        batch_size : int = None,
                        api_key = None):
        '''Changes the values of parameters assigned during the class creation. Parameters that are not inserted will not be changed, so to leave a parameter unchanged either use None as argument
        or do not include the parameter in the function call'''

        for param, value in locals():
            if value:
                setattr(self, param, value)




#####Post-processing of generated data and code snippets creation      #------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#






    def post_process(self, input_string : str) -> str:
        """
        Post-processes the input string to extract the main content after 'Problem Description:' or 'Solution:'.
        """
        # Initialize an empty list to store non-empty lines without the specified strings
        output = []

        if len(input_string) != 0 and input_string is not None:
            # Split the input string into lines
            lines = input_string.splitlines()

            # Iterate through each line starting from the second line
            if "Problem Description:" in input_string or "[Problem Description]" in input_string or "**Problem Description" in input_string:
                for index in range(len(lines)):
                    if "Problem Description:" in lines[index] or "[Problem Description]" in lines[index] or "**Problem Description" in lines[index]:
                        for sub_index in range(index + 1, len(lines)):
                            if lines[sub_index].strip():
                                output.append(lines[sub_index])
            elif "Solution:" in input_string or "[Solution]" in input_string or "**Solution" in input_string:
                for index in range(len(lines)):
                    if "Solution:" in lines[index] or "[Solution]" in lines[index] or "**Solution" in lines[index]:
                        for sub_index in range(index + 1, len(lines)):
                            if lines[sub_index].strip():
                                output.append(lines[sub_index])

            # Join the cleaned non-empty lines to form the new string
            output = '\n'.join(output)            

        return output
    

    def get_seed(self):
        """
        Function to retrieve code snippets dataset based on specified share and total number.

        Args:
        - share (dict): A dictionary specifying the share of snippets for each language.
        - Total_number (int): Total number of snippets to consider.

        Returns:
        - DataFrame: The processed code snippets dataset.
        """
        # Load the dataset from glaiveai/glaive-code-assistant-v3
        # with pkg_resources.open_binary('data_generation.code_generator.code_dataset', 'dataset.pkl') as file:
        #     ds = pkl.load(file)
        ds = load_dataset('glaiveai/glaive-code-assistant-v3')
        ds = ds['train']['answer']
        ds = pd.DataFrame(ds, columns=['string'])
        # Define regex pattern and lambda function to extract code snippets
        pattern = r'```(.*?)```'
        lambda_fun = lambda x: re.findall(pattern, x, re.DOTALL)
        ds['string'] = ds['string'].map(lambda_fun)

        # Filter out empty and short snippets
        ds = ds[ds['string'].apply(lambda x: x != [])]
        Series = ds[ds['string'].apply(lambda x: len(x) > 1)]
        ds.loc[Series.index, 'string'] = Series['string'].apply(lambda x: [''.join(x)])
        ds = ds[ds['string'].apply(lambda x: len(x[0]) > 30)]

        # Flatten the list of code snippets and drop duplicates
        ds['string'] = ds['string'].apply(lambda x: x[0])
        ds = ds.drop_duplicates()
        ds.reset_index(drop=True, inplace=True)

        # Define the source languages
        source = [
            "C",
            "C++",
            "C#",
            "CMake",
            "Dockerfile",  # Solutions are to require Dockerfile
            "Go",
            "HTML",
            "Java",
            "JavaScript",
            "Kotlin",
            "Makefile",  # Solutions are to require Makefile
            "PHP",
            "Python",
            "R",
            "Ruby",
            "Rust",
            "Shell",
            "Swift",
            "SQL",
            "Typescript"
        ]  # Language you want to check

        # Extract language from snippets and standardize language names
        ds['language'] = ds['string'].apply(lambda x: re.findall(r'(\S+)', x)[0]) 
        ds['string'] = ds['string'].apply(lambda x: '\n'.join([i for i in re.split(r'\n(?!$)', x)[1:] if i != ''])) 
        ds['language'] = ds['language'].apply(lambda x: map_to_standard(x, source))

        # Sort by language and drop duplicates again
        ds.sort_values(by='language', ascending=False, inplace=True)
        ds.drop_duplicates(subset='string', inplace=True)
        ds.dropna(inplace=True)
        
        # Create languages_dict object to process and extract snippets
        languages = languages_dict(ds, share=self.share, Total_number=self.Total_number)
        snippets_dataset = languages.seeds()

        self.snippets_dataset = snippets_dataset




#####Functions that manage the generation of the scripts #-------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def generate_training(self, n_jobs : int =None, 
                        test : bool =False, batch_path : str = None, data_frame_path : str = None) -> DataFrame:
        """
        Main function to generate training data by processing batches of code snippets.
        """
        # Get the initial dataset and preprocess it
        snippets_dataset = self.snippets_dataset
        snippets_dataset = snippets_dataset.dropna()
        snippets_dataset['string'] = snippets_dataset['string'].apply(lambda x: fun(x))
        snippets_dataset = snippets_dataset.dropna().drop_duplicates(subset='string')

        print("snippets_dataset--->", len(snippets_dataset))

        # Split the dataset into batches
        batch_list = [snippets_dataset[i:i+self.batch_size] for i in range(0, len(snippets_dataset), self.batch_size)]

        if test:
            batch_list = batch_list[:2]  # Use only a few batches for testing purposes
        
        if not n_jobs:
            n_jobs = min(multiprocessing.cpu_count(), 20)  # Set the number of jobs for parallel processing

        results = []

        def process_and_save(batch, index):
            """
            Function to process a batch and save the result with tqdm progress tracking.
            """
            
            if self.custom:
                with tqdm(total=1, desc=f"Processing Batch {index}") as pbar:
                    result = self.custom_generator(batch=batch)
                    
                    results.append(result)
                    pbar.update(1)  # Update the progress bar to indicate completion of the batch
                    
                save_batch_result_and_concat(result, index, batch_path )  # Save the processed batch and concatenate with previous batches
                return result
        
            else:
                with tqdm(total=1, desc=f"Processing Batch {index}") as pbar:
                    result = self.generator(batch=batch)
                    
                    results.append(result)
                    pbar.update(1)  # Update the progress bar to indicate completion of the batch
                    
                save_batch_result_and_concat(result, index, batch_path )  # Save the processed batch and concatenate with previous batches
                return result

        print("generation process started")
        # Use parallel processing to process and save each batch
        Parallel(n_jobs=n_jobs, prefer="threads")(
            delayed(process_and_save)(batch, index) for index, batch in enumerate(tqdm(batch_list))
        )

        # Concatenate all results into a single DataFrame
        final_df = pd.concat(results, ignore_index=True)

        save_final(final_df, data_frame_path)

        return final_df



#####Function to call all the process once all the parameters are set      #-------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


    def generate(self, n_jobs : int = None, test : bool = False, batch_path : str = None, data_frame_path : str = None) -> DataFrame:

        '''generate a dataframe with code scripts in various languages given the parameter assigned'''

        return self.generate_training(n_jobs, test, batch_path, data_frame_path)
