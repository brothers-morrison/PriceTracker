
import os
import datetime
import re
from promptflow.core import tool

cache_dir="cache"
prompt='''
# system:
You are an fun an engaging adult learning expert. You have a Ph.D in Adult education.
Act as my consultant. Be as detailed as possible. 
Provide complete examples. Ask any clarifying questions that are needed before beginning the complete answer.

# user:
Using the following inputs:
{{prompt_template_form}}


1) Generate a catchy, memorable course title aligned with the audience and outcomes.
2) Refine and finalize learning outcomes to be specific and measurable.
3) Create a PPT outline with:
   - Opening hook (5–10 min)
   - Repeating 10-minute content + activity blocks
   - Clear transitions between blocks
   - Final summary with key takeaways and next steps
4) Ensure tone, examples, and activities strictly follow the provided inputs.
5) If any input is missing, make conservative, explicitly stated assumptions.
'''



# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    result = prompt.replace('{{prompt_template_form}}', input1)
    
    # Parse title from input1
    lines = input1.strip().split('\n')
    if lines:
        first_line = lines[0].strip()
        if first_line.startswith('# '):
            title = first_line[2:].strip()
        else:
            title = first_line
    else:
        title = "untitled"
    
    # Sanitize title for filename
    title = re.sub(r'[^\w\-_]', '_', title).replace(' ', '_')
    
    # Get current date
    date_str = datetime.date.today().isoformat()
    
    # Create filename
    filename = f"{date_str}_{title}.md"
    cache_path = os.path.join(cache_dir, filename)
    
    # Ensure cache directory exists
    os.makedirs(cache_dir, exist_ok=True)
    
    # Save to cache
    with open(cache_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    return result