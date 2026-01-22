"""
.SYNOPSIS

.FEATURES

1. **Formatted prompt**: Uses f-string to create the exact format you specified
2. **Validation**: Checks if input matches one of the choices exactly
3. **Error handling**: Shows clear error message and re-prompts if validation fails
4. **Freetext mode**: Disables validation when `"*"` or `"FREETEXT"` is in choices
5. **Input sanitization**: Uses `.strip()` to remove leading/trailing whitespace

.EXAMPLE
    # Expected input (a single question):
    input = {
        "name": "Target_Audience",
        "choices": ["role", "seniority", "prior knowledge"]
    }

    # OUTPUT>
    Target_Audience: pick one [role, seniority, prior knowledge]
    > role
    You selected: role
"""
from promptflow.core import tool
from typing import List, Dict, Any

global FREEFORM_MATCHES 
FREEFORM_MATCHES = [None, "", " ", "*","FREE", "FREETEXT","FREEFORM", "any", "etc"]
"""
Look for these specific choice inputs, if any match one of these, then skip validatation on the set.
"""

# Source - https://stackoverflow.com/a
# Posted by joeld, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-22, License - CC BY-SA 4.0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREY = '\033[90m'


@tool
def single_question_answer(field_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prompts user for input based on field configuration and validates against choices.
    
    Args:
        field_config: Dict with 'name' and 'choices' keys
        
    Returns:
        str: The validated user input
    """
    name = field_config["name"]
    choices = field_config["choices"]
    
    # Check if validation should be disabled
    skip_validation = False
    if not any(choices):
        # In case there are NO options provided (blank) -- just treat it like a freeform field.
        # Example
        #   Course_Topic:
        skip_validation = True
    for c in choices:
        skip_validation = (c in FREEFORM_MATCHES)
        if(skip_validation):
            print(f"skipping validation, matched freeform field : '{c}'")
            break
    
    # Format and print the prompt
    choices_str = ", ".join(choices)
    if(skip_validation):
        prompt = f"{name}: freeform answer\n> "
    else:
        prompt = f"{name}: pick one [{choices_str}]\n> "
    
    while True:
        user_input = input(prompt).strip()
        
        # If validation is disabled, accept any input
        if not skip_validation:
            # Validate input against choices
            if user_input not in choices:
                print(f"{bcolors.FAIL}Error:{bcolors.ENDC} '{user_input}' is not a valid choice.")
                print(f"Please enter one of the following: {choices_str}")
                print()
            else:
                break
        else:
            break

    return {
            "name": name,
            "answer": user_input
        }


""" 
.EXAMPLE text usage below:
#"""
if __name__ == "__main__":
    # Example with validation
    field1 = {
        "name": "Target_Audience",
        "choices": ["role", "seniority", "prior knowledge"]
    }
    
    result1 = single_question_answer(field1)
    print(f"You selected: '{bcolors.GREY}{result1}{bcolors.ENDC}'\n")
    
    # Example with freetext
    field2 = {
        "name": "Custom_Field",
        "choices": ["FREETEXT"]
    }
    
    result2 = single_question_answer(field2)
    print(f"You entered:'{bcolors.GREY}{result2}{bcolors.ENDC}'")