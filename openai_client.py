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

    def generate_class_description(self, source):
        template_long = """
        You are an expert software engineer and technical writer. Below is the code for a class from a software repository written in Python. Please provide a detailed description of this class in the following format:

        **Purpose:** What is the main responsibility of this class? (I want just a single paragraph)

        [Insert class code here]
        """
        prompt = template_long.replace("[Insert class code here]", source)
        long = self.get_completion(prompt)

        if long is None:
            return ("", "")

        template_short = """
        Can you summarize this in one sentence upto 10 words without markdown
        [Insert string here]
        """

        prompt = template_short.replace("[Insert string here]", long)
        short = self.get_completion(prompt)

        return (short, long)

