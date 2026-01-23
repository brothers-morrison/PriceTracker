from promptflow.core import tool
from typing import List, Dict, Any
from py_single_user_qa import single_question_answer


@tool
def iterate_questions_to_answers(question_obj_json: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Iterate through each field config and collect answers.
    
    Args:
        field_configs: List of field configuration dicts
        
    Returns:
        List of user answers
    """
    answers = []
    
    for question in question_obj_json:
        answer = single_question_answer(question)
        answers.append(answer)
    
    return answers


if __name__ == "__main__":
    # Test
    test_configs = [
        {"name": "Course_Topic", "choices": ["FREETEXT"]},
        {"name": "Target_Audience", "choices": ["role", "seniority", "prior knowledge"]}
    ]
    
    results = iterate_questions_to_answers(test_configs)
    print(f"Results: {results}")