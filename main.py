import sys
from repo_analyzer import RepoParser
from output_reformatter import OutputReformatter
from meta_descriptor import MetaDescriptionGenerator

class Main:
    def main(self):
        file_path = './key'
        with open(file_path, 'r') as file:
            api_key = file.read().strip()  # Read the key and strip any extra whitespace
            if not api_key:
                raise ValueError("API key is empty.")

        repo = RepoParser('./')
        classes = repo.construct_class_dependencies()
    
        diagram_parser = OutputReformatter(classes)
        formatted_output = diagram_parser.generate_structure()
        diagram_parser.save_to_json("formatted_output.json")

        meta_description_generation = MetaDescriptionGenerator(formatted_output, api_key)
        meta_description_generation.save('meta_description.txt')

if __name__ == '__main__':
    Main().main()


