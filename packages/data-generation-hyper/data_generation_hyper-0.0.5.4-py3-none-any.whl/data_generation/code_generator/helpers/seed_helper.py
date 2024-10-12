import numpy as np

def map_to_standard(name, code_languages):
    """
    Maps the input programming language name to a standard format.

    Args:
    - name (str): The input programming language name.
    - code_languages (list): A list of standard programming language names.

    Returns:
    - str or np.nan: The mapped programming language name in standard format or np.nan if not found.
    """
    # Check for C language variations
    if name == 'C' or name == 'c':
        return 'C'
    # Check for C# language variations
    elif name == 'C#' or name == 'c#' or name == 'C #' or name == 'c #':
        return 'C#'
    # Check for C++ language variations
    elif name == 'Cpp' or name == 'C pp' or name == 'cpp' or name == 'c pp':
        return 'C++'
    else:
        # Check if the input name matches any standard language names in the list
        for lang in code_languages:
            if name.lower().capitalize() == lang.lower().capitalize():
                return lang
    # Return np.nan if no match is found
    return np.nan
