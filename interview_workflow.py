class InterviewSession:
    """
    Represents an interview session for gathering requirements for a feature or product.
    """

    def __init__(self, feature_name: str, initial_context: str = None):
        """
        Initialize a new interview session.

        Args:
            feature_name (str): The name of the feature or product being interviewed about.
            initial_context (str, optional): Optional initial context, such as high-level goals or existing docs.
        """
        self.feature_name = feature_name
        self.initial_context = initial_context
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
        Questions progress from broad to specific.
        """
        self.questions = [
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
        return self.questions

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
        
        # Generate Markdown spec
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

# Example usage
if __name__ == "__main__":
    session = InterviewSession("User Authentication Feature", "Goal: Secure login for web app")
    session.start_session()
    questions = session.generate_questions()
    print("Generated questions:")
    for q in questions:
        print(f"- {q}")
    session.conduct_interview()
    spec = session.generate_spec()
    if spec:
        print("\nGenerated Spec:\n", spec)
