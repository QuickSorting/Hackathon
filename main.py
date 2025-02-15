import sys
from repo_analyzer import RepoParser
from output_reformatter import OutputReformatter
from meta_descriptor import MetaDescriptionGenerator

class Main:
    def main(self):
        repo = RepoParser('./')
        classes = repo.construct_class_dependencies()
    
        print(classes)
        diagram_parser = OutputReformatter(classes)
        diagram_parser.generate_structure()
        diagram_parser.save_to_json("formatted_output.json")

        meta_description_generation = MetaDescriptionGenerator()
        meta_description_generation.save('meta_description.txt')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze_repo.py /path/to/repo")
        sys.exit(1)

    Main().main()


