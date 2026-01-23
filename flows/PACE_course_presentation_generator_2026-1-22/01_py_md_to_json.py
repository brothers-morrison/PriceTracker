from promptflow.core import tool
from typing import List, Dict, Any
#import sys
import json
import re

DEBUG_VERBOSE=False

question_answering='''
Please answer the following questions to help us better serve you:
'''

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

@tool
def markdown_to_json(markdown_text: str) -> List[Dict[str, Any]]:
    """
    Convert markdown list items to JSON objects.
    
    Args:
        markdown_text (str): Single line or multiline markdown list items
        
    Returns:
        list or dict: List of JSON objects if multiline, single dict if single line
        
    Example:
        >>> markdown_to_json("- Target_Audience (role, seniority, prior knowledge):")
        {'name': 'Target_Audience', 'choices': ['role', 'seniority', 'prior knowledge']}
    """
    # Check if input contains multiple lines
    lines = [line.strip() for line in markdown_text.strip().split('\n') if line.strip()]
    
    # Process multiple lines
    return [parse_single_line(line) for line in lines if not (line.startswith('#') or line.startswith('['))] 



CHOICE_DELIMITER=','

def parse_single_line(text):
    """
    Parse a single markdown list item.
    
    Args:
        text (str): Single markdown list item
                Example: "- Outcome_Level: (awareness / application / mastery)"
        
    Returns:
        dict: JSON object with 'name' and 'choices' fields
    """
    if '\n' in text:
        raise ValueError("got multiline input")
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove the leading dash and whitespace
    text = re.sub(r'^-\s*', '', text)
    
    
    is_optional = re.match(r'optional', text.lower())

    # Extract name and choices using regex
    # Pattern: capture name before '(', then capture everything inside parentheses
    
    class reg_set:
        """regex helper sets"""
        def __init__(self, input):
            self.input = input
        def set(self):
            return f'[{self.input}]'
        def neg(self):
            return f'[^{self.input}]'

    # set of parens, brackets, or curly braces
    open_set = reg_set(r'\(\[\{\:')
    close_set = reg_set(r'\)\[\}')

    
    cap_name = f"({open_set.neg()}+)"
    space_opt_colon = r'\s*\:?\s*'


    open = open_set.set()
    cap_choices = f"({close_set.neg()}+)"
    close = close_set.set()
    reg = f'{cap_name}{space_opt_colon}{open}{cap_choices}{close}'
    if(DEBUG_VERBOSE):
        print("Regex chunks:")
        print(f"cap_name: {cap_name}")
        print(f"space_opt_colon: {space_opt_colon}")
        print(f"open: {open}")
        print(f"cap_choices: {cap_choices}")
        print(f"close: {close}")
        print(f"Full regex: {reg}")
    match = re.match(reg, text)
    
    if match:
        
        # expected inputs, with either brackets or parens
            # name: [choices, in, brackets]
            # name: (choices, in, parens)

        # EXAMPLES:
        #   Delivery_Format: (live workshop, lecture, async, executive briefing, etc.)
        #   Industry_or_Domain (optional):
        if(DEBUG_VERBOSE):
            for g in match.groups():
                print(g)

        name = match.group(1).strip()
        # Remove trailing colon if present
        name = name.strip().rstrip(':')

        choices_str = match.group(2)
        choices_str = choices_str.rstrip(':')
        
        # Split choices by comma and strip whitespace from each
        # handle this (awareness / application / mastery)
        choices_str = choices_str.replace('/', CHOICE_DELIMITER).replace('\\', CHOICE_DELIMITER)
        choices = [choice.strip() for choice in choices_str.split(CHOICE_DELIMITER)]
        
        special_words=[
            'optional',
            'if any',
            'bullet list',
            'bullet list of observable skills or knowledge',
            'minutes',
            'default: 10 mins'
        ]
        for wd in special_words:
            while wd in choices:
                choices.remove(wd)

        return {
            "name": name,
            "choices": choices,
            "default_choice_index" : 0
        }
    else:
        # No parentheses found - just a name
        return {
            "name": text.strip().strip(':'),
            "choices": [],
            "default_choice_index" : 0
        }


# Example usage
if __name__ == "__main__":
    # Test with the new multiline input
    multiline_input = """
- Course_Topic:
- Outcome_Level: (awareness / application / mastery)
- Industry_or_Domain (optional):
- Delivery_Format: (live workshop, lecture, async, executive briefing, etc.)
"""
    
    print("=== Multiline Input Test ===")
    print("Input:")
    print(multiline_input)
    print("\nOutput:")
    result = markdown_to_json(multiline_input)
    print(json.dumps(result, indent=2))