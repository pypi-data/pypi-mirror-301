import os
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain_core.output_parsers import StrOutputParser
import numpy as np
import time

def fun(snippet):
      
    line_list = []
    snippet_list = snippet.splitlines()

    for i in snippet_list:
        if i != '':          
            line_list.append(i.strip())

    return '\n'.join(line_list)


def model_function(api_key, max_tokens = None, temp = 0.7, model = 'llama-3.1-70b-instruct'):

        
    return ChatOpenAI(
                    base_url="https://api.hyperbee.ai/v1",
                    api_key=api_key,
                    model=model,
                    temperature=temp
                                    )


def problem_text(input,api_key, OSS_problem_prompt, custom = False, request = None, temperature = 0.7, model = 'llama-3.1-70b-instruct'):
    '''  function that take as input a snippet of code and returns a "problem" inspired by the snippets, to be fed to next function for the output of "solution".
        The function also return the number of tokens required by the process  '''
    

    time_to_sleep = 1

    if custom:

        with get_openai_callback() as cb:   
            for _ in range(5):

                problem_model = model_function(api_key, temperature, model = model)
                output_parser = StrOutputParser()
                chain = OSS_problem_prompt | problem_model | output_parser

                try:       
                    problem = chain.invoke({'example': input, 'request': request})

                    if problem == None or problem == "":
                        print('*****problem with problem function*****')
                        continue
                    else:
                        break
                except Exception as exc:
                    problem = np.nan
                    print('*****problem with problem function*****')

                    time_to_sleep += 1
                    time.sleep(time_to_sleep)
                    continue

            tokens_problem = cb

    else:

        with get_openai_callback() as cb:   
            for _ in range(5):

                problem_model = model_function(api_key, temperature, model = model)
                output_parser = StrOutputParser()
                chain = OSS_problem_prompt | problem_model | output_parser

                try:       
                    problem = chain.invoke({'code': input})

                    if problem == None or problem == "":
                        print('*****problem with problem function*****')
                        continue
                    else:
                        break
                except Exception as exc:
                    problem = np.nan
                    print('*****problem with problem function*****')

                    time_to_sleep += 1
                    time.sleep(time_to_sleep)
                    continue

            tokens_problem = cb
    return problem, tokens_problem


def solution_text(problem, api_key, language, OSS_solution_prompt, temperature = 0.5, model = 'llama-3.1-70b-instruct'):
    '''  Function that takes as input "problem" and return a "solution" and the tokens required 
        for the process  '''
    
    time_to_sleep = 1


    with get_openai_callback() as cb:
        
        for _ in range(5):
            solution_model = model_function(api_key, temperature, model = model)
            output_parser = StrOutputParser()
            chain = OSS_solution_prompt | solution_model | output_parser

            try:   
                solution = chain.invoke({'problem': problem, 'language': language})
                if solution == None or solution == "":
                    print('*****problem with solution function*****')
                    continue
                else:
                    break
            except Exception as exc:
                solution = np.nan
                print('*****problem with solution function*****')

                time_to_sleep += 1
                time.sleep(time_to_sleep)
                continue
    
        tokens_solution = cb
    return solution, tokens_solution