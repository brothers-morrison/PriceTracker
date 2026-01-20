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

# Example usage
if __name__ == "__main__":
    session = InterviewSession("User Authentication Feature", "Goal: Secure login for web app")
    session.start_session()
    questions = session.generate_questions()
    print("Generated questions:")
    for q in questions:
        print(f"- {q}")
