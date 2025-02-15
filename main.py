import sys
from repo_analyzer import RepoAnalyzer
from diagram_parser import DiagramParser


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze_repo.py /path/to/repo")
        sys.exit(1)

    repo_path = sys.argv[1]
    analyzer = RepoAnalyzer(repo_path)

    analysis, class_definitions = analyzer.analyze_repository()
    diagram = analyzer.generate_mermaid(analysis)

    diagram_parser = DiagramParser(diagram)
    diagram_parser.to_json("formatted_diagram.json")
