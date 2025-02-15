import sys
from repo_analyzer import RepoParser
from output_reformatter import OutputReformatter

class Main:
    def main(self):
        repo = RepoParser('./')
        classes = repo.construct_class_dependencies()
    
        print(classes)
        diagram_parser = OutputReformatter(classes)
        diagram_parser.generate_structure()
        diagram_parser.save_to_json("formatted_output.json")


if __name__ == '__main__':
    Main().main()


