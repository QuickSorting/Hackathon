from openai_client import OpenAIChatClient
import json

prompt = """You are an expert in analyzing software repositories. Below is a JSON representation of a dependency graph between classes in a Git repository. The JSON consists of:

Nodes: Representing classes, each with an id, label (class name), and additionalInfo (which contains a description of the class).
Edges: Representing dependencies between classes, where source depends on target.
Your task is to generate a high-level, cohesive description of the repository based on:

The functionality and purpose of each class (from additionalInfo).
How the classes are interconnected (from edges).
The overall structure and architecture of the project based on these dependencies.
The main responsibilities of the repository as a whole.
Here is the JSON data:

Copy
Edit

{}

Instructions:

Give a brief summary of the repository's purpose - max 1 paragraph!"""

class MetaDescriptionGenerator:
    def __init__(self, formatted_output, api_key):
        chat_client = OpenAIChatClient(api_key)

        prompt = prompt.format(json.dumps(formatted_output, indent=2), formatted_output)

        chat_client.get_completion(prompt)

