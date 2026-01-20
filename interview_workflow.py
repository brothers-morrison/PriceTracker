import json
import sys
from typing import List, Dict, Optional
import time

class InterviewSession:
    """
    Represents an interview session for gathering requirements for a feature or product.
    """

    def __init__(self, feature_name: str, initial_context: str = None, custom_questions_file: Optional[str] = None, output_format: str = 'markdown'):
        """
        Initialize a new interview session.

        Args:
            feature_name (str): The name of the feature or product being interviewed about.
            initial_context (str, optional): Optional initial context, such as high-level goals or existing docs.
            custom_questions_file (str, optional): Path to a JSON file containing a list of custom questions.
            output_format (str): Output format for the spec ('markdown' or 'json').
        """
        self.feature_name = feature_name
        self.initial_context = initial_context
        self.custom_questions_file = custom_questions_file
        self.output_format = output_format
        self.responses = []  # To store responses during the interview
        self.questions = []  # To store generated questions
        self.spec = None  # Placeholder for generated spec

    def start_session(self):
        """
        Start the interview session. This could be expanded to initialize logging, set up state, etc.
        """
        print("Welcome to the Interactive Specification Interview Workflow!")
        print(f"We're here to help you gather requirements for your feature: {self.feature_name}.")
        if self.initial_context:
            print(f"To get started, here's some initial context: {self.initial_context}")
        print("Let's begin by generating some thoughtful questions to guide our conversation.")
        # Future: Integrate with Claude API for conversational start

    def generate_questions(self):
        """
        Generate a series of probing, open-ended questions tailored to the feature domain.
        Questions progress from broad to specific. If a custom file is provided, load from there.
        """
        if self.custom_questions_file:
            try:
                with open(self.custom_questions_file, 'r') as f:
                    self.questions = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Oops, there was an issue loading your custom questions: {e}. No worries, we'll use our default set instead.")
                self.questions = self._default_questions()
        else:
            self.questions = self._default_questions()
        return self.questions

    def _default_questions(self):
        """
        Default set of questions.
        """
        return [
            "What problem does this feature solve?",
            "Who are the primary users of this feature?",
            "What are the key goals and objectives for this feature?",
            "Can you describe the expected workflow or user journey?",
            "What are the main functional requirements?",
            "Are there any non-functional requirements, such as performance or security?",
            "What dependencies or integrations are needed?",
            "What are the potential risks or challenges?",
            "How will success be measured?",
            "What technical details or constraints should be considered?"
        ]

    def conduct_interview(self):
        """
        Conduct the interactive dialogue by iterating through questions, collecting responses,
        and facilitating basic follow-ups (e.g., clarifying vague answers).
        """
        if not self.questions:
            self.generate_questions()
        
        print("\nAlright, let's dive into the interview. I'll ask you a series of questions to help flesh out the requirements.")
        print("Feel free to provide as much detail as you like – the more info, the better the spec!")
        
        for question in self.questions:
            print(f"\n{question}")
            response = input("Your response: ").strip()
            self.responses.append({"question": question, "response": response})
            
            # Basic follow-up: If response is too short, prompt for more details
            if len(response.split()) < 5:
                follow_up = input("That seems a bit brief. Could you tell me more about that? ").strip()
                if follow_up:
                    self.responses[-1]["follow_up"] = follow_up
                    print("Thanks for the extra details – noted!")
        
        print("\nGreat job! We've completed the interview. Now, let's generate your spec based on what we've discussed.")

    def generate_spec(self):
        """
        Synthesize responses into a comprehensive spec document.
        Includes sections: objectives, user stories, acceptance criteria, technical requirements, dependencies, and risks.
        Output in specified format.
        """
        if not self.responses:
            print("It looks like we don't have any responses yet. Please run the interview first.")
            return None
        
        start_time = time.time()  # Start performance timing
        
        # Extract key info from responses (basic mapping; can be enhanced with NLP later)
        objectives = self._extract_from_responses("What are the key goals and objectives for this feature?")
        user_stories = self._extract_from_responses("Who are the primary users of this feature?") + " " + self._extract_from_responses("Can you describe the expected workflow or user journey?")
        acceptance_criteria = self._extract_from_responses("What are the main functional requirements?")
        technical_reqs = self._extract_from_responses("What technical details or constraints should be considered?") + " " + self._extract_from_responses("Are there any non-functional requirements, such as performance or security?")
        dependencies = self._extract_from_responses("What dependencies or integrations are needed?")
        risks = self._extract_from_responses("What are the potential risks or challenges?")
        
        if self.output_format == 'json':
            spec_data = {
                "feature_name": self.feature_name,
                "objectives": objectives or "Not specified.",
                "user_stories": user_stories or "Not specified.",
                "acceptance_criteria": acceptance_criteria or "Not specified.",
                "technical_requirements": technical_reqs or "Not specified.",
                "dependencies": dependencies or "Not specified.",
                "risks": risks or "Not specified."
            }
            self.spec = json.dumps(spec_data, indent=4)
        else:  # Default to markdown
            spec_content = f"""# Specification for {self.feature_name}

## Objectives
{objectives or "Not specified."}

## User Stories
As a {user_stories or "Not specified."}

## Acceptance Criteria
{acceptance_criteria or "Not specified."}

## Technical Requirements
{technical_reqs or "Not specified."}

## Dependencies
{dependencies or "Not specified."}

## Risks
{risks or "Not specified."}
"""
            self.spec = spec_content
        
        end_time = time.time()  # End performance timing
        elapsed_time = end_time - start_time
        print(f"Spec generation completed in {elapsed_time:.4f} seconds. (Performance check: Ensure this remains under 1 second for typical interviews.)")
        
        print("Your spec has been generated successfully! Here's what we came up with:")
        return self.spec

    def _extract_from_responses(self, question_text):
        """
        Helper to extract response text for a given question.
        """
        for resp in self.responses:
            if resp["question"] == question_text:
                response = resp["response"]
                if "follow_up" in resp:
                    response += " " + resp["follow_up"]
                return response
        return ""

    def save_session(self, filepath: str):
        """
        Save the current session state to a JSON file for persistence.
        """
        state = {
            "feature_name": self.feature_name,
            "initial_context": self.initial_context,
            "custom_questions_file": self.custom_questions_file,
            "output_format": self.output_format,
            "responses": self.responses,
            "questions": self.questions,
            "spec": self.spec
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=4)
        print(f"Session saved to {filepath}.")

    def load_session(self, filepath: str):
        """
        Load a session state from a JSON file.
        """
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            self.feature_name = state.get("feature_name", self.feature_name)
            self.initial_context = state.get("initial_context", self.initial_context)
            self.custom_questions_file = state.get("custom_questions_file", self.custom_questions_file)
            self.output_format = state.get("output_format", self.output_format)
            self.responses = state.get("responses", [])
            self.questions = state.get("questions", [])
            self.spec = state.get("spec", None)
            print(f"Session loaded from {filepath}.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Sorry, there was an error loading the session: {e}.")

# Example usage
if __name__ == "__main__":
    # Allow command-line args for customization
    import argparse
    parser = argparse.ArgumentParser(description="Run an interview session for gathering feature requirements.")
    parser.add_argument("feature_name", help="Name of the feature you're interviewing about")
    parser.add_argument("--initial_context", help="Any initial context or background info")
    parser.add_argument("--custom_questions_file", help="Path to a JSON file with your own questions")
    parser.add_argument("--output_format", choices=['markdown', 'json'], default='markdown', help="How you'd like the spec output (default: markdown)")
    parser.add_argument("--save_session", help="Where to save the session for later")
    parser.add_argument("--load_session", help="Path to a saved session to resume")
    args = parser.parse_args()

    session = InterviewSession(args.feature_name, args.initial_context, args.custom_questions_file, args.output_format)
    if args.load_session:
        session.load_session(args.load_session)
    session.start_session()
    questions = session.generate_questions()
    print("\nHere are the questions we'll cover:")
    for q in questions:
        print(f"- {q}")
    session.conduct_interview()
    spec = session.generate_spec()
    if spec:
        print("\nGenerated Spec:\n", spec)
    if args.save_session:
        session.save_session(args.save_session)
