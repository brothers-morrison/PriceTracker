import json
import sys
from typing import List, Dict, Optional

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
        print(f"Starting interview session for feature: {self.feature_name}")
        if self.initial_context:
            print(f"Initial context: {self.initial_context}")
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
                print(f"Error loading custom questions: {e}. Using defaults.")
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
        
        for question in self.questions:
            print(f"\nQuestion: {question}")
            response = input("Response: ").strip()
            self.responses.append({"question": question, "response": response})
            
            # Basic follow-up: If response is too short, prompt for more details
            if len(response.split()) < 5:
                follow_up = input("That seems brief. Can you elaborate? ").strip()
                if follow_up:
                    self.responses[-1]["follow_up"] = follow_up
                    print("Follow-up noted.")
        
        print("\nInterview completed. Responses collected.")

    def generate_spec(self):
        """
        Synthesize responses into a comprehensive spec document.
        Includes sections: objectives, user stories, acceptance criteria, technical requirements, dependencies, and risks.
        Output in specified format.
        """
        if not self.responses:
            print("No responses available. Please conduct the interview first.")
            return None
        
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
        print("Spec generated successfully.")
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
            print(f"Error loading session: {e}.")

# Example usage
if __name__ == "__main__":
    # Allow command-line args for customization
    import argparse
    parser = argparse.ArgumentParser(description="Run an interview session.")
    parser.add_argument("feature_name", help="Name of the feature")
    parser.add_argument("--initial_context", help="Initial context")
    parser.add_argument("--custom_questions_file", help="Path to custom questions JSON file")
    parser.add_argument("--output_format", choices=['markdown', 'json'], default='markdown', help="Output format for spec")
    parser.add_argument("--save_session", help="Filepath to save session after interview")
    parser.add_argument("--load_session", help="Filepath to load session from")
    args = parser.parse_args()

    session = InterviewSession(args.feature_name, args.initial_context, args.custom_questions_file, args.output_format)
    if args.load_session:
        session.load_session(args.load_session)
    session.start_session()
    questions = session.generate_questions()
    print("Generated questions:")
    for q in questions:
        print(f"- {q}")
    session.conduct_interview()
    spec = session.generate_spec()
    if spec:
        print("\nGenerated Spec:\n", spec)
    if args.save_session:
        session.save_session(args.save_session)
