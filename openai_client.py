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

    def generate_class_descriptions(self, class_definitions):
        template = """
        You are an expert software engineer and technical writer. Below is the code for a class from a software repository written in Python. Please provide a detailed description of this class in the following format:

        **Purpose:** What is the main responsibility of this class? (I want just a single paragraph)

        [Insert class code here]
        """

        class_descriptions = {}
        for class_name, source_code in class_definitions.items():
            # Replace placeholder with actual source code
            prompt = template.replace("[Insert class code here]", source_code)
            # print(f"Prompt for class {class_name}:\n{prompt}\n")
            # print(self.get_completion(prompt))
            class_descriptions[class_name] = self.get_completion(prompt)

        return class_descriptions

if __name__ == "__main__":
    file_path = './key'
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()  # Read the key and strip any extra whitespace
            if not api_key:
                raise ValueError("API key is empty.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The key file '{file_path}' does not exist.")
    except IOError as e:
        raise IOError(f"An error occurred while reading the key file: {e}")

    client = OpenAIChatClient(api_key=api_key)

    from repo_analyzer import RepoAnalyzer
    analyzer = RepoAnalyzer("./")
    analysis, class_definitions = analyzer.analyze_repository()

    class_descriptions = client.generate_class_descriptions(class_definitions)
    print(class_descriptions)
