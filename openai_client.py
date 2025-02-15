import openai

class OpenAIChatClient:
    def __init__(self, api_key):
        """
        Initializes the OpenAI client with the provided API key.
        """
        self.client = openai.OpenAI(api_key=api_key)

    def get_completion(self, user_input):
        """
        Sends a chat completion request to the OpenAI API based on the user input
        and returns the completion as a string.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Specify the model here. Adjust as necessary for different models.
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content # Assumes that the completion structure includes 'content'.
        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    api_key = "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"
    client = OpenAIChatClient(api_key=api_key)

    from repo_analyzer import RepoAnalyzer
    analyzer = RepoAnalyzer("./")
    analysis, class_definitions = analyzer.analyze_repository()
    print(type(class_definitions))
    print(class_definitions)

    exit(0)
    
    user_input = "Write a haiku about recursion in programming."
    print(client.get_completion(user_input))
