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
Please gain inspiration from the following random code snippet to create programming problem.
You have to imagine that who's asking the problem is a person with basic-to-medium programming skills.
The text of the problem should be phrased simply and be conversational but
the task itself should be highly complex and require advanced knowledge of programming to be solved. 
The problem shall contain only a few hints and constraits.
Keep in mind that, even thought the problem is asked by a intermediate-beginner, it will be a practionioner with advanced level of programming skills to solve the problem.

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

OSS_problem_prompt_complex_conversational = ChatPromptTemplate.from_messages(
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

OSS_solution_prompt_complex_conversational = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(OSS_solution_template_1),
        HumanMessagePromptTemplate.from_template(OSS_solution_template_2),
    ]
)