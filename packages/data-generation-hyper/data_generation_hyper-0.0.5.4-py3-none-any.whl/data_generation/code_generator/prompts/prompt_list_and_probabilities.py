from .prompt import OSS_problem_prompt, OSS_solution_prompt, OSS_problem_prompt_custom
from .complex_prompt import OSS_problem_prompt_complex, OSS_solution_prompt_complex, OSS_problem_prompt_complex_custom
from .complex_brief_prompt import OSS_problem_prompt_complex_brief, OSS_solution_prompt_complex_brief
from .complex_conversational_prompt import OSS_problem_prompt_complex_conversational, OSS_solution_prompt_complex_conversational


prompt_list = [(OSS_problem_prompt, OSS_solution_prompt), (OSS_problem_prompt_complex, OSS_solution_prompt_complex),
               (OSS_problem_prompt_complex_brief, OSS_solution_prompt_complex_brief), (OSS_problem_prompt_complex_conversational, OSS_solution_prompt_complex_conversational)]

probabilities = [0, 1, 0, 0]

#-------------------------------------------------------------------------------------------

# CUSTOM PROMPT

#-------------------------------------------------------------------------------------------

prompt_list_custom = [(OSS_problem_prompt_custom, OSS_solution_prompt), (OSS_problem_prompt_complex_custom, OSS_solution_prompt_complex),]

probabilities_custom = [0.7, 0.3]  