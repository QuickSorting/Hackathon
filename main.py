import sys
from repo_analyzer import RepoAnalyzer
from output_reformatter import OutputReformatter


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze_repo.py /path/to/repo")
        sys.exit(1)

    repo_path = sys.argv[1]
    analyzer = RepoAnalyzer(repo_path)

    analysis, class_definitions = analyzer.analyze_repository()

    diagram_parser = OutputReformatter(analysis)
    diagram_parser.to_json("formatted_output.json")
