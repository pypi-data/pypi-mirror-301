import random
from pandas import DataFrame

from .code_generator.prompts.prompt_list_and_probabilities import prompt_list, probabilities, prompt_list_custom, probabilities_custom
from .code_generator.helpers.generator_helper import fun, problem_text, solution_text



class generator_helper:

    def custom_generator(self, batch: DataFrame) -> DataFrame: 


        # Create a copy of the batch to avoid SettingWithCopyWarning
        batch = batch.copy()

        if self.prob_custom: 
            OSS_problem_prompt_custom, OSS_solution_prompt = random.choices(prompt_list_custom, self.prob_custom)[0] 

        else:
            OSS_problem_prompt_custom, OSS_solution_prompt = random.choices(prompt_list_custom, probabilities_custom)[0]

        OSS_problem_prompt, _ = random.choices(prompt_list, probabilities)[0]

        
        # Generate problem and solution texts
        probl_text = batch['string'].apply(lambda x: problem_text(fun(x), self.api_key, OSS_problem_prompt, 
                                                    model=self.model, temperature=self.temperature_problem))
        
        batch['problem_text_custom'] = probl_text.apply(lambda x: problem_text(x, self.api_key, OSS_problem_prompt_custom, custom = True, 
                                                                               request = self.custom,
                                                                                model=self.model, temperature=self.temperature_problem))

        batch['solution_text'] = batch.apply(lambda x: solution_text(x['problem_text_custom'], self.api_key, x['language'], OSS_solution_prompt, 
                                            model=self.model, temperature=self.temperature_solution), axis=1)
        
        # Extract tokens from the generated texts
        batch['problem_tokens'] = batch['problem_text_custom'].apply(lambda x: x[1])
        batch['solution_tokens'] = batch['solution_text'].apply(lambda x: x[1])

        # Extract only the text part, discard the tokens
        batch['problem_text_custom'] = batch['problem_text_custom'].apply(lambda x: x[0])
        batch['solution_text'] = batch['solution_text'].apply(lambda x: x[0])

        # Apply post-processing to extract the main content
        batch['problem_text_custom'] = batch['problem_text_custom'].apply(lambda x: self.post_process(x))
        batch['solution_text'] = batch['solution_text'].apply(lambda x: self.post_process(x))

        return batch


        





    def generator(self, batch : DataFrame) -> DataFrame:
        """
        Function to generate problem and solution texts along with their tokens for a given batch of data.
        """
        # Create a copy of the batch to avoid SettingWithCopyWarning
        batch = batch.copy()

        if self.prob: 
            OSS_problem_prompt, OSS_solution_prompt = random.choices(prompt_list, self.prob)[0]

        else:
            OSS_problem_prompt, OSS_solution_prompt = random.choices(prompt_list, probabilities)[0]

        # Generate problem and solution texts
        batch['problem_text'] = batch['string'].apply(lambda x: problem_text(fun(x), self.api_key, OSS_problem_prompt, 
                                                    model=self.model, temperature=self.temperature_problem))
        

        batch['solution_text'] = batch.apply(lambda x: solution_text(x['problem_text'], self.api_key, x['language'], OSS_solution_prompt, 
                                            model=self.model, temperature=self.temperature_solution), axis=1)
        
        # Extract tokens from the generated texts
        batch['problem_tokens'] = batch['problem_text'].apply(lambda x: x[1])
        batch['solution_tokens'] = batch['solution_text'].apply(lambda x: x[1])

        # Extract only the text part, discard the tokens
        batch['problem_text'] = batch['problem_text'].apply(lambda x: x[0])
        batch['solution_text'] = batch['solution_text'].apply(lambda x: x[0])

        # Apply post-processing to extract the main content
        batch['problem_text'] = batch['problem_text'].apply(lambda x: self.post_process(x))
        batch['solution_text'] = batch['solution_text'].apply(lambda x: self.post_process(x))

        return batch

