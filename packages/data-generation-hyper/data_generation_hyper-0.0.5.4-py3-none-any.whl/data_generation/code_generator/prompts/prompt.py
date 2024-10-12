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

Present your output in: [Problem Description]
"""

OSS_problem_template_2 = """
Code snippet for inspiration:
```
{code}
```

Guidelines for each section:
[Problem Description]: This should be **completely self-contained**, providing all the contextual information one needs to understand and solve the problem. Assume common programming knowledge, but ensure that any specific context, variables, or code snippets pertinent to this problem are explicitly included.
"""

OSS_problem_prompt = ChatPromptTemplate.from_messages(
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
Inlude necessary comments but avoid introductory phrases such as "Here is the solution."

Present your output in: [Solution]
"""

OSS_solution_template_2 = """
```
{problem}
```

Guidelines for each section:
[Solution]: Offer a comprehensive and **correct** coding solution that accurately addresses the [Problem Description]. Try to solve it with {language}
"""

OSS_solution_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(OSS_solution_template_1),
        HumanMessagePromptTemplate.from_template(OSS_solution_template_2),
    ]
)
OSS_solution_prompt


###############################################################################################################################################################
###############################################################################################################################################################
###############################################################################################################################################################


OSS_problem_template_custom = """You are exceptionally skilled at crafting high-quality programming problems. 
You will be asked to create a custom programming problem on the request of a customer, you will be given a example problem as an inspiration. 
The request pertain the topic of the code and not the complexity of the code structure or syntax, the request complexity and the code complexity are two separate requirements. The request and the code snippets might differ significantly, 
if this happens, the customisation request has the priority, but you should still gain insights from the snippets.

Present your output in: [Problem Description]

Example problem for inspiration: '''
cj = cookielib.CookieJar()\npython\nopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))\npython\nopener.addheaders = [('User-agent', 'Mozilla/5.0')]\npython
'''

Here's the user request: "a complex calculus concept"

Important Clarification:
The request pertain the topic of the code and not the complexity of the code structure or syntax, the request complexity and the code complexity are two separate requirements. The request and the problem example might differ significantly, 
the example is inteded just as an inspiration for the structure of the programming problem, its characteristic and its complexity and you should craft a similar problem but around the topic or the domain of the reques.


Guidelines for each section:
[Problem Description]: This should be completely self-contained, providing all the contextual information one needs to understand and solve the problem. Assume common programming knowledge, but ensure that any specific context, variables, or code snippets pertinent to this problem are explicitly included. 
"""

OSS_problem_prompt_custom = ChatPromptTemplate.from_messages(
    [
        OSS_problem_template_custom
    ]
)