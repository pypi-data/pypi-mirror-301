from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

#---------------------------------------------------------------------------------------------
# PROBLEM PROMPT
#---------------------------------------------------------------------------------------------

OSS_problem_template_1 = """
You are exceptionally skilled at crafting high-quality programming problems.
Please gain inspiration from the following random code snippet to create a high-quality programming problem.
Problems are intended for advanced practitioners that know deeply how to program and are trained 
to solve highly structured and complex problem, so the complexity and structure of the problem should reflect a task that require exceptional programming skills to be completed. 

Present your output in: [Problem Description]
"""

OSS_problem_template_2 = """
Code snippet for inspiration:
```
{code}
```

Guidelines for each section:
[Problem Description]: This should be **completely self-contained**, providing all the contextual information one needs to understand and solve the problem. Ensure that any specific context, variables, or code snippets pertinent to this problem are explicitly included.
"""

OSS_problem_prompt_complex = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(OSS_problem_template_1),
        HumanMessagePromptTemplate.from_template(OSS_problem_template_2),
    ]
)

#---------------------------------------------------------------------------------------------
# SOLUTION PROMPT
#---------------------------------------------------------------------------------------------

OSS_solution_template_1 = """
You are exceptionally skilled at offering precise coding solutions to high-quality programming problems.
Include necessary comments but avoid introductory phrases such as "Here is the solution."
Solution you are supposed to produce should be extremely detailed and are intended to be on par with those of advanced level practitioners, that know deeply how to program and are trained 
to solve highly structured and complex problem. The complexity and structure of the code should be chosen to reflect a solution that require exceptional programming skills to be completed. 
If the problem is simple produce a simple, yet high level code.

Present your output in: [Solution]
"""

OSS_solution_template_2 = """
```
{problem}
```

Guidelines for each section:
[Solution]: Offer a comprehensive and **correct** coding solution that accurately addresses the [Problem Description]. Try to solve it with {language}
"""

OSS_solution_prompt_complex = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(OSS_solution_template_1),
        HumanMessagePromptTemplate.from_template(OSS_solution_template_2),
    ]
)


###############################################################################################################################################################
###############################################################################################################################################################
###############################################################################################################################################################

OSS_problem_template_custom = """
You are exceptionally skilled at crafting high-quality programming problems.
You will be asked to create a custom high-quality programming problem on the request of a customer, you will be given a problem example as an inspiration for you.
The coding problems are intended for advanced practitioners that know deeply how to program and are trained 
to solve highly structured and complex problem, so the complexity and structure of the problem should reflect a programming task that require exceptional programming skills to be completed, indipendently from the topic of the request. 
Present your output in: [Problem Description]
problem example for inspiration:
```
{example}
```
User request: {request}

Important Clarification:
When you are told that the problem should be challenging also for avanced practitioners, it means from a programming point of view only(like including dynamic programming, caching, parallelization and other algorithmic and programming advanced skills). The difficulty of other aspects or the topic domain(matehmatics, web scraping etc), are irrelevant
in this regard and should not be accounted in the complexity of the program from a programming exclusive point of view.

Guidelines for each section:
[Problem Description]: This should be **completely self-contained**, providing all the contextual information one needs to understand and solve the problem. Ensure that any specific context, variables, or code snippets pertinent to this problem are explicitly included.
"""

OSS_problem_prompt_complex_custom = ChatPromptTemplate.from_messages(
    [
        OSS_problem_template_custom
    ]
)