# Output setup message
echo "Lisa Plan - Interview Started"
echo ""
echo "Feature: $FEATURE_NAME"
echo "State: $STATE_PATH"
echo "Draft: $DRAFT_PATH"
echo "Output: $SPEC_PATH"
echo "JSON: $JSON_PATH"
echo "Progress: $PROGRESS_PATH"
if [[ -n "$CONTEXT_FILE" ]]; then
  echo "Context: $CONTEXT_FILE"
fi
if [[ $MAX_QUESTIONS -gt 0 ]]; then
  echo "Max Questions: $MAX_QUESTIONS"
else
  echo "Max Questions: unlimited"
fi
if [[ "$FIRST_PRINCIPLES" == "true" ]]; then
  echo "Mode: First Principles (will challenge assumptions first)"
fi
echo ""
echo "The interview will continue until you say \"done\" or \"finalize\"."
echo "All questions will use the AskUserQuestion tool."
echo ""
echo "Beginning interview..."
echo ""
echo "$INTERVIEW_PROMPT"